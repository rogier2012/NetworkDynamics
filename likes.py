#!/usr/bin/python
import json

from config import *
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = GOOGLE_API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
file = "20151109_1800_data"

def get_song_names(dataset):
    result = []
    with open('data/spotify_top100/'+dataset+'.json') as data_file:
        data = json.load(data_file)
    for entry in data['tracks']['items']:
        result.append(entry['track']['name'])
    return result


def get_likes(songname):
    with open('data/youtube_top100/'+file+'.json') as data_file:
        data = json.load(data_file)
    for entry in data:
        if songname in (entry['snippet']['title']):
            return (entry['statistics']['likeCount'], entry['statistics']['dislikeCount'])

def get_likes_dataset(filename):
    songs =  get_song_names(filename)
    res = dict()
    for song in songs:
        if get_likes(song) is not None:
            res[song] = get_likes(song)
    print(len(res))
    return res


print((get_likes_dataset(file)))

