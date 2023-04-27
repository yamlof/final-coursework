from flask import Blueprint, render_template, request,flash,jsonify,Flask
import requests
from flask_login import login_required
from .mangadex_api import MangaDex

views = Blueprint('views' , __name__)



@views.route('/', methods=['GET', 'POST'])
def display_manga():
    mangadex = MangaDex()
    manga = mangadex.get_manga_by_id('')
    return render_template('home.html',manga=manga)
    

@views.route('/manga',methods=['GET','POST'])
def manga_details():
    return render_template("manga.html")





    """endpoint = 'https://api.mangadex.org'
    manga_id = 'f98660a1-d2e2-461c-960d-7bd13df8b76d'
    r = requests.get(f"{endpoint}/manga/{manga_id}/feed")
    processed_data = [chapter["id"] for chapter in r.json()["data"]]
    return render_template('home.html', data=jsonify(processed_data))"""

    """response = requests.get('https://api.mangadex.org')
    data = response.json()
    processed_data = process_data(data)
    return render_template('views.home',data = jsonify(processed_data))

def process_data(data):
    data_dict = json.loads(data)
    manga_id = "f98660a1-d2e2-461c-960d-7bd13df8b76d"
    r = requests.get(f"{data_dict}/manga/{manga_id}/feed")

    processed_data = ([chapter["id"] for chapter in r.json()["data"]])
    return processed_data"""












""""  mangafreak = Mangafreak()

    # make a GET request to the base URL
    response = mangafreak.client.get(mangafreak.base_url)

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # select all manga items on the page
    manga_elements = soup.select('.item')

    # create a list of manga objects from the HTML elements
    manga_list = []
    for manga in manga_elements:
        manga = mangafreak.manga_from_element(manga, 'a')
        manga_list.append(manga)

    # render a template with the manga list
    return render_template('home.html', manga_list=manga_list)"""


"""mangafreak = Mangafreak()

    response = mangafreak.client.get(mangafreak.base_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    manga_elements = soup.select('.item')

    manga_list = []
    for manga in manga_elements:
        manga = mangafreak.manga_from_element(BeautifulSoup, str)
        manga_list.append(manga)

    return render_template('home.html',manga_list=manga_list)"""