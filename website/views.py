from flask import Blueprint, render_template,flash,Response,request
from .models import User,Chapters
import os,requests
from . import db

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
def display_manga():

    jujutsu_kaisen = "c52b2ce3-7f95-469c-96b0-479524fb7a1a"
    solo_levelling = "32d76d19-8a05-4db0-9fc2-e0b0648fe9d0"
    one_piece = "a1c7c817-4e59-43b7-9365-09675a149a6f"

    jk_cover_url = f"/manga-cover/{jujutsu_kaisen}"
    sl_cover_url = f"/manga-cover/{solo_levelling}"
    op_cover_url = f"/manga-cover/{one_piece}"
    


    return render_template('home.html',
                           jk = jujutsu_kaisen,
                           sl = solo_levelling,
                           op = one_piece,
                           jk_cover = jk_cover_url,
                           sl_cover = sl_cover_url,
                           op_cover = op_cover_url)

@views.route('/manga-cover/<manga_id>')
def manga_cover_proxy(manga_id):
    """
    Proxy function to fetch and serve manga covers directly from MangaDex
    """
    try:
        # Step 1: Get manga details to find cover art relationship
        manga_response = requests.get(
            f"https://api.mangadex.org/manga/{manga_id}?includes[]=cover_art"
        )
        
        if manga_response.status_code != 200:
            return Response("Failed to retrieve manga details", status=manga_response.status_code)
        
        manga_data = manga_response.json()
        
        # Step 2: Extract cover art ID and filename
        cover_filename = None
        for relationship in manga_data["data"]["relationships"]:
            if relationship["type"] == "cover_art" and "attributes" in relationship:
                cover_filename = relationship["attributes"].get("fileName")
                break
                
        # If we couldn't find filename directly (older API versions), make another request
        if not cover_filename and relationship["type"] == "cover_art":
            cover_id = relationship["id"]
            cover_response = requests.get(f"https://api.mangadex.org/cover/{cover_id}")
            if cover_response.status_code == 200:
                cover_data = cover_response.json()
                cover_filename = cover_data["data"]["attributes"]["fileName"]
        
        if not cover_filename:
            return Response("Cover not found", status=404)
            
        # Step 3: Fetch the actual image
        image_url = f"https://uploads.mangadex.org/covers/{manga_id}/{cover_filename}"
        image_response = requests.get(image_url, stream=True)
        
        if image_response.status_code != 200:
            return Response("Failed to retrieve cover image", status=image_response.status_code)
            
        # Step 4: Stream the image back to the client with proper headers
        return Response(
            image_response.raw.read(),
            content_type=image_response.headers['content-type'],
            headers={
                'Cache-Control': 'public, max-age=86400',  # Cache for 1 day
            }
        )
        
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

@views.route('/manga',methods=['GET','POST'])
def manga_details():
    return render_template("base_manga.html")

@views.route('/manga/<manga_id>',methods=['GET', 'POST'])
def jujutsu_kaisen(manga_id):

    base_url = "https://api.mangadex.org"

    cover =f"/manga-cover/{manga_id}"


    try:
        manga_response = requests.get(
            f"{base_url}/manga/{manga_id}",
            params={"translatedLanguage[]" : ["en"]}
        )

        manga_json = manga_response.json()

        title = manga_json['data']['attributes']['title']['en']
        description = manga_json['data']['attributes']['description']['en']
    except Exception as e:
        raise e
    
    try:
        # Fetch chapters for the manga
        response = requests.get(
            f"{base_url}/manga/{manga_id}/feed",
            params={"translatedLanguage[]": ["en"]}
        )
        
        if not response.ok:
            return render_template("error.html", error=f"API error: {response.status_code}"), response.status_code
        
        chapters_json = response.json()

        chapters = []
        
        for chapter_data in chapters_json['data']:
            chapter_id = chapter_data['id']
            chapter_num = chapter_data['attributes']['chapter']
            chapter_title = chapter_data['attributes']['title']

            data = {
                "id" : chapter_id,
                "chapter_num" : chapter_num,
                "chapter_title" : chapter_title
            }

            chapters.append(data)
        
        return render_template("manga.html", data=chapters,title = title,description = description,cover = cover)
    
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
        r_json = response.json()

        host = r_json["baseUrl"]
        chapter_hash = r_json["chapter"]["hash"]
        data = r_json["chapter"]["data"]
        data_saver = r_json["chapter"]["dataSaver"]

        images =[f"/manga/proxy-image/{chapter_hash}/{image}" for image in data] 

        #images = [response.url for response in images]
        
        # Pass the list of image URLs to the template for rendering
        return render_template("base_chapter.html", images=images)
    
    else:
        # Handle the case where the API request fails
        return f"Error: Could not fetch chapter data (Status Code: {response.status_code})", 500

# Creates a proxy route to display from the api to website
@views.route('/manga/proxy-image/<chapter_hash>/<path:image_filename>')
def proxy_manga_image(chapter_hash, image_filename):
    # Create the original image URL based on MangaDex API structure
    # You might want to cache the baseUrl as it could be the same for multiple images
    api_url = "https://api.mangadex.org/at-home/server"
    
    # Optional: You can choose between data and dataSaver with a query parameter
    use_data_saver = request.args.get('data_saver', 'false').lower() == 'true'
    
    # Determine which MangaDex endpoint to use based on data_saver preference
    endpoint = "data-saver" if use_data_saver else "data"
    
    # Construct the full image URL
    image_url = f"https://uploads.mangadex.org/{endpoint}/{chapter_hash}/{image_filename}"
    
    try:
        # Make the request to the original image
        response = requests.get(
            image_url,
            stream=True  # Important for larger files
        )
        
        # Return the image with correct content type
        return Response(
            response.iter_content(chunk_size=10*1024),
            content_type=response.headers.get('Content-Type', 'image/jpeg'),
            status=response.status_code
        )
    except Exception as e:
        return f"Error fetching image: {str(e)}", 500

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
