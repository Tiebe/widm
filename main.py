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

info = json.loads(widm_requests.get_info().content)

candidates: list = info["candidates"]

for candidate in candidates:
    print(candidate)

proxy = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}

file = open("users-" + str(datetime.now().year) + ".txt", "r+")

if file.read() == "":
    for candidate in candidates:
        username = unidecode("teasstiebe-" + candidate['name'])
        email = unidecode("tedsstwidm-" + candidate['name']+"@tiebe.dev")
        password = "widm2023"

        response = widm_requests.create_account(username, email, password, proxy)

        if response.status_code == 429:
            renew_connection()
            response = widm_requests.create_account(username, email, password)

        print(response.content)
        json_response = json.loads(response.content)
        print(response.content)

        file.write(f"{username}\t{email}\t{password}\t{json_response['token']}\n")

else:
    file.seek(0)
    lines = file.readlines()

    active = {}

    for i,candidate in enumerate(candidates):
        if candidate['active']:
            active[i] = candidate

    for i in active:
        print(active[i])
        token = lines[i].split("\t")[3][:-1]

        profile = json.loads(widm_requests.get_profile(token).content)

        widm_requests.vote(token, active, active[i], profile["available_score"]).content

        
