import requests
from datetime import datetime,timedelta
from .models import Manga
import json

client_id = "HHGSX"
client_secret = "edwinelliotevans"


def make_session():
        
        # define URL for the login API endpoint
        url = 'https://api.mangadex.org/auth/login'
        
        # dictionary creation
        data = {'username' : "HHGSX", "password" : 'edwinelliotevans'}

        # sends a POST request to the API with the data dictionary
        response = requests.post(url, json=data)
        response_json = response.json()

        # then checks if the response status is 200 (OK)
        if response.status_code != 200:
             print("response.status_code")
             raise Exception ('failed to log in to MangaDex API')


        # extract the variables bellow from the response JSON
        session_token = response_json['token']
        expires_in = response_json['expiresIn']
        expires = datetime.now() + timedelta(seconds=expires_in)
        refresh_token = response_json['resfresh']

        return session_token,expires , refresh_token


class MangaDex:

    def __init__(self):
        self.session_token ,self.refresh_token,self.expires = make_session()
        self.base_url = "https://api.mangadex.org"
        


    #manga 
    def get_manga_by_id(self,manga_id:str) -> Manga:

        # send GET request to the API with the authorization from the function before
        url = f'{self.base_url}/manga/{manga_id}'
        headers = {'Autorization':f'Bearer{"session_token"}'}

        response = requests.get(url ,headers=headers)
        response_json = response.json()

        # extract variables below
        manga_id = response['data']['id']
        title = response_json['data']['attributes']['title']['en']
        description = response_json['data']['attributes']['description']['en']
        cover_art = response_json['data']['attributes']['cover_art']
        authors = [author['attributes']['name'] for author in response_json['data']['relationships'] if author['type'] == 'author']

        # creates a manga object with the extracted information and returns it
        return Manga(manga_id,title,description,cover_art,authors)
 





"""r = Request(
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
        return manga"""


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