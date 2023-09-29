import os
import tweepy
import requests
import random
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('MUSIXMATCH_API_KEY')

endpoint = 'https://api.musixmatch.com/ws/1.1/track.search'


def randomgen():
    random_page = random.randint(0, 5)
    if random_page < 5:
        random_song = random.randint(0, 99)
    else:
        random_song = random.randint(0, 55)
    return [random_page, random_song]


params = {
    'f_artist_id': 259675,
    'f_has_lyrics': 1,
    'f_is_instrumental': 0,
    'apikey': api_key,
    'format': 'json',
    'page_size': 100,
    'page': randomgen()[0]
}

response = requests.get(endpoint, params=params)

if response.status_code == 200:
    data = response.json()
    # print(data['message']['header']['status_code'])
    if data['message']['header']['status_code'] == 200:
        random_song = randomgen()[1]
        track_id = data['message']['body']['track_list'][random_song]['track']['track_id']  # noqa: E501
        # print(data['message']['body']['track_list'][random_song]['track']['track_id'])  # noqa: E501
        # print(data['message']['body']['track_list'][random_song]['track']['track_name'], "\n")  # noqa: E501
        lyricsendpoint = 'https://api.musixmatch.com/ws/1.1/track.lyrics.get'  # noqa: E501
        lyricsparams = {
            'track_id': track_id,
            'apikey': api_key,
            'format': 'json',
        }
        lyrics_response = requests.get(lyricsendpoint, params=lyricsparams)  # noqa: E501
        lyrics = lyrics_response.json()
        lyrics_body = lyrics['message']['body']['lyrics']['lyrics_body']
        lyrics_list = lyrics_body.splitlines()
        lyrics_list = [string for string in lyrics_list if string != '']
        lyrics_list = lyrics_list[:-3]
        random_lyric = lyrics_list[random.randint(0, len(lyrics_list)-1)]
        print(random_lyric)
    elif data['message']['header']['status_code'] == 401:
        print("API ERROR!")
else:
    print(f"Error: {response.status_code}")


client = tweepy.Client(
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
)

response = client.create_tweet(
    text=random_lyric
)

print(f"https://twitter.com/user/status/{response.data['id']}")
