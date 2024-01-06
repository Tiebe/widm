import json
from datetime import datetime

import widm_requests

info = widm_requests.get_candidates()

candidates = info["allCandidates"]
remaining: list = info["currentEpisode"]["remainingCandidateIds"]

proxy = {'http':  'socks5://127.0.0.1:9050',
         'https': 'socks5://127.0.0.1:9050'}

file = open("users-" + str(datetime.now().year) + ".txt", "w+")

file.seek(0)
lines = file.readlines()


for i, candidate in enumerate(remaining):
    email = lines[i].split("\t")[1]
    password = lines[i].split("\t")[2][:-1]

    token = json.loads(widm_requests.login(email, password))
    print(token)
    profile = json.loads(widm_requests.get_profile(token).content)

    widm_requests.vote(token, active, active[i], profile["available_score"]).content
