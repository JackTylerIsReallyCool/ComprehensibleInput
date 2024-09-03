from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_videos():
    videos = []
    with open('videos.csv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            videos.append(row)
    return videos

@app.route('/')
def homepage():
    videos = load_videos()
    languages = sorted({video['language'] for video in videos})
    return render_template('homepage.html', languages=languages)

@app.route('/browse/<language>')
def browse(language):
    videos = load_videos()
    filtered_videos = [video for video in videos if video['language'] == language]
    return render_template('browse.html', language=language, videos=filtered_videos)

@app.route('/video/<video_id>')
def video_page(video_id):
    return render_template('video.html', video_id=video_id)

if __name__ == '__main__':
    app.run(debug=True)