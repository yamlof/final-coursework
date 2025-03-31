from flask import Blueprint, render_template,flash
from .mangareques import chapter_request
from .models import User,Chapters
import os,requests
from . import db

views = Blueprint('views' , __name__)



@views.route('/', methods=['GET', 'POST'])
def display_manga():

    return render_template('home.html')
    

@views.route('/manga',methods=['GET','POST'])
def manga_details():
    return render_template("base_manga.html")

@views.route('/manga/sololeveling',methods=['GET', 'POST'])
def solo_leveling():
    return render_template("sololeveling.html")

@views.route('/manga/onepiece',methods=['GET', 'POST'])
def one_piece():
    return render_template("onepiece.html")

@views.route('/manga/jujutsukaisen',methods=['GET', 'POST'])
def jujutsu_kaisen():
    manga_id = "c52b2ce3-7f95-469c-96b0-479524fb7a1a"  # Jujutsu Kaisen manga ID
    base_url = "https://api.mangadex.org"
    
    try:
        # Fetch chapters for the manga
        response = requests.get(
            f"{base_url}/manga/{manga_id}/feed",
            params={"translatedLanguage[]": ["en"]}
        )
        
        if not response.ok:
            return render_template("error.html", error=f"API error: {response.status_code}"), response.status_code
        
        chapters_json = response.json()
        
        # Process each chapter (you might want to limit this to avoid overloading)
        for chapter_data in chapters_json['data']:  # Limit to first 10 chapters
            chapter_id = chapter_data['id']
            chapter_num = chapter_data['attributes']['chapter']
            chapter_title = chapter_data['attributes']['title']
            
            # Check if chapter already exists in database
            existing_chapter = Chapters.query.filter_by(chapter_number=chapter_num).first()
            if not existing_chapter:
                # Get manga title
                manga_info = requests.get(f"{base_url}/manga/{manga_id}")
                if manga_info.ok:
                    manga_title = manga_info.json()['data']['attributes']['title']['en']
                    
                    # Add to database
                    new_chapter = Chapters(
                        title=chapter_title,
                        chapter_number=chapter_num,
                        manga_title=manga_title
                    )
                    
                    try:
                        db.session.add(new_chapter)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(f"Database error: {str(e)}")
        
        # Get all chapters from database
        data = Chapters.query.filter_by(manga_title="Jujutsu Kaisen").order_by(Chapters.chapter_number).all()
        
        return render_template("jujutsukaisen.html", data=data)
    
    except Exception as e:
        print(f"Error in jujutsu_kaisen route: {str(e)}")
        return render_template("error.html", error=str(e)), 500

@views.route('/manga/jujutsukaisenchapter/<chapter_id>',methods=['GET', 'POST'])
def jujutsu_kaisen_chapter(chapter_id):
    # API URL to fetch chapter metadata (replace 'chapter_id' with actual ID)
    api_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    
    # Send GET request to the API to fetch the chapter's metadata
    response = requests.get(api_url)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract the base URL and image data
        base_url = data.get("baseUrl", "")
        image_data = data.get("chapter", {}).get("data", [])
        image_urls = []

        # Construct the full URLs for each image
        if base_url and image_data:
            for image in image_data:
                # Construct the full image URL for original quality
                image_url = f"{base_url}/data/{data['chapter']['hash']}/{image}"
                image_urls.append(image_url)
        
        # Pass the list of image URLs to the template for rendering
        return render_template("base_chapter.html", images=image_urls)
    
    else:
        # Handle the case where the API request fails
        return f"Error: Could not fetch chapter data (Status Code: {response.status_code})", 500


@views.route('/chapter',methods=['GET', 'POST'])
def chapter():
    return render_template("base_chapter.html")






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