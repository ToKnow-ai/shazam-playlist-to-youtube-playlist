"""Shazam Playlist to Youtube Playlist"""

from pathlib import Path
import random
from typing import Optional
import logging
import pandas as pd
from pytube import Search, YouTube
from flask import Flask, request, send_from_directory
from sklearn.utils import shuffle as sklearn_shuffle

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
        return parse_csv_util(pd.read_csv(csv_path, header=1), True)
    except Exception as e:
        return str(e)

def get_youtube_song(title: str, artist: str) -> Optional[YouTube]:
    """Searches for a YouTube video based on the given title and artist"""
    search_result = Search(f'{title} by {artist}')
    return search_result.results[0] if search_result.results else None

def parse_csv_util(df: pd.DataFrame, shuffle = False):
    try:
        df = df.drop_duplicates(subset=['TrackKey'])[['Title', 'Artist']]
        if shuffle:
            for random_state in random.sample(range(444, 44444), 3):
                df = sklearn_shuffle(df, random_state=random_state).reset_index(drop=True)
        return df.to_json(orient="records")
    except Exception as e:
        return str(e)