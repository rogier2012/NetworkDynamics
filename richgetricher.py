import os
import json
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def derivative_data(input_dict):
    result = []
    previous = 0
    for k, v in input_dict:
        result.append((k, v - previous))
        previous = v

    del result[0]

    return result


def dict_to_tuple_list(input_dict, date_conversion_needed=False):
    result = []
    for k, v in input_dict.items():
        if date_conversion_needed:
            d = datetime.strptime(k, "%Y-%m-%d")
            result.append((d, v))
        else:
            result.append((k, v))

    return sorted(result)


def power_law_youtube():
    json_data1 = open("data/intermediate_data/views_over_time.json").read()
    songs = json.loads(json_data1)
    day = None
    result = []
    for song in songs:
        result.append(dict_to_tuple_list(song, True)[0][1])
        if songs.index(song) == 0:
            day = dict_to_tuple_list(song, True)[0][0]
    print(result)
    new_result = []
    for item in result:
        x = item
        y = 0
        for i in result:
            if i >= x:
                y += 1
        new_result.append((np.log(x), np.log(y)))
    plt.scatter(*zip(*new_result))
    plt.title(day.strftime("%A %d %B %Y"))
    plt.ylabel("log(number of songs)")
    plt.xlabel("log(views)")
    plt.show()


def rank_over_time(song_name, index):
    spotify_folder = "spotify_top100"
    # song_name = "Sorry"
    spotify_ranking = []

    for filename in os.listdir("data/" + spotify_folder + "/"):
        if filename == "20160105_1800_data.json":
            break
        if filename.endswith("1800_data.json"):
            json_data1 = open("data/" + spotify_folder + "/" + str(filename)).read()
            spotify_data = json.loads(json_data1)
            tracks = spotify_data.get("tracks").get("items", [])
            year = int(filename[:4])
            month = int(filename[4:6])
            day = int(filename[6:8])
            for track in tracks:
                track_name = track.get("track", {}).get("name", "")
                if song_name == track_name:
                    spotify_ranking.append(((dt.date(year, month, day), tracks.index(track) + 1)))

    youtube_folder = "youtube_top100_small"
    youtube_ranking = []

    for filename in os.listdir("data/" + youtube_folder + "/"):
        if filename == "20160105_1800_data.json":
            break
        if filename.endswith("1800_data.json"):
            json_data1 = open("data/" + youtube_folder + "/" + str(filename)).read()
            youtube_data = json.loads(json_data1)
            video_viewCount = int(youtube_data[index].get("statistics", {}).get("viewCount", ""))
            year = int(filename[:4])
            month = int(filename[4:6])
            day = int(filename[6:8])
            rank = 1
            for video in youtube_data:
                if int(video.get("statistics", {}).get("viewCount", "")) > video_viewCount:
                    rank += 1

            youtube_ranking.append((dt.date(year, month, day), rank))

    plt.plot(*zip(*spotify_ranking), label="spotify " + song_name)
    plt.plot(*zip(*youtube_ranking), label="youtube " + song_name)
    # plt.legend()
    # plt.title(song_name)

power_law_youtube()

# power_law_youtube()
rank_over_time("Hello", 0)
rank_over_time("Sorry", 1)
plt.gca().invert_yaxis()
plt.legend(loc="lower right")
plt.show()
