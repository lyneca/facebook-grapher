import numpy as np
import matplotlib.pyplot as plt
import json
import math
import re
import uncurl
import requests
from datetime import datetime

your_id = '100009563164658'
end = '{\n   '

print("1. Go to messenger.com and to the conversation you want to graph.")
print("2. Press F12 and go to the network tab.")
print("3. Scroll up in the conversation so that you load more messages.")
print("4. You should see a POST request to /api/graphqlbatch/. Right click on this request, and click \"Copy as cURL\".")
curl = input("Paste the cURL request you copied here: ")

your_name = input("What is your name? ")
their_name = input("What is their name? ")

print("Tidying cURL request...")
curl = re.sub(r"%2C%22before%22%3A\d+%7D", "%7D", curl)
curl = re.sub(r"message_limit%22%3A\d+%2C", "message_limit%22%3A10000000%2C", curl)
curl = re.sub(r" --2.0", "", curl)

print("Getting data...")
r = eval(uncurl.parse(curl))

print("Decoding and extracting...")
x = r.content.decode('U8')
j = json.loads(x[:x.index(end) - 1])
j = j['o0']['data']['message_thread']
messages = j['messages']['nodes']

other = [x for x in messages if x['message_sender']['id'] != your_id]
you = [x for x in messages if x['message_sender']['id'] == your_id]
other_times = [x['timestamp_precise'] for x in other]
you_times = [x['timestamp_precise'] for x in you]
other_times = [datetime.fromtimestamp(int(x)/1000) for x in other_times]
you_times = [datetime.fromtimestamp(int(x)/1000) for x in you_times]

print("Sorting...")
days = sorted(list(set(["{}-{}-{}".format(x.year, x.month, x.day) for x in other_times + you_times])), key=lambda x: [int(y) for y in x.split('-')])

_other_days = ["{}-{}-{}".format(x.year, x.month, x.day) for x in other_times]
other_days = sorted(list(set(_other_days)))
other_counts = [_other_days.count(x) for x in days]

_you_days = ["{}-{}-{}".format(x.year, x.month, x.day) for x in you_times]
you_days = sorted(list(set(_you_days)))
you_counts = [_you_days.count(x) for x in days]

width = 0.35
ind = np.arange(len(days))

print("Graphing...")
fig, ax = plt.subplots(figsize=(16,8))
ax.bar(ind, you_counts, width, label=your_name)
ax.bar(ind+width, other_counts, width, label=their_name)
#  ax.plot(you_counts, label=your_name)
#  ax.plot(other_counts, label=their_name)
ax.set_title("Messages Sent By Day")
ax.set_ylabel("Messages Sent")
ax.set_xlabel("Date")
space = 2
ax.set_xticks([x*(len(days)//10) for x in range(10)])
ax.set_xticklabels(days[::len(days)//10] + [days[-1]])
ax.legend()
print("Saving...")
name = your_name + '_' + their_name + '_daily' + '.png'
fig.savefig(name)
print("Done. Saved to '{}'".format(name))
#  plt.show()
