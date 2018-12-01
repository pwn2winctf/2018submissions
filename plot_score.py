#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
from math import floor, log
import datetime
import itertools
import json

topN = 5

def compute_score(num_solves):
    K, V, minpts, maxpts = 80.0, 3.0, 50, 500
    return int(max(minpts, floor(maxpts - K*log((num_solves + V)/(1 + V), 2))))


with open("accepted-submissions.json") as f:
    scoreboard = json.load(f)

standings = scoreboard['standings']
standings.sort(key=lambda t: t['pos'])

all_solves = sorted(itertools.chain.from_iterable([(data['time'], chall_id) for chall_id, data in t['taskStats'].items()]
                                                  for t in standings))

top_standings = standings[:topN]
top_solves = {t['team']: sorted((data['time'], chall_id) for chall_id, data in t['taskStats'].items()) for t in top_standings}

chall_solves = defaultdict(lambda: 0)
time_axis = []
score_axis = defaultdict(lambda: [])

for time, chall_id in all_solves:
    time_axis.append(datetime.datetime.fromtimestamp(time))
    chall_solves[chall_id] += 1

    for team, team_challs in top_solves.items():
        score = 0
        for team_time, team_chall in team_challs:
            if team_time > time:
                break
            score += compute_score(chall_solves[team_chall])

        score_axis[team].append(score)

for i, team in enumerate(t['team'] for t in top_standings):
    for line in plt.plot(time_axis, score_axis[team], label=team):
        line.set_zorder(topN - i)

plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))

plt.ylabel('Team Score')
plt.legend(prop={'size': 8})
plt.tight_layout()
plt.savefig('top.pdf')
plt.savefig('top.svg')

