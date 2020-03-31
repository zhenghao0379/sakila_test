# 定位到工作根目录
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../..'))


import numpy as np
import os, sys
import pandas as pd
import datetime
import calendar
import pendulum

from package.env import *
print(1)
from package.sql_connect import *
print(2)

# 自定义函数
def week_in_month(date_value):
    dt = pendulum.parse(date_value)
    return int(dt.week_of_month)


def quarter_number(x):
    if '01' <= x <= '03':
        return '01'
    elif '04' <= x <= '06':
        return '02'
    elif '07' <= x <= '09':
        return '03'
    elif '10' <= x <= '12':
        return '04'
    else:
        return 'error'

df_index = pd.date_range(datetime.date(2000,1,1), datetime.date(2030,1,1))

df_date = pd.DataFrame()

df_date["date_key"] = df_index.strftime("%Y%m%d")
df_date["date_value"] = df_index.strftime("%F")
df_date["date_short"] = df_index.strftime("%D")
df_date["date_medium"] = df_index.strftime("%b %d, %Y")
df_date["date_long"] = df_index.strftime("%B %d, %Y")
df_date["date_full"] = df_index.strftime("%A, %B %d, %Y")
df_date["day_in_year"] = df_index.strftime("%j")
df_date["day_in_month"] = df_index.strftime("%d")
df_date["day_abbreviation"] = df_index.strftime("%a")
df_date["day_name"] = df_index.strftime("%A")
df_date["week_in_year"] = df_index.strftime("%W")
df_date["week_in_month"] = df_date["date_value"].apply(week_in_month)
df_date["is_first_in_week"] = df_date["day_abbreviation"].apply(lambda x: 'yes' if x == 'Mon' else 'no')
df_date["is_last_in_week"] = df_date["day_abbreviation"].apply(lambda x: 'yes' if x == 'Sun' else 'no')
df_date["month_number"] = df_index.strftime("%m")
df_date["month_abbreviation"] = df_index.strftime("%b")
df_date["month_name"] = df_index.strftime("%B")
df_date["year2"] = df_index.strftime("%y")
df_date["year4"] = df_index.strftime("%Y")
df_date["quarter_name"] = df_date["month_number"].apply(quarter_number) + 'Q'
df_date["quarter_number"] = df_date["month_number"].apply(quarter_number)
df_date["year_quarter"] = df_date["year4"] + '-' + df_date["quarter_name"]
df_date["year_month_number"] = df_index.strftime("%Y-%m")
df_date["year_month_abbreviation"] = df_index.strftime("%Y-%b")

dev()
conn, engine = mysql_on("sakila_dwh_py")

mysql_upload(df_date, "load_dim_date", conn, engine, type="r")