import os
import json
import datetime
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def find_cascades():
    cascades = dict()
    for i in range(100):
        likes_per_day, song_name = get_likes_dislikes(i, folder="radio538_alarmschijf")
        if len(likes_per_day) > 0:
            data = []
            data_with_date = {}
            for k, v1, v2 in likes_per_day:
                total = v1 + v2
                diff = v1 - v2
                data.append((total, diff))
                data_with_date[total] = k
            diff_data = []
            diff_data_with_date = []
            previous = 0
            for k, v in data:
                diff_data.append((k, v - previous))
                diff_data_with_date.append((data_with_date[k], v - previous))
                previous = v
            del diff_data[0]
            x, y = (zip(*diff_data))
            x = np.array(x)
            y = np.array(y)
            m, b = np.polyfit(x, y, 1)
            cascades[song_name] = m > 0
            if (m > 0):
                plt.plot(*zip(*diff_data))
                plt.plot(x, m * x + b, '-')
                plt.title(song_name)
                filename = song_name.replace(" ","_")
                plt.savefig("figures/cascades/" + filename + str(".png"))
                plt.close()
    return cascades


def plot_popularity_song():
    likes_per_day, song_name = get_likes_dislikes(86, folder="youtube_top100")
    if len(likes_per_day) > 0:
        data = []
        data_with_date = {}
        for k, v1, v2 in likes_per_day:
            total = v1 + v2
            diff = v1 - v2
            data.append((total, diff))
            data_with_date[total] = k

        diff_data = []
        diff_data_with_date = []
        previous = 0
        for k, v in data:
            diff_data.append((k, v - previous))
            diff_data_with_date.append((data_with_date[k], v - previous))
            previous = v
        del diff_data[0]
        plt.plot(*zip(*diff_data))
        x, y = (zip(*diff_data))
        x = np.array(x)
        y = np.array(y)
        m, b = np.polyfit(x, y, 1)
        # plt.plot(x, y, '.')
        plt.plot(x, m * x + b, '-')
        plt.title(song_name)
        plt.show()


def get_likes_dislikes(index, folder="youtube_top100"):
    result = []
    counter = 0
    song_name = ""
    for file in os.listdir("data/" + folder + "/"):
        if (counter < 300):
            json_data1 = open("data/" + folder + "/" + file).read()
            youtube = json.loads(json_data1)
            if (index < len(youtube)):
                entry = youtube[index]
                if song_name == "": song_name = entry.get("snippet", {}).get("title", "")
                # if entry['snippet']['title'] == "Drake - Hotline Bling":
                if str(file) == "20160530_1800_data.json":
                    (key, likes, dislikes) = result[len(result) - 1]
                    step = (int(entry['statistics']['likeCount']) - likes) // 4
                    dislike_step = (int(entry['statistics']['dislikeCount']) - dislikes) // 4
                    result.append(("20160527", likes + step, dislikes + dislike_step))
                    result.append(("20160528", likes + 2 * step, dislikes + 2 * dislike_step))
                    result.append(("20160529", likes + 3 * step, dislikes + 3 * dislike_step))
                elif str(file) == "20160808_1800_data.json":
                    (key, likes, dislikes) = result[len(result) - 1]
                    step = (int(entry['statistics']['likeCount']) - likes) // 3
                    dislike_step = (int(entry['statistics']['dislikeCount']) - dislikes) // 3
                    result.append(("20160806", likes + step, dislikes + dislike_step))
                    result.append(("20160807", likes + 2 * step, dislikes + 2 * dislike_step))
                result.append((file.replace("_1800_data.json", ""), int(entry['statistics']['likeCount']),
                               int(entry['statistics']['dislikeCount'])))
        counter += 1

    return result, song_name


for k, v in find_cascades().items():
    if v:
        print(k)
# plot_popularity_song()
