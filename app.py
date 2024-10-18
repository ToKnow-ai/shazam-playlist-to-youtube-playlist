"""Shazam Playlist to Youtube Playlist"""

from pathlib import Path
from typing import Optional
import logging
import pandas as pd
from pytube import Search, YouTube
from flask import Flask, request, send_from_directory

# https://github.com/pytube/pytube/issues/1270#issuecomment-2100372834
pytube_logger = logging.getLogger('pytube')
pytube_logger.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def index():
    """Route handler for the home page"""
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return str(e)
    
@app.route('/video_id', methods=['POST'])
def video_id() -> str:
    """Route handler for retrieving the YouTube video ID"""
    try:
        title: str = request.json.get('title')
        artist: str = request.json.get('artist')
        youtube: YouTube = get_youtube_song(title, artist)
        return youtube.video_id
    except Exception as e:
        return str(e)

@app.route('/parse_csv', methods=['POST'])
def parse_csv():
    """Route handler for parsing the uploaded CSV file"""
    try:
        file = request.files['file']
        # Process the uploaded file
        return parse_csv_util(pd.read_csv(file, header=1))
    except Exception as e:
        return str(e)

@app.route('/parse_csv_test', methods=['GET'])
def parse_csv_test():
    """Route handler for parsing the test CSV file"""
    try:
        # Construct the path to the CSV file
        csv_path = Path(__file__).parent / 'shazamlibrary.test.csv'
        return parse_csv_util(pd.read_csv(csv_path, header=1))
    except Exception as e:
        return str(e)

def get_youtube_song(title: str, artist: str) -> Optional[YouTube]:
    """Searches for a YouTube video based on the given title and artist"""
    search_result = Search(f'{title} by {artist}')
    return search_result.results[0] if search_result.results else None

def parse_csv_util(shazamlibrary_df):
    try:
        shazamlibrary_df = shazamlibrary_df.drop_duplicates(subset=['TrackKey'])[['Title', 'Artist']]
        return shazamlibrary_df.to_json(orient="records")
    except Exception as e:
        return str(e)