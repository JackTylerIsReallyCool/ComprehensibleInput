# I will update the provided script to use the YouTube API's uploads playlist approach instead of the search endpoint.
# This change will ensure that videos are fetched in chronological order (most recent first) and reduce unnecessary API calls.

import requests
import csv
import os
import html
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

YOUTUBE_API_KEYS = os.getenv('YOUTUBE_API_KEYS').split(',')
api_key_index = 0
CHANNELS_CSV = "channels.csv"
VIDEOS_CSV = 'videos.csv'

# Load channel data from CSV
channels = []
with open(CHANNELS_CSV, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        channels.append(row)

# Get the uploads playlist ID for a channel
def get_uploads_playlist_id(channel_id):
    global api_key_index
    while True:
        api_key = YOUTUBE_API_KEYS[api_key_index]
        url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}"
        response = requests.get(url).json()
        if 'error' in response:
            print(f"Error fetching uploads playlist for channel {channel_id}: {response['error']['message']}")
            if len(YOUTUBE_API_KEYS) > api_key_index + 1:
                api_key_index += 1
                continue
            return None
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Fetch videos from the uploads playlist since the specified date
def fetch_videos_from_playlist(playlist_id, latest_date):
    global api_key_index
    videos = []
    params = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'maxResults': 50,
    }

    while True:
        params['key'] = YOUTUBE_API_KEYS[api_key_index]
        response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params=params)
        data = response.json()

        if 'error' in data:
            print("API Quota reached or other error:", data['error']['message'])
            if len(YOUTUBE_API_KEYS) > api_key_index + 1:
                api_key_index += 1
                continue
            break

        if 'items' in data:
            for item in data['items']:
                video_id = item['snippet']['resourceId']['videoId']
                published_at = item['snippet']['publishedAt']
                published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

                # Stop fetching if we encounter a video older than the latest date
                if published_date <= latest_date:
                    return videos

                videos.append(item)

        # Check for nextPageToken to continue fetching
        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
        else:
            break

    return videos

# Load the latest video dates from the existing CSV
def load_latest_video_dates():
    latest_dates = {}
    if not os.path.exists(VIDEOS_CSV):
        return latest_dates
    
    with open(VIDEOS_CSV, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            channel_id = row['channel_id']
            published_at = row['upload_date']
            published_date = datetime.strptime(published_at, "%B %d, %Y")

            if channel_id not in latest_dates or published_date > latest_dates[channel_id]:
                latest_dates[channel_id] = published_date

    return latest_dates

# Save new videos to the CSV
def save_videos_to_csv(videos, channel_id, language):
    existing_video_ids = load_existing_video_ids()

    with open(VIDEOS_CSV, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.path.getsize(VIDEOS_CSV) == 0:
            writer.writerow(['video_id', 'channel_id', 'language', 'title', 'channel_title', 'upload_date'])

        for video in videos:
            video_id = video['snippet']['resourceId']['videoId']
            if video_id not in existing_video_ids:
                decoded_title = html.unescape(video['snippet']['title'])
                decoded_channel_title = html.unescape(video['snippet']['channelTitle'])
                upload_date = datetime.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").strftime('%B %d, %Y')

                writer.writerow([
                    video_id,
                    channel_id,
                    language,
                    decoded_title,
                    decoded_channel_title,
                    upload_date
                ])
                existing_video_ids.add(video_id)

# Load existing video IDs to avoid duplicates
def load_existing_video_ids():
    if not os.path.exists(VIDEOS_CSV):
        return set()
    
    with open(VIDEOS_CSV, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row['video_id'] for row in reader}

# Main function
def main():
    latest_dates = load_latest_video_dates()

    for channel in channels:
        channel_id = channel['channel_id']
        language = channel['language']
        latest_date = latest_dates.get(channel_id, datetime.min)

        print(f"Fetching uploads playlist for channel {channel_id}...")
        uploads_playlist_id = get_uploads_playlist_id(channel_id)

        if not uploads_playlist_id:
            print(f"Failed to get uploads playlist for channel {channel_id}. Skipping.")
            continue

        print(f"Fetching videos from uploads playlist since {latest_date.strftime('%B %d, %Y')}...")
        new_videos = fetch_videos_from_playlist(uploads_playlist_id, latest_date)

        if new_videos:
            print(f"Found {len(new_videos)} new videos for channel {channel_id}.")
            save_videos_to_csv(new_videos, channel_id, language)
        else:
            print(f"No new videos found for channel {channel_id}.")

if __name__ == '__main__':
    main()

