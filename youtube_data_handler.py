import os
import json
import datetime
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

def difference_likes_dislikes():
    result = {}
    json_data1 = open("data/spotify_top100/20151109_1800_data.json").read()
    spotify_data = json.loads(json_data1)
    spotify_tracks = spotify_data.get("tracks").get("items", [])
    del spotify_tracks[29]
    del spotify_tracks[45]
    json_data2 = open("data/youtube_top100/20151109_1800_data.json").read()
    youtube_data_begin = json.loads(json_data2)
    del youtube_data_begin[29]
    del youtube_data_begin[45]
    json_data2 = open("data/youtube_top100/20161126_1800_data.json").read()
    youtube_data_end = json.loads(json_data2)

    for track in spotify_tracks:
        track_name = track.get("track", {}).get("name", "")
        # if (spotify_tracks.index(track)< 98):
        statistics = youtube_data_begin[spotify_tracks.index(track)].get("statistics", {})
        blikes = int(statistics.get("likeCount"))
        bdislikes = int(statistics.get("dislikeCount"))
        d1 = blikes+bdislikes
        statistics = youtube_data_end[spotify_tracks.index(track)].get("statistics", {})
        elikes = int(statistics.get("likeCount",0))
        edislikes = int(statistics.get("dislikeCount",0))
        d2 = blikes+bdislikes
            # print(spotify_tracks.index(track))
            # print(youtube_data_begin[spotify_tracks.index(track)].get("snippet").get("title"))
            # print(youtube_data_end[spotify_tracks.index(track)].get("snippet").get("title"))

        result[track_name] = {"index": spotify_tracks.index(track),
                              "likes": [],
                              "d1"   : d1 ,
                              "d2"   : d2
                            }


    counter = 0
    for filename in os.listdir("data/youtube_top100"):
        if (filename.endswith(".json") and counter > 60):

            json_data = open("data/youtube_top100/" + filename).read()
            youtube_data = json.loads(json_data)
            for video in youtube_data:

                statistics = video.get("statistics", {})
                likes = int(statistics.get("likeCount"))
                dislikes = int(statistics.get("dislikeCount"))
                for k,v in result.items():
                    if v.get("index",-1) == youtube_data.index(video):
                        v.get("likes").append(likes-dislikes)
        counter += 1


    return result




def plot_hotline_bling():
    likes_per_day = {}
    # likes_per_day = get_likes_dislikes_hotline_bling()
    data = dict()
    for k,v in likes_per_day.items():
        total = v[0] + v[1]
        diff = v[0] - v[1]
        data[total] = diff
    plt.scatter(data.keys(),data.values())
    plt.title("Hotline Bling")
    plt.show()

# plt.plot(data[1].get("likes"))
# plt.title(data[0])
# plt.show()




def get_likes_dislikes_hotline_bling():
    result = dict()
    for file in os.listdir("data/youtube_top100/"):
        json_data1 = open("data/youtube_top100/" + file).read()
        youtube = json.loads(json_data1)
        entry = youtube[2]
        if entry['snippet']['title'] == "Drake - Hotline Bling":
            result[(file.replace("_1800_data.json", ""))] = ((entry['statistics']['likeCount']), (entry['statistics']['dislikeCount']))
    return result


print(len(get_likes_dislikes_hotline_bling()))