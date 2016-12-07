import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

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

json_data1 = open("data/intermediate_data/views_over_time.json").read()
songs = json.loads(json_data1)

data = dict_to_tuple_list(songs[0], True)
diff_data = derivative_data(data)

per_day = [0,0,0,0,0,0,0]
x = range(len(per_day))
width = 1/1.5
for k,v in data:
    per_day[k.weekday()] = per_day[k.weekday()] + v

plt.bar(x,per_day,width,color="blue")
plt.ylim(ymin=min(per_day))
plt.show()