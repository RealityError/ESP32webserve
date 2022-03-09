#初始化一些数据库位置
database_user = "./database/database_user.xlsx"
database_ro = "./database/database_ro.xlsx"
IP_use = "./database/IP.txt"

f = open(IP_use,"r")   #设置文件对象
IP = f.read()     #将txt文件的所有内容读入到字符串str中
f.close()   #将文件关闭

