import requests
import json
import threading
import time

lock=threading.Lock()
num=0

def ip_location(ip):
    url='http://apis.baidu.com/showapi_open_bus/ip/ip'
    headers={
        'apikey':'6910ed2c5831ea4f22c2333c08670ef8'
    }
    res_p=requests.get(url+'?ip='+ip,headers=headers,timeout=30).text
    result=json.loads(res_p)
    code=result['showapi_res_code']
    if code==0:
        return result['showapi_res_body']
    return False

class IP(threading.Thread):
    def __init__(self,ip,date):
        super(IP,self).__init__()
        self.ip=ip
        self.date=date

    def run(self):
        try:
            self.result=ip_location(self.ip)
        except:
            self.result=False
        if self.result!=False:
            self.result['date']=self.date
            with lock:
                global num
                f=open('ips.txt','a')
                f.write(str(self.result)+'\n')
                f.close()
                num+=1
                print(num,self.ip,'ok')

def get_location():
    lines=[line.replace('\n','').split(',') for line in open('log.txt','r')]
    all_num=0
    while len(lines):
        threadings=[]
        count=0
        while count<30:
            try:
                line=lines.pop()
                work=IP(line[0],line[-1])
                threadings.append(work)
                count+=1
                all_num+=1
            except:
                break
        for work in threadings:
            work.start()
        time.sleep(3)
        print(all_num)

get_location()
