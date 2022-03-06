#!/user/bin/python
# -*- coding:utf-8 -*-
# 作者：realityerror
# 创建：2022-03-06
# 更新：2022-03-06
# 用意：搭建网站的主题目录




#网站初始化
import os
from flask import Flask, render_template, Response, make_response, request, session
from config import Config
import json
#数据库(简单表)初始化
from datebase import datause


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        




if __name__ == '__main__':
    app.run()