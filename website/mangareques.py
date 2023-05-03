import requests
from .models import Chapters
import os
from flask import Blueprint
from . import db

scraping = Blueprint('scraping',__name__)


def chapter_request():
    #variables of API request
    manga_id = "c52b2ce3-7f95-469c-96b0-479524fb7a1a"
    languages = ["en"]
    base_url = "https://api.mangadex.org"

    #send API request for the list of chapters of the manga
    r = requests.get(
        f"{base_url}/manga/{manga_id}/feed",
        params={"translatedLanguage[]": languages},
    )

    #extract all IDs of the chapters
    chapter_id=(list(chapter['id'] for chapter in r.json()['data']))

    #specific ID for testing
    id = 'c69b7ace-4fc5-46a9-bfb4-6d72b11dd390'

    # API request for chapter details
    r = requests.get(f"{base_url}/at-home/server/{id}")

    #error handling
    if r.status_code == 404:
                    print("error 404")
    elif not r.ok:
                print( requests.HTTPError(f"Error response returned. {r.status_code} {base_url}: {r.reason}"))
    else:
                    # chapter information extraction
                    info_request = requests.get(f"{base_url}/chapter/{id}")
                    info_json = info_request.json()
                    num_chapter = info_json["data"]["attributes"]["chapter"]
                    chapter_title = info_json["data"]["attributes"]["title"]
                    #information to extract the images in chapter
                    r_json = r.json()
                    host = r_json["baseUrl"]
                    chapter_hash = r_json["chapter"]["hash"]
                    data = r_json["chapter"]["data"]
                    data_saver = r_json["chapter"]["dataSaver"]

    #request to link chapter name with pages        
    manga_title = requests.get(f"{base_url}/manga/c52b2ce3-7f95-469c-96b0-479524fb7a1a")
    manga_json = manga_title.json()
    manga_t = manga_json["data"]["attributes"]["title"]["en"]

    #storing pages into folder
    folder_path = f"Mangadex/{chapter_title}"
    os.makedirs(folder_path, exist_ok=True)

    for page in data:
        r = requests.get(f"{host}/data/{chapter_hash}/{page}")

        with open(f"{folder_path}/{page}", mode="wb") as f:
            f.write(r.content)
    # storing details into database
    new_chapter = Chapters( title = chapter_title, chapter_number = num_chapter , manga_title = manga_t )
    print(f"Downloaded {len(data)} pages.")       

    db.session.add(new_chapter)
    # makes sure a duplicate does not happen
    try:
            db.session.commit()
    except:
        db.session.rollback()



