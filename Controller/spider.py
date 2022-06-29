import urllib3
import requests
import re

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
    print(html);
    for res in result:
        r = http.request('GET',
             res,
             #fields={'wd': 'hello'},
             headers=header)
        filename=res.split("/")[-1]
        print(r.status) # 200
        with open('F:/图片/test/'+filename,'wb') as f:
            f.write(r.data);

#reg="ess-data[\w\W]*?http.*?(jpg|gif|png|bmp)"
#reg="ess-data</span>='<[^>]+>(.*?)</[^>]+>"
reg="<img.*?ess-data='(.*?)'>"
regtitle="<title>(.*?)</title>"
html=gethtml("");
# with open("D:/pcode/growpupdaily_api/Asset/test.html") as file_object:
#     contends = file_object.read();
#     getphoto(contends);
getphoto(html);
    

