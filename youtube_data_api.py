#!/usr/bin/python
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
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


def get_statistics(video_ids):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_r = youtube.videos().list(id=video_ids, part="statistics, snippet").execute()
    result = search_r.get('items', [])
    return result[0]['statistics']

def is_music_video(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_r = youtube.videos().list(id=video_id, part="id, snippet" ).execute()
    if search_r['items'][0]['snippet']['categoryId'] == '10':
        return (True, search_r.get('items', [])[0]['snippet']['title'])
    else:
        return (False, "")

def get_related_video(video_id, listOfIds):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)


    search_response = youtube.search().list(
        relatedToVideoId=video_id,
        part="id",
        type="video",
        maxResults=20
    ).execute()
    result = {}
    possibleIds = []
    for i in range(0,20):
        id = result['id'] = search_response.get('items',[])[i]['id']['videoId']
        if id not in listOfIds:
            (a,b) = is_music_video(id)
            if (a):
                result['name'] = b
                print(b)
                result['statistics'] = get_statistics(result['id'])

                return result
    return None
def get_video_list(song_name, listOfIds, limit = 100):
    result_list = []
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=song_name,
        part="id,snippet",
        maxResults=1,

    ).execute()
    result = {}
    result['name'] = search_response.get('items', [])[0]['snippet']['title']
    result['id'] = search_response.get('items', [])[0]['id']['videoId']
    result['statistics'] = get_statistics(result['id'])
    result_list.append(result)
    prev = result['id']
    for i in range(1,limit):
        listOfIds.append(prev)
        result = get_related_video(prev, listOfIds)

        result_list.append(result)
        prev = result['id']
    res = {'data':result_list}
    with open("data/"   + 'own_data.json', 'w') as outfile:
        json.dump(res, outfile)




def power_law_youtube():
    json_data1 = open("data/own_data.json").read()
    songs = json.loads(json_data1)['data']
    day = None
    result = []
    for song in songs:
        result.append(int(song['statistics']['viewCount']))

    new_result = []
    for item in result:
        x = item
        y = 0
        for i in result:
            if i >= x:
                y += 1
        new_result.append((np.log(x), np.log(y)))
    plt.scatter(*zip(*new_result))
    plt.title('HAHA HITLER')
    plt.ylabel("log(number of songs)")
    plt.xlabel("log(views)")
    plt.show()



if __name__ == "__main__":
  # argparser.add_argument("--q", help="Search term", default="")
  # argparser.add_argument("--max-results", help="Max results", default=5)
  # args = argparser.parse_args()
  # print(args)
  try:
      # print(is_music_video('X5Cfi7U4eL4'))
    get_video_list("deetox alone", [])
    power_law_youtube()
    # is_music_video('OQcne0OxUnA')
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))