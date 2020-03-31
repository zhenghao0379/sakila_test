# 环境文件

# 载入工具包
import datetime
import os
import configparser

# 设置路径
path = os.path.dirname(os.path.abspath(__file__))
# 读取config.ini
config = configparser.ConfigParser()
config.read(path + '\..\config\config.ini')
# 设置工作目录（绝对路径）
workspace = config.get('default', 'workspace')
print('workspace =', workspace)
os.chdir(workspace)

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


class global_val:
    def __init__(self):
        self.DATE = DATE
        self.DATETIME = DATETIME
        self.DAYS = DAYS
        self.RPT_TYPE = RPT_TYPES

    def get_val(self, item):
        pass

    def set_val(self, item):
        pass
print("env load")