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
    for track in spotify_tracks:
        track_name = track.get("track", {}).get("name", "")
        result[track_name] = {"index": spotify_tracks.index(track), "likes": []}

    for filename in os.listdir("data/youtube_top100"):
        if (filename.endswith(".json")):
            year = int(filename[:4])
            month = int(filename[4:6])
            day = int(filename[6:8])
            date = datetime.date(year,month,day)
            datenum = matplotlib.dates.date2num(date)
            json_data = open("data/youtube_top100/" + filename).read()
            youtube_data = json.loads(json_data)
            for video in youtube_data:

                statistics = video.get("statistics", {})
                likes = statistics.get("likeCount")
                dislikes = statistics.get("dislikeCount")
                for k,v in result.items():
                    if v.get("index",-1) == youtube_data.index(video):
                        v.get("likes").append((int(likes)-int(dislikes)))

    return result



# print(difference_likes_dislikes())
data = difference_likes_dislikes().popitem()
# print(data[1].get("likes").keys())
begin = datetime.date(2015,11,9)
end = datetime.date(2016,11,28)
delta = datetime.timedelta(days=1)
dates = drange(begin,end,delta)



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