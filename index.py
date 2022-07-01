# 导入Flask类
from flask import Flask, jsonify
# from flask import render_template
from flask import request
from flask_cors import CORS
from jinja2 import Undefined
import threading
import logging
from logging.handlers import RotatingFileHandler

from Comm import JsonEncoderCustom
from Controller import Photo
from Controller import spider
import datetime

# 实例化，可视为固定格式
app = Flask(__name__)
CORS(app, supports_credentials=True)

# route()方法用于设定路由；类似spring路由配置
@app.route('/helloworld')
def hello_world():
    Photo.Photo().addUser('admin','123456','F:\漫画\灌篮高手','http://192.168.31.248:50010')
    return 'Hello, World!'

@app.route('/rest_test',methods=['Get'])
def hello_world1():
    """
    通过request.json以字典格式获取post的内容
    通过jsonify实现返回json格式
    """
    #post_param = request.json
    param=request.path
    result_dict = {
        "result_code": 2000,
        "post_param": param
    }
    return jsonify(result_dict)

### api
#获取照片
@app.route('/photo/getAllPhoto',methods=['Get'])
def get_photo():
    userid=request.args.get("userid")
    return Success(Photo.Photo().getAllPhoto(userid))

#获取userid对应的tag
@app.route('/photo/getTagsByUserId',methods=['Get'])
def getTagsByUserId():
    userid=request.args.get("userid")
    return Success(Photo.Photo().getTagsByUserId(userid))

#添加userid对应的tag
@app.route('/photo/addTagsByUserId',methods=['Post'])
def addTagsByUserId():
    userid=request.form.get("userid")
    tagname=request.form.get("tagname")
    return Success(Photo.Photo().addTagsByUserId(userid,tagname))

#添加照片tag
@app.route('/photo/addPhotoByTag',methods=['Post'])
def addPhotoByTag():
    post_param = request.json
    return Success(Photo.Photo().addPhotoByTag(post_param.get('userid'),post_param.get('tags'),post_param.get('photoid')))

#获取照片tag
@app.route('/photo/getPhotoByTag',methods=['Post'])
def getPhotoByTag():
    post_param = request.json
    return Success(Photo.Photo().getPhotoByTag(post_param.get('userid'),post_param.get('tagid')))

@app.route('/photo/getPhotoById',methods=['Post'])
def getPhotoById():
    post_param = request.json
    return Success(Photo.Photo().getPhotoById(post_param.get('userid'),post_param.get('photoid')))

@app.route('/spider/start',methods=['Get'])
def spiderStart():
    thread = threading.Thread(target=spider.Start)
    thread.start()
    return Success("spider start ok")

@app.route('/spider/stop',methods=['Get'])
def spiderStop():
    spider.Stop()
    return Success("spider start ok")

@app.route('/spider/qsize',methods=['Get'])
def spiderQsize():
    return Success({"qsize": spider.q.qsize(),"errlist":spider.errlist,"suclist":spider.suclist})

@app.route('/spider/addurl',methods=['Get'])
def spiderAddurl():
    url=request.args.get("url")
    return Success(spider.AddUrl(url))

def Success(data,message=None):
    return JsonEncoderCustom.JsonEncoderCustom().encode({
        'code':0,
        'message':message,
        'data':data,
        'operationTime':datetime.datetime.now()
    })

def Fail(message=None,code=1):
    return jsonify({
        'code':code,
        'message':message,
        'data':None,
        'operationTime':datetime.datetime.now()
    })

def SetLogger():
    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler =logging.handlers.RotatingFileHandler("logs/log.txt", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    SetLogger()
    spiderStart()
    app.run(host="0.0.0.0", port=5000)