#!/user/bin/python
# -*- coding:utf-8 -*-
# 作者：realityerror
# 创建：2022-03-06
# 更新：2022-03-06
# 用意：搭建网站


from ast import Global
import socket
from wsgiref.simple_server import make_server

#网站初始化
from asyncio.windows_events import NULL
import re, os 
import pickletools
from flask import Flask, render_template, Response, make_response, request, session
from flask_cors import *

from config import Config
import json

#数据库(简单表)初始化
from datause import database

#引用一些变量
from init import *

#调用摄像头
from camera import VideoCamera

#渲染图标
from jinja2 import Markup
from pyecharts import options as opts
from pyecharts.charts import Bar
import random

#多网卡情况下，根据前缀获取IP
def GetLocalIPByPrefix(prefix):
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip
     
    return localIP
     

app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SECRET_KEY'] = '$%^&*()345671231adFGHJBHJK,./'




#------------------------------主页面业务-------------------------------
#主页获取
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == 'GET':
        return render_template('main.html')

#主页面业务-注册
@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')   
        use_tmp = database(database_user,'user')
        if password is not NULL and email is not NULL and password is not NULL:
            data = use_tmp.find_C(2)
            for i in data:
                print(i)
                if name in i:
                    return render_template('main.html', msg="该用户已经注册")
            use_tmp.set_one(use_tmp.max_x(),1,"普通用户")         
            use_tmp.set_one(use_tmp.max_x(),2,name)
            use_tmp.set_one(use_tmp.max_x(),3,email)
            use_tmp.set_one(use_tmp.max_x(),4,password)
            return render_template('index.html','注册成功,请登录')
        else:
            return render_template('main.html',msg="有错误")


#主页面业务-登录
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('main.html')
    else:
        email = request.form.get('email_login')
        password = request.form.get('password_login') 
        use_tmp = database(database_user,'user')
        email_data = use_tmp.find_C(3)


        for i in range(use_tmp.user.max_column):
            if email == email_data[i]:
                if use_tmp.find_one(i+1,4) == password:
                    session['username'] = use_tmp.find_one(i+1,2)
                    picture_src = use_tmp.find_one(i+1,5)    
                    if picture_src == None:
                        picture_src = '/static/picture/index/ro.png'
                    return render_template('index.html',
                    picture = picture_src,
                    name = use_tmp.find_one(i+1,2) 
                    
                    
                    )
                else:
                    return render_template('main.html',msg="密码错误")
        return render_template('main.html',msg="该用户不存在")    
        
#----------------------------------------------------------------------




#-------------------------404错误响应----------------------------------

@app.errorhandler(404)
def page_unauthorized(error):
    return render_template('404.html'), 404

#----------------------------------------------------------------------


#------------------------------服务端业务-------------------------------
#index页面跳转逻辑
@app.route("/index", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return render_template('main.html')
    return render_template('index.html')

#欢迎页面
@app.route("/welcome",methods=["GET", "POST"])
def welcome():
    if 'username' not in session:
        return render_template('main.html')
    ro_tmp = database(database_ro,'data')

    return render_template('welcome.html',
        robot_data = ro_tmp.zidian_ro()
    
    
    
    
    )

#获取机器人信息
@app.route("/robot",methods=["GET", "POST"])
def robot():
    if 'username' not in session:
        return render_template('main.html')



    #获取机器人的信息    
    ro_tmp = database(database_ro,'data')
    ro_info = database(database_ro,'info')  
    ro_data = database(database_ro,'json') 



    return render_template('robot_data.html',
      robot_data = ro_tmp.zidian_ro(),
      robot_info = ro_info.zidian_ro(),
      robot_json = ro_data.zidian_ro()
    
    )



#病人体征图表
def bar_base() -> Bar:
  c = (
    Bar()
      .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
      .add_yaxis("商家A", [random.randint(10, 100) for _ in range(6)])
      .add_yaxis("商家B", [random.randint(10, 100) for _ in range(6)])
      .set_global_opts(title_opts=opts.TitleOpts(title="", subtitle=""))
  )
  return c

@app.route("/bar")
def get_chart():
  return render_template('text.html')

@app.route("/barChart")
def get_bar_chart():
  c = bar_base()
  return c.dump_options_with_quotes()




#-----------------------------------------------------------------------





#----------------------------远程摄像头服务------------------------------
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
 
@app.route('/camera', methods=["GET", "POST"])
def video_on():
    if 'username' not in session:
        return render_template('main.html')

    if request.method == 'GET':
        ro_tmp = database(database_ro,'data')
        ro_ip = database(database_ro,'ip_CAM')
        return render_template('camera.html',
        robot_data = ro_tmp.zidian_ro(),
        IP = json.dumps(ro_ip.zidian_ro())
    )
    if request.method == 'POST':
        global IP_USE
        IP_USE = request.form.get('IP')
        print(IP_USE)

        ro_tmp = database(database_ro,'data')
        ro_ip = database(database_ro,'ip_CAM') 


        return render_template('camera.html',
        robot_data = ro_tmp.zidian_ro(),
        IP = json.dumps(ro_ip.zidian_ro())
        )
    

@app.route('/video_feed',methods=["GET", "POST"])
def video_feed():
    if 'username' not in session:
        return render_template('main.html')
    global IP_USE
    print("用户正在调用摄像头")
    return Response(gen(VideoCamera(IP_USE)), mimetype='multipart/x-mixed-replace; boundary=frame')

#-----------------------------------------------------------------------



#主程序运行
if __name__ == '__main__':
    IP_USE = ''
    print("已检索到本地IP"+GetLocalIPByPrefix('192.168'))
    print("正在开启网络服务")
    app.run(host = GetLocalIPByPrefix('192.168'),threaded=True)

