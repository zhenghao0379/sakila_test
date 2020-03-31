# 定位到工作根目录
# import sys
# from os.path import abspath, join, dirname
# sys.path.insert(0, join(abspath(dirname(__file__)), '\..\..'))

# 加载环境文件
from package.env import *
from package.sql_connect import *

# 加载工具包
import pandas as pd
import time
import pendulum


# 自定义函数


# 主体
l_hours = [i for i in range(0, 24)]
l_minutes = [i for i in range(0, 60)]
l_seconds = [i for i in range(0, 60)]

index = pd.MultiIndex.from_product([l_hours, l_minutes, l_seconds], names = ["hours24", "minutes", "seconds"])

df_data = pd.DataFrame(index=index).reset_index()

df_data['hours12'] = df_data['hours24'].apply(lambda x: x % 12)
df_data['am_pm'] = df_data['hours24'].apply(lambda x: 'AM' if x < 12 else 'PM')

df_data['time_value'] = df_data['hours24'].apply(lambda x: '0' if x < 10 else '') + df_data['hours24'].astype(str) + ':' + \
                        df_data['minutes'].apply(lambda x: '0' if x < 10 else '') + df_data['minutes'].astype(str) + ':' + \
                        df_data['seconds'].apply(lambda x: '0' if x < 10 else '') + df_data['seconds'].astype(str)

df_data['time_key'] = df_data.index.values + 1

print(df_data.head())
# 载入数据
dev()
conn, engine = mysql_on("sakila_dwh_py")
mysql_upload(df_data, "dim_time", conn, engine, type="r", update_time=False)
mysql_close(conn, engine)
