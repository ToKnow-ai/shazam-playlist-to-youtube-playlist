from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        return 'Hello, World!'
    except Exception as e:
        return str(e)

@app.route('/video_id', methods=['POST'])
def get_video_id():
    try:
        title = request.json.get('title')
        artist = request.json.get('artist')
        return { 'artist': artist, 'title': title }
    except Exception as e:
        return str(e)