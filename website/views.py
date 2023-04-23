from flask import Blueprint, render_template, request,flash,jsonify
import requests
from flask_login import login_required

views = Blueprint('views' , __name__)



@views.route('/', methods=['GET', 'POST'])

def display_manga():
    url = "https://community-manga-eden.p.rapidapi.com/list/0"

    headers = {
	"content-type": "application/octet-stream",
	"X-RapidAPI-Key": "c050c47ec0mshbad7e0b618d47f1p1c6d33jsn884f15dde2fd",
	"X-RapidAPI-Host": "community-manga-eden.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    return render_template('home.html')












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