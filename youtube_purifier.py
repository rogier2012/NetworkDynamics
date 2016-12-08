import os
import json

folder = "youtube_top100_small"


for filename in os.listdir("data/"+folder):
    json_data2 = open("data/" + folder + "/" + str(filename)).read()
    youtube_data = json.loads(json_data2)
    old = len(youtube_data)
    indices = []
    for video in youtube_data:
        if "Jumpman" in video.get("snippet", {}).get("title", ""):
            indices.append(youtube_data.index(video))
        elif "Back to Back" in video.get("snippet", {}).get("title", ""):
            indices.append(youtube_data.index(video))
        elif "Big Rings" in video.get("snippet", {}).get("title", ""):
            indices.append(youtube_data.index(video))

    for i in indices:
        del youtube_data[i]
    new = len(youtube_data)
    if (old == 100 and new == 97):
        with open("data/" + folder + "/" + str(filename), 'w') as outfile:
            json.dump(youtube_data, outfile)
    else:
        print(filename)