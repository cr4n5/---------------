import requests
import Paillier

def restart():
    url="http://127.0.0.1:5000/restart"
    response = requests.post(url)
    url="http://127.0.0.1:5001/restart"
    response = requests.post(url)

def get_pubkey():
    url="http://127.0.0.1:5000/get_pubkey"
    response = requests.post(url)
    pubkey = response.json()['key']
    return pubkey

def submit_vote(data):
    url="http://127.0.0.1:5001/submit_vote"
    response = requests.post(url, json=data)

def get_vote_result():
    url="http://127.0.0.1:5000/get_vote_result"
    response = requests.post(url)
    return response.json()

if __name__ == "__main__":
    restart()
    pubkey = get_pubkey()

    data={
        "username": "userA",
        "vote": {
            "teacher1":Paillier.encrypt(pubkey, 999),
            "teacher2":Paillier.encrypt(pubkey, 2),
            "teacher3":Paillier.encrypt(pubkey, 98)
        },
        "pubkey": pubkey
    }
    submit_vote(data)

    data={
        "username": "userB",
        "vote": {
            "teacher1":Paillier.encrypt(pubkey, 4),
            "teacher2":Paillier.encrypt(pubkey, 5),
            "teacher3":Paillier.encrypt(pubkey, 6)
        },
        "pubkey": pubkey
    }
    submit_vote(data)

    data={
        "username": "userC",
        "vote": {
            "teacher1":Paillier.encrypt(pubkey, 7),
            "teacher2":Paillier.encrypt(pubkey, 8),
            "teacher3":Paillier.encrypt(pubkey, 9)
        },
        "pubkey": pubkey
    }
    submit_vote(data)
    
    print(get_vote_result())
