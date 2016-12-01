import os
import json
import datetime
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import operator

def plot_hotline_bling():
    likes_per_day = {}
    likes_per_day = get_likes_dislikes_hotline_bling()
    data = dict()
    for k,v in likes_per_day.items():
        total = int(v[0]) + int(v[1])
        diff = int(v[0]) - int(v[1])
        data[total] = diff
    print(data)
    sorted_data = (sorted(data.items(), key=operator.itemgetter(0)))
    diff_data = []
    previous = 0
    for k,v in sorted_data:
        diff_data.append((k,v-previous))
        previous = v
    del diff_data[0]
    plt.plot(*zip(*diff_data))
    plt.title("Koudspel")
    plt.show()


def get_likes_dislikes_hotline_bling():
    result = dict()
    counter =0
    for file in os.listdir("data/youtube_top100/"):
        if (counter < 20):
            json_data1 = open("data/youtube_top100/" + file).read()
            youtube = json.loads(json_data1)
            entry = youtube[2]
            # if entry['snippet']['title'] == "Drake - Hotline Bling":
            result[(file.replace("_1800_data.json", ""))] = (int(entry['statistics']['likeCount']), int(entry['statistics']['dislikeCount']))
        counter += 1

    return result


plot_hotline_bling()