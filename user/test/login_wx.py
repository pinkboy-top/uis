import requests

api = "https://cat-match.easygame2021.com/sheep/v1/user/login_wx?"

data = {
    "code": "0834QK000syPzO1keI100cJRvp14QK0C"
}

prox = {
    "https": "127.0.0.1:7890"
}

req = requests.post(api, data=data, verify=False)

print(req)

