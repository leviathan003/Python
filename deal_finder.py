from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request as urllib

s=HTMLSession()
dealList=[]

def site_connect():
    site='https://www.amazon.in'
    response=urllib.urlopen(site)
    if response.getcode()== 200:
        print("Connected with code: ",response.getcode())
    else:
        print("Connection failed")
        exit(1)


print(".....Welcome to Python Deal Finder.....")
print("Search site: Amazon")
site_connect()

search_query=input("Enter item to Search for sale in Amazon: ")
if ' 'in search_query: 
    first,second=search_query.split(' ')
    search_query=first+'+'+second
print(search_query)
url= f'https://www.amazon.in/s?k={search_query}&i=todays-deals'


def get_Data(url):
    r=s.get(url)
    r.html.render(sleep=20)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def get_Deal(soup):
    products=soup.find_all('div',{'data-component-type': 's-search-result'})
    for item in products:
        title=item.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()
        short_title=item.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:30]
        link=item.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
        sale_price=float(item.find_all('span',{'class':'a-price-whole'})[0].text.strip().replace('₹','').replace(',',''))
        orig_price=float(item.find_all('span',{'class':'a-offscreen'})[1].text.strip().replace('₹','').replace(',',''))
        try:
            review_nos=item.find('span',{'class':'a-size-base s-underline-text'}).text.strip()
        except:
            review_nos=0
        #print(short_title,sale_price,orig_price,review_nos,link)
    
        sale_item={
            'title':title,
            'short_title':short_title,
            'link':link,
            'sale_price':sale_price,
            'orig_price':orig_price,
            'reviews':review_nos
        }

        dealList.append(sale_item)

def get_Nextpg(soup):
    pages=soup.find('span',{'class':'s-pagination-strip'})
    if pages==None:
        return
    if not pages.find('span',{'class':'s-pagination-item s-pagination-next s-pagination-disabled'}):
        url= 'https://www.amazon.in'+str(pages.find('a',{'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
        return url
    else:
        return
#s-pagination-item s-pagination-next s-pagination-disabled
while(True):
    data=get_Data(url)
    get_Deal(data)
    print(url)
    print(len(dealList))
    url=get_Nextpg(data)
    if not url:
        break

df=pd.DataFrame(dealList)
df['percentoff']=100-((df.sale_price/df.orig_price)*100)
df=df.sort_values(by=['percentoff'],ascending=False)
print(df.head())