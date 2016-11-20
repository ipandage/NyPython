import re
import datetime

def clear():
    f=open('log.txt','w')
    for line in open('log.out','r'):
        try:
            result=re.findall('(\d+\.\d+\.\d+\.\d+).*?\[(.*?)\] (.*?) =>',line)[0]
        except:
            continue
        date_str=datetime.datetime.strptime(result[1],'%a %b %d %H:%M:%S %Y')
        date_str=date_str.strftime("%Y-%m-%d %H:%M:%S")
        print(date_str)
        f.write(','.join(result)+',%s\n'%date_str)
    f.close()

clear()
