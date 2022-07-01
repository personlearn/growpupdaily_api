import urllib3
import requests
import re
import os
from queue import Queue
import time
import logging


logger = logging.getLogger('flask.app')
#logger.info('flask.app')
#from flask import current_app
#current_app.logger.info('logged by current_app from main')

q=Queue();
errlist=[]
suclist=[]
isstart=False;
def AddUrl(url):
    q.put(url)
    return "ok";

def Start():
    global isstart;
    isstart=True;
    logger.info('启动spider成功')
    #current_app.logger.info('启动spider成功')
    exec();

def Stop():
    global isstart;
    isstart=False

def exec():
    while isstart:
        if not q.empty():
            url=q.get()
            try:
                html=gethtml(url)
                getphoto(html)
                suclist.append(url)
                logger.info('下载：'+url+' 成功')
                #current_app.logger.info('下载：'+url+' 成功')
            except Exception as e:
                #current_app.logger.info('下载：'+url+'报错：'+ e)
                logger.info('下载：'+url+'报错：'+str(e))
                errlist.append(url)

        time.sleep(3);

def gethtml(url): 
    #  忽略警告：InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
    requests.packages.urllib3.disable_warnings()
    # 一个PoolManager实例来生成请求, 由该实例对象处理与线程池的连接以及线程安全的所有细节
    http = urllib3.PoolManager()
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    # 通过request()方法创建一个请求：
    r = http.request('GET',
             url,
             #fields={'wd': 'hello'},
             headers=header)
    #print(r.status) # 200
    #print(r.data.decode())
    #html=r.data.decode();
    return r.data.decode();

def getphoto(html):
    pattern=re.compile(reg);
    result=re.findall(pattern,html);
    title=re.search(re.compile(regtitle),html).group(1);
    http = urllib3.PoolManager();
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'} 
    print(result)
    folder='F:/图片/test/'+title;
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    #print(html);
    for res in result:
        r = http.request('GET',
             res,
             #fields={'wd': 'hello'},
             headers=header)
        filename=res.split("/")[-1]
        print(r.status) # 200
        with open(folder+'/'+filename,'wb') as f:
            f.write(r.data);

#reg="ess-data[\w\W]*?http.*?(jpg|gif|png|bmp)"
#reg="ess-data</span>='<[^>]+>(.*?)</[^>]+>"
reg="<img.*?ess-data='(.*?)'>"
regtitle="<title>(.*?)</title>"
#html=gethtml("");
# with open("D:/pcode/growpupdaily_api/Asset/test.html") as file_object:
#     contends = file_object.read();
#     getphoto(contends);
#getphoto(html);
    

