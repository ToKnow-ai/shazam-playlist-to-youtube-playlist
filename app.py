from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/video_id/<video_id>')
def get_video_id(video_id):
    return f'video_id = {video_id}!'