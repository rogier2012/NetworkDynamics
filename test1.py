import json
import os
# json_data1=open("data/spotify_top100/20151109_1800_data.json").read()
# spotify_data = json.loads(json_data1)
# # print(youtube_data[0].get("snippet",{}).get("title"),"")
# spotify_tracks = spotify_data.get("tracks").get("items", [])
# for track in spotify_tracks:
#     track_name = track.get("track",{}).get("name","")
#     # print(track_name + " with " + str(likes) + " likes and "  + str(dislikes) + " dislikes")
#
#     print("rank_over_time(\"" +track_name  + "\", " + str(spotify_tracks.index(track)) + ")")
# counter = 0
# folder = "youtube_top100"
#
#
# for filename in os.listdir("data/"+folder):
#     counter += 1
#     json_data2 = open("data/"+folder+"/"+str(filename)).read()
#     youtube_data = json.loads(json_data2)
#     print(str(counter) + ". " + filename)
#     print(len(youtube_data))
#
#     break

for filename in os.listdir("figures/networkeffects"):
    if "diff_1" in filename:
        print("\\includegraphics[width=0.33\\textwidth]{figures/networkeffects/" + filename + "}")
