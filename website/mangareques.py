import requests
from .models import Chapters
import os
from flask import Blueprint,jsonify,Response
from . import db

scraping = Blueprint('scraping', __name__)

@scraping.route('/manga/chapter/<chapter_id>')
def chapter_request(chapter_id):
    # API configuration
    base_url = "https://api.mangadex.org"
    languages = ["en"]
    manga_id = "c52b2ce3-7f95-469c-96b0-479524fb7a1a"  # Consider making this configurable
    
    try:
        # Validate chapter_id exists in the manga
        manga_chapters = requests.get(
            f"{base_url}/manga/{manga_id}/feed",
            params={"translatedLanguage[]": languages},
        )
        
        if not manga_chapters.ok:
            return jsonify({"error": f"Failed to fetch chapters: {manga_chapters.status_code}"}), manga_chapters.status_code
        
        chapter_ids = [chapter['id'] for chapter in manga_chapters.json()['data']]
        
        # Check if requested chapter exists
        if chapter_id not in chapter_ids:
            return jsonify({"error": "Chapter not found"}), 404
        
        # Get chapter details
        chapter_server = requests.get(f"{base_url}/at-home/server/{chapter_id}")
        
        if not chapter_server.ok:
            return jsonify({"error": f"Failed to fetch chapter server: {chapter_server.status_code}"}), chapter_server.status_code
        
        # Get chapter information
        info_request = requests.get(f"{base_url}/chapter/{chapter_id}")
        
        if not info_request.ok:
            return jsonify({"error": f"Failed to fetch chapter info: {info_request.status_code}"}), info_request.status_code
        
        info_json = info_request.json()
        num_chapter = info_json["data"]["attributes"]["chapter"]
        chapter_title = info_json["data"]["attributes"]["title"]
        
        # Get manga title
        manga_info = requests.get(f"{base_url}/manga/{manga_id}")
        
        if not manga_info.ok:
            return jsonify({"error": f"Failed to fetch manga info: {manga_info.status_code}"}), manga_info.status_code
        
        manga_json = manga_info.json()
        manga_title = manga_json["data"]["attributes"]["title"]["en"]
        
        # Extract image data
        chapter_data = chapter_server.json()
        host = chapter_data["baseUrl"]
        chapter_hash = chapter_data["chapter"]["hash"]
        data = chapter_data["chapter"]["data"]
        
        # Store chapter in database
        new_chapter = Chapters(
            title=chapter_title,
            chapter_number=num_chapter,
            manga_title=manga_title
        )
        
        try:
            db.session.add(new_chapter)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # Log the error, but continue since we can still serve the image
            print(f"Database error: {str(e)}")
        
        # For now, just serve the first page
        # Consider adding a parameter to specify which page to serve
        page = data[0]
        image_data = requests.get(f"{host}/data/{chapter_hash}/{page}")
        
        if not image_data.ok:
            return jsonify({"error": "Failed to fetch image"}), image_data.status_code
        
        return Response(image_data.content, mimetype='image/jpeg')
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



