import numpy as np
import pandas as pd
import datetime
import  from package

df_index = pd.date_range(datetime.date(2000,1,1), datetime.date(2030,1,1))

df_date = pd.DataFrame()

df_date["date"] = df_index.strftime("%F")
df_date["year"] = df_index.strftime("%Y")
df_date["month"] = df_index.strftime("%m")
df_date["day"] = df_index.strftime("%d")
df_date["week"] = df_index.strftime("%w")
df_date["week"] = df_date["week"].replace("0", "7")
df_date["month_full_name"] = df_index.strftime("%B")
df_date["month_short_name"] = df_index.strftime("%b")
df_date["week_full_name"] = df_index.strftime("%A")
df_date["week_short_name"] = df_index.strftime("%a")

