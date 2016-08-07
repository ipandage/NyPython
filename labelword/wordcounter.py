import os
import openpyxl
import time
import chardet
import re

def wordcut(text):
    delete='[\s+\.\!\/_,$%^*\(\d+\"\']+|[；！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;]+'
    text=re.sub(delete,' ',text)
    words=text.split(' ')
    result={}
    for word in words:
        if word==' ' or word=='':
            continue
        try:
            result[word.lower()]+=1
        except:
            result[word.lower()]=1
    return result

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    return coding['encoding']

def load_deletewords():
    encoding=get_chardet('settings/deletewords')
    if encoding=='GB2312':
        encoding='GBK'
    deletewords=[]
    for line in open('settings/deletewords','r',encoding=encoding):
        deletewords.append(line.replace('\r','').replace('\n','').replace(' ',''))
    return deletewords

def wordcounter(filename,deletewords):
    encoding=get_chardet('data/'+filename)
    if encoding=='GB2312':
        encoding='GBK'
    text=open('data/'+filename,'r',encoding=encoding).read()
    words=wordcut(text)
    result={}
    for key in words:
        if len(key)==1:
            continue
        if key not in deletewords:
            result[key]=words[key]
    result=sorted(result.items(),key=lambda x:x[1],reverse=True)
    write_to_excel(result,filename)

def write_to_excel(words,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in words:
        sheet.append(item)
    excel.save('result/%s.xlsx'%(filename.replace('.txt','')))

def main():
    try:
        deletewords=load_deletewords()
    except:
        deletewords=[]
    for filename in os.listdir('data'):
        if filename.endswith('txt'):
            try:
                wordcounter(filename,deletewords)
            except:
                print(filename,'failed')
                continue
            print(filename,'ok')
    time.sleep(50)

main()
