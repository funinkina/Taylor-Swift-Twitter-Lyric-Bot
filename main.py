from bs4 import BeautifulSoup as bs
import requests
import random
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

artist_link = 'https://www.azlyrics.com/t/taylorswift.html'

song_list = requests.get(artist_link)
if song_list.status_code != 200:
    print(f"Error: {song_list.status_code}")
    exit()

soup = bs(song_list.text, 'lxml')
songs = soup.find_all('div', class_='listalbum-item')
song_list = []
for song in songs:
    link = song.find('a')['href']
    song_list.append(link)

lyric_link = "https://azlyrics.com"+random.choice(song_list)
lyric_page = requests.get(lyric_link)
soup = bs(lyric_page.text, 'lxml')

title = soup.find('title').text.removesuffix(" Lyrics | AZLyrics.com").removeprefix("Taylor Swift ")  # noqa: E501
body = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
lyrics = body.find_all('div')[5].text.split("\n\n")

para = random.choice(lyrics).strip().split("\n")
line = [para[i] + '\n' + para[i + 1] if i + 1 < len(para) else para[i] for i in range(0, len(para), 2)]  # noqa: E501

text = random.choice(line) + "\n\t" + title
print(text)

client = tweepy.Client(
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
)

response = client.create_tweet(
    text=text
)

print(f"https://twitter.com/user/status/{response.data['id']}")
