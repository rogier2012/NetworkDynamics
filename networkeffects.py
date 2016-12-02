import os
import json
import datetime
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_views_time():
    data = []
    song_name = ""
    for file in os.listdir("data/youtube_top100" + "/"):
        json_data1 = open("data/youtube_top100" + "/" + file).read()
        youtube = json.loads(json_data1)
        entry = youtube[47]
        year = int(file[:4])
        month = int(file[4:6])
        day = int(file[6:8])
        if song_name == "": song_name = entry.get("snippet", {}).get("title", "")
        if str(file) == "20160530_1800_data.json":
            (key, viewCount) = data[len(data) - 1]
            step = (int(entry['statistics']['viewCount']) - viewCount) // 4
            d27 = datetime.date(2016,5,27)
            d28 = datetime.date(2016, 5, 28)
            d29 = datetime.date(2016, 5, 29)
            data.append((d27, viewCount + step))
            data.append((d28, viewCount + 2 * step))
            data.append((d29, viewCount + 3 * step))
        elif str(file) == "20160808_1800_data.json":
            (key, viewCount) = data[len(data) - 1]
            step = (int(entry['statistics']['viewCount']) - viewCount) // 3
            d06 = datetime.date(2016, 8, 6)
            d07 = datetime.date(2016, 8, 7)
            data.append((d06, viewCount + step))
            data.append((d07, viewCount + 2 * step))
        data.append((datetime.date(year,month,day), int(entry['statistics']['viewCount'])))
    plt.plot(*zip(*data))
    plt.title(song_name)
    plt.show()
    plt.close()

plot_views_time()