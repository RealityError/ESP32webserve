#数据库(简单表)初始化
from datause import database

#引用一些变量
from init import *

user = database(database_user,'user')
print(user.find_C(2))


