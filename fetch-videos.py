import requests
import csv
import os
import html
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNELS = [
    {'channel_id': 'UCJgre6She3TQCVEXxk6kc8Q', 'language': 'Polish'},
    {'channel_id': 'UCoQSVlV8NfSm1IFK4hNAB9A', 'language': 'Polish'},
    {'channel_id': 'UC08Pyl-LVr2aKiREeY6zh-w', 'language': 'Polish'},
]
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
CSV_FILE = 'videos.csv'

def fetch_videos(channel_id):
    videos = []
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 50,
        'type': 'video',
        'key': YOUTUBE_API_KEY
    }

    while True:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if 'items' in data:
            videos.extend(data['items'])
        
        # Check if there is a nextPageToken to continue fetching
        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
        else:
            break

    return videos

def load_existing_video_ids():
    if not os.path.exists(CSV_FILE):
        return set()  # Return an empty set if the file doesn't exist
    
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row['video_id'] for row in reader}  # Set of existing video IDs

def save_videos_to_csv(videos, channel_id, language):
    existing_video_ids = load_existing_video_ids()

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.path.getsize(CSV_FILE) == 0:
            writer.writerow(['video_id', 'channel_id', 'language', 'title', 'channel_title', 'upload_date'])  # Write headers if file is empty

        for video in videos:
            video_id = video['id']['videoId']
            if video_id not in existing_video_ids:
                # Decode HTML entities in the video title and channel title
                decoded_title = html.unescape(video['snippet']['title'])
                decoded_channel_title = html.unescape(video['snippet']['channelTitle'])
                
                # Format the publishedAt date
                upload_date = datetime.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").strftime('%B %d, %Y')
                
                writer.writerow([
                    video_id, 
                    channel_id, 
                    language, 
                    decoded_title,
                    decoded_channel_title,  
                    upload_date
                ])
                existing_video_ids.add(video_id)  # Update the set to include this new video ID

def main():
    for channel in CHANNELS:
        channel_id = channel['channel_id']
        language = channel['language']
        videos = fetch_videos(channel_id)
        if videos:
            save_videos_to_csv(videos, channel_id, language)
            print(f"Saved {len(videos)} videos from channel {channel_id} in {language} to CSV.")

if __name__ == '__main__':
    main()
