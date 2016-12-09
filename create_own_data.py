#!/usr/bin/python
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import scipy

from config import *
from apiclient.discovery import build
from apiclient.errors import HttpError
from scipy import stats



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
    search_r = youtube.videos().list(id=video_ids, part="id, statistics, snippet").execute()
    if search_r['items'][0]['snippet']['categoryId'] == '10':
        result = search_r['items'][0]['statistics']
        return (True, (search_r.get('items', [])[0]['snippet']['title']), result)
    else:
        return (False, None, None)

def get_related_video(video_id, listOfIds):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)


    search_response = youtube.search().list(
        relatedToVideoId=video_id,
        part="id",
        type="video",
        maxResults=20,
        relevanceLanguage='nl'
    ).execute()
    result = {}
    possibleIds = []
    for i in range(0,20):
        id = result['id'] = search_response.get('items',[])[i]['id']['videoId']
        if id not in listOfIds:
            (is_music, name, statistics) = get_statistics(id)
            if (is_music):
                result['name'] = name
                print(name)
                result['statistics'] = statistics
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
    result['statistics'] = get_statistics(result['id'])[2]
    result_list.append(result)
    prev = result['id']
    for i in range(1,limit):
        print(i)
        listOfIds.append(prev)
        result = get_related_video(prev, listOfIds)
        if result is None:
            break
        result_list.append(result)
        prev = result['id']
    res = {'data':result_list}
    with open("data/"+ 'own_data.json', 'w') as outfile:
        json.dump(res, outfile)

    power_law_youtube(song_name)


def power_law_youtube(song_name, log_log=False):
    json_data1 = open("data/own_data.json").read()
    songs = json.loads(json_data1)['data']
    result = []
    print(len(songs))
    for song in songs:
        result.append(int(song['statistics']['viewCount']))

    new_result = []
    for item in result:
        x = item
        y = 0
        for i in result:
            if i >= x:
                y += 1
        if(log_log):
            new_result.append((np.log(y), np.log(x)))

        else:
            new_result.append((y, x))

    if(log_log):
        plt.xlabel("log(ranking of songs)")
        plt.ylabel("log(views )")
    else:
        plt.xlabel("ranking of songs")
        plt.ylabel("views")
    plt.scatter(*zip(*new_result))
    plt.title('Result for query: '+ song_name + " N = 1000")
    # plt.show()
    plt.savefig("figures/own_data/" + "own_data"+ str(".png"))
    plt.close()


def calculate_percentual_difference(set1, set2):
    json_data1 = open("data/own_data_"+set1+".json").read()
    json_data2 = open("data/own_data_"+set2+".json").read()
    songs1 = json.loads(json_data1)['data']
    songs2 = json.loads(json_data2)['data']
    idset1 = set()
    idset2 = set()
    for i in range(0, len(songs1)):
        idset1.add(songs1[i]['id'])
        idset2.add(songs2[i]['id'])
    return (1.0-(len(idset1&idset2)/len(idset1)))*100

def calculate_shapiro_wilk():
    print('Testing dataset if it is normal distributed')
    json_data1 = open("data/own_data.json").read()
    songs = json.loads(json_data1)['data']
    result = []
    for song in songs:
        result.append(int(song['statistics']['viewCount']))
    W, p = scipy.stats.shapiro(result)
    print("W: " + str(W))
    print("p: " + str(p))
    print('N: ' + str(len(songs)))
    print('p < 0.05? ' + str(p<.05))
    print('Dataset normally distributed? ' + str(p>.05))

try:
    query = "acdc thunderstruck"
    # get_video_list(query, [], 1000)
    # if data already available, run this function:
    # power_law_youtube(query)
    power_law_youtube(query, log_log=True)
    # print(calculate_percentual_difference('hotline_100', 'rood_100'))
    # calculate_shapiro_wilk()
except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))