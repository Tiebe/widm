import random

import widm_requests
import json
from datetime import datetime
from unidecode import unidecode
from stem import Signal
from stem.control import Controller

def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)

info = widm_requests.get_candidates()

candidates = info["allCandidates"]
remaining: list = info["currentEpisode"]["remainingCandidateIds"]

proxy = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}

file = open("users-" + str(datetime.now().year) + ".txt", "w+")


for candidate in remaining:
    name = candidates[candidate]

    username = unidecode("tiebe" + name).encode()
    email = unidecode("widm" + name + "@tiebe.dev").encode()
    password = b"Widm2024!"

    print(email)
    response = widm_requests.create_account(username, email, password)

    if response is None:
        renew_connection()
        response = widm_requests.create_account(username, email, password)

    print(response)

    widm_requests.vote(candidate, 100, response["access_token"], None)

    file.write(f"{str(username)}\t{str(email)}\t{str(password)}\n")

