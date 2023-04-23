from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import requests
from website.models import Manga
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

r = Request(
    url='https://w15.mangafreak.net/',
    headers={'User-Agent':'Mozilla/5.0'})

class Mangafreak():
    
    # properties of the class

    name: str = "Mangafreak"
    lang: str = "en"
    base_url: str = "https://w15.mangafreak.net/"
    supports_latest: bool = True

    # initializes client attribute by calling "setup_client"
    def __init__(self) -> None:
        self.client = self.setup_client(
            timeout=(1,1) ,retries = 3 , redirects = True ,verify_ssl=True
        )
    
    # makes the HTTP requests
    def setup_client(self , **kwargs) -> requests.Session:
        session = requests.Session()
        retry= Retry(connect=3,backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session
    
    
    @staticmethod
    def manga_from_element( element:BeautifulSoup,url_selector: str) -> range:
        manga=Manga(
            cover = element.select_one("img").get("abs:src"),
            title=element.select_one(url_selector).text,
            url = element.select_one(url_selector).get("href"),
        )
        return manga


    # returns a manga object with its atributes

    

"""def latest_titles_scraping():

    mangafreak = Mangafreak()

    titles = mangafreak.latest_titles()
    for title in titles:
        print(title.title, title.thumnail_url ,title.url)
   
    webpage=urlopen(r).read()

    soup = BeautifulSoup(webpage, 'html.parser')

    img_items=soup.find('div',{'class':'latest_list'})
    img_div= img_items.find_all(class_='image')
    manga_weblink = img_items.find_all('href',class_="image")

    for img in img_div:
        images=img.find('img')
        #prints image source link
        image_link=(images['src'])
        #outputs title
        image_name=(images['alt'])
        print(image_name,image_link)
    
    for manga_weblink in img_div:
        print(manga_weblink['href'])"""


"""latest_titles_scraping()"""

"""def latest_titles_scraping():
   
    webpage=urlopen(r).read()

    soup = BeautifulSoup(webpage, 'html.parser')

    img_items=soup.find('div',{'class':'latest_list'})
    img_div= img_items.find_all(class_='image')

    for img in img_div:
        images=img.find('img')
        #prints image source link
        image_link=(images['src'])
        #outputs title
        image_name=(images['alt'])
        response = requests.get(image_link)
        with open(image_name,'wb') as f:
            f.write(response.content)"""