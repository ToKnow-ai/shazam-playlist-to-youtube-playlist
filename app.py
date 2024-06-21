"""Shazam Playlist to Youtube Playlist"""

from typing import Optional
import pandas as pd
from pytube import Search, YouTube
from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return str(e)
    
@app.route('/video_id', methods=['POST'])
def video_id() -> str:
    try:
        title: str = request.json.get('title')
        artist: str = request.json.get('artist')
        youtube: YouTube = _get_youtube_song(title, artist)
        return youtube.video_id
    except Exception as e:
        return str(e)

@app.route('/parse_csv', methods=['POST'])
def parse_csv():
    try:
        file = request.files['file']
        # Process the uploaded file
        shazamlibrary_df = pd.read_csv(file, header=1)
        shazamlibrary_df = shazamlibrary_df.drop_duplicates(subset=['TrackKey'])[['Title', 'Artist']]
        return shazamlibrary_df.to_json(orient="records")
    except Exception as e:
        return str(e)
    

def _get_youtube_song(title: str, artist: str) -> Optional[YouTube]:
    search_result = Search(f'{title} by {artist}')
    return search_result.results[0] if search_result.results else None