import pandas as pd
import pymysql
import sqlalchemy
from .env import DATE, DATETIME, DAYS, RPT_TYPES

# 定义连接的全局变量
CONNS = ""
CONN = ''
ENGINE = ''
MYSQL_USER = ""


# 环境切换
def mysql_env(env='test'):
    global CONNS
    db = pd.read_csv("config/db.csv")
    if env == 'test':
        CONNS = db.loc[db['state'] == 'test']
        print("it`s test env now!")
    else:
        CONNS = db.loc[db['state'] == 'dev']
        print("it`s dev env now!")

# 测试环境
def test():
    global CONNS
    db = pd.read_csv("config/db.csv")
    CONNS = db.loc[db['state'] == 'test']
    print("it`s test env now!")


# 正式环境
def dev():
    global CONNS
    db = pd.read_csv("config/db.csv")
    CONNS = db.loc[db['state'] == 'dev']
    print("it`s dev env now!")


# 选择数据库
def mysql_on(db_name):
    global CONNS, MYSQL_USER, CONN, ENGINE
    mysql_user = {
        "host": CONNS.loc[CONNS["db_name"] == db_name, "host"].item(),
        "port": CONNS.loc[CONNS["db_name"] == db_name, "port"].item(),
        "user": CONNS.loc[CONNS["db_name"] == db_name, "user"].item(),
        "password": CONNS.loc[CONNS["db_name"] == db_name, "password"].item(),
        "db_name": db_name
    }
    MYSQL_USER = mysql_user
    # conn
    conn = pymysql.connect(
        host=mysql_user["host"],
        user=mysql_user["user"],
        passwd=mysql_user["password"],
        database=db_name,
        charset='utf8'
    )
    print(conn)
    # engine
    url = "mysql+pymysql://" + str(mysql_user["user"]) + ":" + str(mysql_user["password"]) + "@" + str(
        mysql_user["host"]) + ":" + str(mysql_user["port"]) + "/" + db_name + "?charset=utf8"
    engine = sqlalchemy.create_engine(url, echo=False, encoding='utf-8')
    print(engine)
    CONN = conn
    ENGINE = ENGINE
    return conn, engine


# 获取数据
def mysql_download(table_name, sql, engine, day, rpt_type):
    sql = "select * from where day = {day} and rpt_type = {rpt_type}".format_map(vars())
    df_data = pd.read_sql(sql, engine)
    return df_data


# 载入数据
def mysql_upload(df, table_name, conn, engine, type, update_time=True, rpt_type=RPT_TYPES, *day):
    global DATETIME, MYSQL_USER
    db_name = MYSQL_USER["db_name"]
    if update_time:
        df["upload_time"] = DATETIME
    print(df.dtypes)

    # 判断table_name 是否在数据库中
    table_names = \
        pd.read_sql("select table_name from information_schema.tables WHERE table_schema = '{db_name}'".format_map(
            vars()), engine)["table_name"]
    print(table_names)
    if table_name in table_names.values:
        print(f"OK, {table_name}  in {db_name}.")
    else:
        return print("ERROR! {table_name} not in {db_name}.".format_map(vars()))

    # 载入数据
    if type == "replace" or type == "r":
        # 替换：为了保留源数据库字段格式
        # 先清空表
        sql = "DELETE FROM {table_name}".format_map(vars())
        print(sql)
        cursor = conn.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            conn.commit()
        except:
            # 发生错误时回滚
            conn.rollback()
        df.to_sql(table_name, engine, if_exists="append", index=False)
    elif type == "day" or type == "d":
        # 替换：为了保留源数据库字段格式
        # 先清空表
        sql = "DELETE FROM {table_name} where day='{day}'".format_map(vars())
        print(sql)
        cursor = conn.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            conn.commit()
        except:
            # 发生错误时回滚
            conn.rollback()
        df.to_sql(table_name, engine, if_exists="append", index=False)
    elif type == "append" or type == "a":
        df.to_sql(table_name, engine, if_exists="append", index=False)
    else:
        print("need type value")

    return print(f"upload {table_name} to {db_name} success !")


def mysql_close(conn=CONN, engine=ENGINE):
    conn.close()
    engine.dispose()
    print("the connector has been closed!")


def kill_all_connector():

    pass


def add_label():
    pass
