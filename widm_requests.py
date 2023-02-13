import requests
import hashlib
import hmac
import base64

SECRET = bytes('d9913722-3b89-4705-a4b6-f5d413733e6a', 'utf-8')


def run_request(file_content, proxy = None):
    headers, body = file_content.split('\n\n', 1)

    method, path, _ = headers.split(' ', 2)

    if body and body[-1] == '\n':
        body = body[:-1]

    headers = headers.split('\n')[1:]
    header_lookup = dict()
    for header in headers:
        name, value = header.split(': ', 1)
        header_lookup[name] = value

    body_hashed = hashlib.sha256(body.encode('utf-8')).hexdigest()
    message = f'{method}\n{body_hashed}\n{header_lookup["Content-Type"]}\n{header_lookup["Date"]}\n{path}'
    hmac_value = base64.b64encode(hmac.new(SECRET, bytes(message, 'utf-8'), digestmod=hashlib.sha256).digest())
    header_lookup["X-Signature"] = f'HMAC widm-api:{hmac_value.decode()}'

    if method == "POST":
        return requests.post('https://api.wieisdemol.nl'+path, headers=header_lookup, data=body, proxies=proxy)

    else:
        return requests.get('https://api.wieisdemol.nl'+path, headers=header_lookup, data=body, proxies=proxy)



def get_info():
    return run_request(open("requests/get_info").read())


def create_account(username, email, password, proxy = None):
    data = open("requests/create_account").read().replace("$username", username).replace("$email", email).replace("$password", password)


    return run_request(data, proxy)

def get_profile(token):
    return run_request(open("requests/profile_get").read().replace("$token", token))

def vote(token, candidates, candidate, score):
    data = open("requests/vote").read().replace("$token", token)

    votes = {}

    for vote in candidates:
        if candidates[vote] == candidate:
            votes[candidates[vote]["id"]] = score
        else:
            votes[candidates[vote]["id"]] = 0

    data = data.replace("$votes", str(votes).replace("'", '"'))

    print(data)

    return run_request(data)