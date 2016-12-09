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


def power_law_youtube(day_number):
    json_data1 = open("data/intermediate_data/views_over_time.json").read()
    songs = json.loads(json_data1)
    day = None
    result = []
    for song in songs:
        result.append(dict_to_tuple_list(song, True)[day_number][1])
        if songs.index(song) == 0:
            day = dict_to_tuple_list(song, True)[day_number][0]
    # print(result)
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
    plt.savefig("figures/richgetricher/" + str(day.strftime("%Y%m%d")) + ".png")
    plt.close()


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
            highest = video_viewCount
            highestVideo = ""
            for video in youtube_data:
                if int(video.get("statistics", {}).get("viewCount", "")) > video_viewCount:
                    rank += 1
                if int(video.get("statistics", {}).get("viewCount", "")) > highest:
                    highest = int(video.get("statistics", {}).get("viewCount", ""))
                    highestVideo = video.get("snippet",{}).get("title")

            youtube_ranking.append((dt.date(year, month, day), rank))

    plt.plot(*zip(*spotify_ranking), label="spotify")
    plt.plot(*zip(*youtube_ranking), label="youtube")
    # plt.legend()
    # plt.title(song_name)
    plt.gca().invert_yaxis()
    plt.xlabel("time")
    plt.ylabel("ranking")
    plt.legend(loc="lower right")
    plt.savefig("figures/richgetricher/" + str(index) + song_name.split()[0] + ".png")
    plt.close()

# power_law_youtube()

# power_law_youtube(0)
# power_law_youtube(50)
# power_law_youtube(100)
# power_law_youtube(150)
# power_law_youtube(200)
# power_law_youtube(244)
rank_over_time("Hello", 0)
# rank_over_time("Sorry", 1)
# rank_over_time("Hotline Bling", 2)
# rank_over_time("What Do You Mean?", 3)
# rank_over_time("Stitches", 4)
# rank_over_time("Can't Feel My Face", 5)
# rank_over_time("On My Mind", 6)
# rank_over_time("Locked Away", 7)
# rank_over_time("Focus", 8)
# rank_over_time("How Deep Is Your Love", 9)



