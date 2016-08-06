import os
import re
import chardet

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    return coding['encoding']

def wordlabel(filename,limitnum,delwords,colors):
    encoding=get_chardet('data/'+filename)
    if encoding=='GB2312':
        encoding='GBK'
    text=open('data/'+filename,'r',encoding=encoding).read()
    words=wordcut(text)
    html='<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<meta charset="utf-8">\r\n<title>{title}</title>\r\n</head>\r\n<body>{body}\r\n</body>\r\n</html>'
    body=''
    textline='<p>{line}</p>'
    wordcolor='<font color="{color}">{word}</font>'
    points=['.',',','?','!',"'",'《','》',':',';','"','\r\n','\n']
    for line in open('data/'+filename,'r',encoding=encoding):
        body+=textline.format(line=line)+'\r\n'
    for word in words:
        if word in delwords:
            continue
        if len(word)==1:
            continue
        if words[word]>=limitnum:
            num=words[word]
            color=''
            for item in colors:
                if num>item[0]:
                    color=item[1]
                    break
            if color=='':
                color='Salmon'
            for point in points:
                body=body.replace(' '+word+point,' '+wordcolor.format(color=color,word=word)+point)
                body=body.replace(' '+word.capitalize()+point,' '+wordcolor.format(color=color,word=word.capitalize())+point)
                body=body.replace(point+word+' ',point+wordcolor.format(color=color,word=word)+' ')
                body=body.replace(point+word.capitalize()+' ',point+wordcolor.format(color=color,word=word.capitalize())+' ')
            body=body.replace(' '+word+' ',' '+wordcolor.format(color=color,word=word)+' ')
            body=body.replace(' '+word.capitalize()+' ',' '+wordcolor.format(color=color,word=word.capitalize())+' ')
    return html.format(body=body,title=filename.replace('.txt',''))

def load_deletewords():
    encoding=get_chardet('settings/deletewords')
    if encoding='GB2312':
        encoding='GBK'
    deletewords=[]
    for line in open('settings/deletewords','r',encoding=encoding):
        deletewords.append(line.replace('\r','').replace('\n','').replace(' ',''))
    return deletewords

def loadcolor():
    encoding=get_chardet('settings/color')
    if encoding='GB2312':
        encoding='GBK'
    colors={}
    for line in open('settings/color','r',encoding=encoding):
        line=line.replace('\r','').replace('\n','').replace(' ','')
        try:
            colors[int(line.split('-')[0])]=line.split('-')[-1]
        except:
            continue
    colors=sorted(colors.items(),key=lambda x:x[0],reverse=True)
    return colors

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

def main():
    colors=loadcolor()
    delwords=load_deletewords()
    while True:
        try:
            limit=input('输入词频限度：')
            limit=int(limit)
            break
        except:
            print('输入不合法，重新输入')
    for filename in os.listdir('data'):
        if filename.endswith('txt'):
            try:
                html=wordlabel(filename,limit,delwords,colors)
            except:
                print(filename,'failed')
                continue
            f=open('result/%s.html'%(filename.replace('.txt','')),'w',encoding='utf-8')
            f.write(html)
            f.close()
main()
