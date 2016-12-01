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
    # for i in range(50):
    likes_per_day = get_likes_dislikes(2)
    data = []
    data_with_date = {}
    for k,v1,v2 in likes_per_day:
        total = v1 + v2
        diff = v1 - v2
        data.append((total,diff))
        data_with_date[total] = k

    diff_data = []
    diff_data_with_date = []
    previous = 0
    for k,v in data:
        diff_data.append((k,v-previous))
        diff_data_with_date.append((data_with_date[k],v-previous))
        previous = v
    del diff_data[0]
    print(diff_data_with_date)
    # print(sorted_data)
    # print(diff_data)
    # plt.plot(*zip(*diff_data))
    # plt.title("Hotline Bling")
    # plt.show()


def get_likes_dislikes(index):
    result = []
    counter =0
    for file in os.listdir("data/youtube_top100/"):
        if (counter < 300):
            json_data1 = open("data/youtube_top100/" + file).read()
            youtube = json.loads(json_data1)
            entry = youtube[index]
            # if entry['snippet']['title'] == "Drake - Hotline Bling":
            result.append((file.replace("_1800_data.json", ""),int(entry['statistics']['likeCount']), int(entry['statistics']['dislikeCount'])))
        counter += 1

    return result


plot_hotline_bling()