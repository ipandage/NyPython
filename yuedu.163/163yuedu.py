import requests
import json
import json
from bs4 import BeautifulSoup
import base64
import time
import pdfkit


headers = {
    'Host':"yuedu.163.com",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def book_list(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'yd-book-content'}).find_all('div',{'class':'yd-book-item'})
    result=[]
    for item in table:
        book={}
        book['title']=item.find('h2').get_text()
        book['bookid']=item.find('a').get('href').split('/')[-1]
        book['imgurl']=item.find('img').get('src')
        book['author']=item.find('div',{'class':'author-container'}).get_text().replace('\r','').replace('\n','').replace('作者：','')
        book['des']=item.find('div',{'class':'summery'}).find('p').get_text()
        result.append(book)
    return result

def get_book(bookid):
    html=requests.get('http://yuedu.163.com/getBook.do?id='+bookid,headers=headers).text
    data=json.loads(html)
    book={}
    book['title']=data['title']
    book['bookid']=data['id']
    book['author']=data['author']
    book['coverImg']=data['coverImg']
    book['shareDescription']=data['shareDescription']
    pages=[]
    for item in data['portions']:
        page={}
        page['title']=item['title']
        page['articleUuid']=item['id']
        page['bigContentId']=item['bigContentId']
        pages.append(page)
    book['pages']=pages
    return book

def article_content(bookid,articleUuid,bigContentId=''):
    html=requests.get('http://yuedu.163.com/getArticleContent.do?sourceUuid={sourceUuid}&articleUuid={articleUuid}&bigContentId={bigContentId}'.format(sourceUuid=bookid,articleUuid=articleUuid,bigContentId=bigContentId),headers=headers).text
    data=json.loads(html)
    article=base64.b64decode(data['content'])
    return article.decode()

def download(book):
    html='''<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title></title>
        </head>
        <body>
            {body}
        </body>
    </html>'''
    book_text=''
    for page in book['pages']:
        book_text+=article_content(book['bookid'],page['articleUuid'],page['bigContentId'])+'<br><br><br>\n'
        time.sleep(0.2)
    html=html.format(body=book_text)
    filename=book['title']+'.pdf'
    html2pdf(html,filename)

def html2pdf(html,filename):
    options={
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_string(html,filename,options=options)

if __name__ == '__main__':
    books=book_list('http://yuedu.163.com/book/category/category/800/1_0_1')
    for book in books:
        book=get_book(book['bookid'])
        download(book)
        print(book['title'],'ok')
