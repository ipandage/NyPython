import requests
import json
import json
from bs4 import BeautifulSoup
import base64

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
    book_text=''
    for page in book['pages']:
        book_text+=article_content(book['bookid'],page['articleUuid'],page['bigContentId'])+'\n'
        print(page['title'])
    with open('book.html','w') as f:
        f.write(book_text)

if __name__ == '__main__':
    book=get_book('d050cae1f7cf4137ac28109827cbe90b_4')
    download(book)
