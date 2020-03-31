# 环境文件

# 载入工具包
import datetime

# 全局变量
# 时间
DATE = datetime.datetime.now().strftime("%Y-%m-%d")
print("DATE:", DATE)
DATETIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("DATETIME:", DATETIME)

# azkaban变量
DAYS = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")
print("DAYS:", DAYS)
RPT_TYPES = "D"
print("RPT_TYPES:", RPT_TYPES)

print("env load")