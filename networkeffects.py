import os
import json
import datetime
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)


def store_time_views():
    data = []
    for i in range(100):
        int_result = []
        song_name = ""
        for file in os.listdir("data/youtube_top100" + "/"):
            json_data1 = open("data/youtube_top100" + "/" + file).read()
            youtube = json.loads(json_data1)
            if (i < len(youtube)):
                entry = youtube[i]
            else:
                entry = {}
            year = int(file[:4])
            month = int(file[4:6])
            day = int(file[6:8])
            if (len(entry) > 0):
                if song_name == "": song_name = entry.get("snippet", {}).get("title", "")
                if str(file) == "20160530_1800_data.json":
                    (key, viewCount) = int_result[len(int_result) - 1]
                    step = (int(entry['statistics']['viewCount']) - viewCount) // 4
                    d27 = datetime.date(2016,5,27)
                    d28 = datetime.date(2016, 5, 28)
                    d29 = datetime.date(2016, 5, 29)
                    int_result.append((d27, viewCount + step))
                    int_result.append((d28, viewCount + 2 * step))
                    int_result.append((d29, viewCount + 3 * step))
                elif str(file) == "20160808_1800_data.json":
                    (key, viewCount) = int_result[len(int_result) - 1]
                    step = (int(entry['statistics']['viewCount']) - viewCount) // 3
                    d06 = datetime.date(2016, 8, 6)
                    d07 = datetime.date(2016, 8, 7)
                    int_result.append((d06, viewCount + step))
                    int_result.append((d07, viewCount + 2 * step))
                int_result.append((datetime.date(year, month, day), int(entry['statistics']['viewCount'])))

        result = {}
        for k,v in int_result:
            result[str(k)] = v
        if len(result) > 0: data.append(result)
    with open('data/intermediate_data/views_over_time.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

store_time_views()
