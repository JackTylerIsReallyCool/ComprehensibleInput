import requests
import csv
import os
import html
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNELS = [
    {'channel_id': 'UC3VyG75zgWvLkK3mL77Yz3g', 'language': 'English'},
    {'channel_id': 'UCSW8FB6e8tUGEaDsoe7SlWw', 'language': 'English'},
    {'channel_id': 'UC0QAymHwRmS84Crn8Bgt0tQ', 'language': 'English'},
    {'channel_id': 'UCouyFdE9-Lrjo3M_2idKq1A', 'language': 'Spanish'},
    {'channel_id': 'UCfG2VhlQgy5bHGmkpeKcjVA', 'language': 'Spanish'},
    {'channel_id': 'UCoHJ7PkM6T92LwgJgrnDhWA', 'language': 'Spanish'},
    {'channel_id': 'UC6Xtu6v_op552SsOr5_jWrg', 'language': 'Japanese'},
    {'channel_id': 'UCMNVKIaw8hV8ln3dDE5z-hA', 'language': 'Japanese'},
    {'channel_id': 'UCsQCbl3a9FtYvA55BxdzYiQ', 'language': 'Japanese'},
    {'channel_id': 'UCXo8kuCtqLjL1EH6m4FJJNA', 'language': 'Japanese'},
    {'channel_id': 'UCjSFDgRCzh_1ZPhxChVgK7Q', 'language': 'Chinese'},
    {'channel_id': 'UCcvTOgUiplI80SPR73ogCEQ', 'language': 'Chinese'},
    {'channel_id': 'UCxqLWT3swHvP9_4bv7Qssxw', 'language': 'Chinese'},
    {'channel_id': 'UCCD-nJGAxKmh1GnSuUx8Gig', 'language': 'French'},
    {'channel_id': 'UC-XUpEBvcQcRqMdtLhoXmOA', 'language': 'French'},
    {'channel_id': 'UCbC9Utt1c6UXRqWw2lOTCBg', 'language': 'French'},
    {'channel_id': 'UCDqH89_8ThHUWatP2sLC1Qw', 'language': 'Portuguese'},
    {'channel_id': 'UC_8_OHEb2-Xn8k00NVqnzlg', 'language': 'Portuguese'},
    {'channel_id': 'UClOb0MwFKLrj1g9BvDPenig', 'language': 'Portuguese'},
    {'channel_id': 'UC4Quzpomix0zB3CeKZtceuQ', 'language': 'Dutch'},
    {'channel_id': 'UChyx8ibmFMTTe3aS_l_eaKA', 'language': 'German'},
    {'channel_id': 'UC2xMra98Bvpcq9kNnnWC2xw', 'language': 'German'},
    {'channel_id': 'UCsYGAmiWIvOjvT9f1sgQXRw', 'language': 'German'},
    {'channel_id': 'UCwKGRXeMl_hsZnlOrTyZ9lQ', 'language': 'German'},
    {'channel_id': 'UCGJ9gQg6AKfjRmxTVS-8nzw', 'language': 'German'},
    {'channel_id': 'UCWBek-qVDuFNsvFbRClPjrA', 'language': 'Thai'},
    {'channel_id': 'UCjx6BYaOnbbfbIdsE3BEqWw', 'language': 'Thai'},
    {'channel_id': 'UC2IdTAO0WwpIHt8OupH_18Q', 'language': 'Thai'},
    {'channel_id': 'UCrMi6Eyw6G7j2XC7TBEW1gw', 'language': 'Thai'},
    {'channel_id': 'UCjEpP8NpiAtTwhQl-iO7fWw', 'language': 'Italian'},
    {'channel_id': 'UCC2E_oDRXJT9ZeGpnwVxk6A', 'language': 'Italian'},
    {'channel_id': 'UCegEedDeryCYSVT7eBCm-RQ', 'language': 'Italian'},
    {'channel_id': 'UCDNbk-uX4D6nsthi8L03fng', 'language': 'Russian'},
    {'channel_id': 'UCcZfmnPdD6ZgzzuD3fm6WIQ', 'language': 'Russian'},
    {'channel_id': 'UCstP8x5cV3_fMvVFT_aQ-nA', 'language': 'Russian'},
    {'channel_id': 'UCldG3IoWKLAt3ZUCNTGSL9w', 'language': 'Russian'},
    {'channel_id': 'UCIbkDDk1BCPvh0rnL98jDIw', 'language': 'Russian'},
    {'channel_id': 'UCIbkDDk1BCPvh0rnL98jDIw', 'language': 'Russian'},
    {'channel_id': 'UC737T1zTN6MQ1uWorHVAXvA', 'language': 'Korean'},
    {'channel_id': 'UCxwSrFHHC3I9xFxrChfuqwA', 'language': 'Korean'},
    {'channel_id': 'UC-3wHyVaLCiujjjPYXtif5w', 'language': 'Korean'},
    {'channel_id': 'UC5ixjApuU6oJHS540E_SSSw', 'language': 'Korean'},
    {'channel_id': 'UCQdEQ6KW8fpwuVSdtalXupg', 'language': 'Arabic'},
    {'channel_id': 'UC8mUu9ygbDMDj5P6297H_dA', 'language': 'Arabic'},
    {'channel_id': 'UCX-XgyB8SQurLqXiT3b3wNg', 'language': 'Arabic'},
    {'channel_id': 'UCkwOyylAOUEwfvYPnps6yzg', 'language': 'Arabic'},
    {'channel_id': 'UCVt9SQjiL-R1GuH-5Uieovw', 'language': 'Hindi'},
    {'channel_id': 'UCNmGEGBqjDAkybQPVO0NZkg', 'language': 'Punjabi'},
    {'channel_id': 'UC87kNP67aPeGk3QqRSWuZnw', 'language': 'Indonesian'},
    {'channel_id': 'UCNtU6lkGwuoNHJB_FMZjK5w', 'language': 'Welsh'},
    {'channel_id': 'UCONrz2yl94NVTzy8ZQq7znQ', 'language': 'Tagalog'},
    {'channel_id': 'UCbWJOQ7td4kgHZPw0WCXMzQ', 'language': 'Serbain'},
    {'channel_id': 'UCgwKyufKMXaB-xjA05JqGxw', 'language': 'Greek'},
    {'channel_id': 'UC29y5DkSuf4ShtT3Vsv7Gag', 'language': 'Greek'},
    {'channel_id': 'UCaOl_QBOxS7YSrNWjw06xZQ', 'language': 'Norwegian'},
    {'channel_id': 'UCxdRJ5lW2QlUNRfff-ZoE-A', 'language': 'Norwegian'},
    {'channel_id': 'UCqc2J-HDTOfVOJNox2BdkUQ', 'language': 'Swedish'},
    {'channel_id': 'UCbG0VOqIo9EqEtfE3Ru2BaQ', 'language': 'Swedish'},
    {'channel_id': 'UCoDbIqejIAS9eZgYNzE2FCg', 'language': 'Finnish'},
    {'channel_id': 'UCvvo0wV6usH_SS-6Pcz9Qnw', 'language': 'Hungarian'},
    {'channel_id': 'UCMRaqTlmQ2Qvc5ynFOg84gw', 'language': 'Hungarian'},
    {'channel_id': 'UC3U2lryw5Hksu71fMwsGT9A', 'language': 'Vietnamese'},
    {'channel_id': 'UC4di2z7dbPra5xhp6BN7XwQ', 'language': 'Vietnamese'},
    {'channel_id': 'UCQS2_zzisMq5C_FggxsQwTQ', 'language': 'Cantonese'},
    {'channel_id': 'UC9xosUh_LZUdQv-kw38RehA', 'language': 'Cantonese'},
    {'channel_id': 'UCAXD2TuTkY_Tld20lYNL15g', 'language': 'Turkish'},
    {'channel_id': 'UCeMQiXmFNTtN3OHlNJxnnUw', 'language': 'Turkish'},
    {'channel_id': 'UCQg2AzkYEueS5giD84wxLdg', 'language': 'Ukrainian'},
    {'channel_id': 'UCTJzD-YVoDGolkN7lQ4ZasQ', 'language': 'Ukrainian'},
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
