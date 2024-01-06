import json
from datetime import datetime

import widm_requests

info = widm_requests.get_candidates()

candidates = info["allCandidates"]
remaining: list = info["currentEpisode"]["remainingCandidateIds"]

proxy = {'http':  'socks5://127.0.0.1:9050',
         'https': 'socks5://127.0.0.1:9050'}

file = open("users-" + str(datetime.now().year) + ".txt", "r+")

file.seek(0)
lines = file.readlines()

points = 100 * 2**(int(info["currentEpisode"]["episodeId"])-1)
print(points)

for i, candidate in enumerate(remaining):
    email = lines[i].split("\t")[1]
    password = lines[i].split("\t")[2][:-1]

    tokens = widm_requests.login(email, password)

    #widm_requests.vote(candidate, points, tokens["access_token"], None)

