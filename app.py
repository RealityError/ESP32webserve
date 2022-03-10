#!/user/bin/python
# -*- coding:utf-8 -*-
# 作者：realityerror
# 创建：2022-03-06
# 更新：2022-03-06
# 用意：搭建网站




#网站初始化
from asyncio.windows_events import NULL
import os
import pickletools
from flask import Flask, render_template, Response, make_response, request, session
from config import Config
import json

#数据库(简单表)初始化
from datause import database

#引用一些变量
from init import *

#调用摄像头
from camera import VideoCamera

app = Flask(__name__)
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
    ro_tmp = database(database_ro,'data')

    return render_template('camera.html',
        robot_data = ro_tmp.zidian_ro(),
        IP = IP
    
    
    
    )

@app.route('/video_feed',methods=["GET", "POST"])
def video_feed():
    if 'username' not in session:
        return render_template('main.html')
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

#-----------------------------------------------------------------------
#主程序运行
if __name__ == '__main__':
    app.run(host='0.0.0.0')