import json

import requests
import hashlib
import hmac
import base64
import protobuf.CreateAccount_pb2 as CreateAccount
import protobuf.Vote_pb2 as Vote
from protobuf_decoder.protobuf_decoder import Parser

SECRET = bytes('d9913722-3b89-4705-a4b6-f5d413733e6a', 'utf-8')

def vote(person, amount, token, proxy):
    url = "https://api.app.wieisdemol.avrotros.nl/user.v1.UserVoteService/UpdateVote"

    headers = get_headers(token)

    data = Vote.VoteMessage()
    vote_message = data.message.add()
    vote_message.int = 1

    vote = vote_message.votes.add()
    vote.person = person
    vote.amount = amount

    print(data.SerializeToString().hex())
    response = requests.post(url, headers=headers, data=data.SerializeToString(), proxies=proxy)
    print(response.content)
    print(response.status_code)

def get_candidates(proxy=None):
    return json.loads(requests.get("https://app.wieisdemol.avrotros.nl/config.json", proxies=proxy).content)

def create_account(username, email, password, proxy=None):
    url = "https://api.app.wieisdemol.avrotros.nl/identity.v1.IdentityService/PasswordSignUp"

    data = CreateAccount.PasswordSignUp()
    data.email = email
    data.password = password

    headers = {
        "accept-encoding": "gzip",
        "connect-protocol-version": "1",
        "Connection": "Keep-Alive",
        "Content-Type": "application/proto"
    }

    response = requests.post(url, data=data.SerializeToString(), headers=headers, proxies=proxy)

    if response.status_code == 429:
        return None

    response_data = Parser().parse(bytes(response.content).hex())
    token = response_data.results[0].data.results[0].data

    set_notifcation_token(token, proxy)
    set_username(username, token, proxy)

    return {
        "access_token": str(response_data.results[0].data.results[0].data),
        "refresh_token": str(response_data.results[0].data.results[1].data),
        "user_id": str(response_data.results[1].data.results[0].data)
    }

def get_headers(token):
    return {
        "accept-encoding": "gzip",
        "connect-protocol-version": "1",
        "Connection": "Keep-Alive",
        "Content-Type": "application/proto",
        "Host": "api.app.wieisdemol.avrotros.nl",
        "user-agent": "connect-kotlin/0.0",
        "Authorization": "Bearer " + token
    }

def set_username(username, token, proxy):
    url = "https://api.app.wieisdemol.avrotros.nl/user.v1.UserProfileService/SetProfile"

    headers = get_headers(token)
    data = CreateAccount.SetUsername()
    data.username = username
    data.gender = 2
    data.age = 25

    print(data.SerializeToString().hex())

    usernameset = requests.post(url, data.SerializeToString(), headers, proxies=proxy)

    print("USername")
    print(usernameset.status_code)
    print(usernameset.content)

def set_notifcation_token(token, proxy):
    url = "https://api.app.wieisdemol.avrotros.nl/user.v1.UserProfileService/SetNotificationToken"

    headers = get_headers(token)

    data = CreateAccount.NotificationToken()
    data.token = "cLlfgf-ZQtKB7aR42ybrxd:APA91bEP8-ddcRfJnXMgkG97EoB_Pxr8KvWLNT_YrqSvOaTTtxby-WeXdMU-1h3mSTghLN7zZH0R7K5PGvo-fw0QXakUAfanBCBgfph_mDWZLGeCERjDFiWZcyFh6i_c9KUKvP22vedh"
    data.allowed = 2

    response = requests.post(url, headers=headers, data=data.SerializeToString(), proxies=proxy)
