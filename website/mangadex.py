creds = {
    "username": "testuser",
    "password": "testpass",
}
import requests
from datetime import datetime

base_url = "https://api.mangadex.org"

r = requests.post(
    f"{base_url}/auth/login", 
    json=creds
)
r_json = r.json()

session_token = r_json["token"]["session"]
expires = datetime.now().timestamp() + 15 * 60000
refresh_token = r_json["token"]["refresh"]

print(session_token, expires, refresh_token)

