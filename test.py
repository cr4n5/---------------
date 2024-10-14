import requests
import Paillier


def restart(data):
    url = "http://127.0.0.1:5000/restart"
    response = requests.post(url, json=data)
    url = "http://127.0.0.1:5001/restart"
    response = requests.post(url, json=data)


def get_pubkey():
    url = "http://127.0.0.1:5000/get_pubkey"
    response = requests.get(url)
    print(response)
    pubkey = response.json()["key"]
    return pubkey


def submit_vote(data):
    url = "http://127.0.0.1:5001/submit_vote"
    response = requests.post(url, json=data)


def get_vote_result():
    url = "http://127.0.0.1:5000/get_vote_result"
    response = requests.get(url)
    return response.json()


def set_vote_info(data):
    url = "http://127.0.0.1:5000/set_vote_info"
    response = requests.post(url, json=data)


if __name__ == "__main__":
    restart({"vote_obj": "班干部"})
    restart({"vote_obj": "班委"})
    restart({"vote_obj": "学习委员"})

    data = {"vote_obj": "班干部", "list": ["teacher1", "teacher2", "teacher3"]}
    set_vote_info(data)
    data = {"vote_obj": "班委", "list": ["teacher1", "teacher2", "teacher3"]}
    set_vote_info(data)

    pubkey = get_pubkey()

    data = {
        "vote_obj": "班干部",
        "username": "userA",
        "vote": {
            "teacher1": Paillier.encrypt(pubkey["班干部"], 999),
            "teacher2": Paillier.encrypt(pubkey["班干部"], 2),
            "teacher3": Paillier.encrypt(pubkey["班干部"], 98),
        },
        "pubkey": pubkey["班干部"],
    }
    submit_vote(data)

    data = {
        "vote_obj": "班干部",
        "username": "userA",
        "vote": {
            "teacher1":Paillier.encrypt(pubkey["班干部"], 90),
            "teacher2":Paillier.encrypt(pubkey["班干部"], 2),
            "teacher3":Paillier.encrypt(pubkey["班干部"], 98)
        },
        "pubkey": pubkey["班干部"]
    }
    submit_vote(data)

    data={
        "vote_obj": "班干部",
        "username": "userB",
        "vote": {
            "teacher1": Paillier.encrypt(pubkey["班干部"], 4),
            "teacher2": Paillier.encrypt(pubkey["班干部"], 5),
            "teacher3": Paillier.encrypt(pubkey["班干部"], 6),
        },
        "pubkey": pubkey["班干部"],
    }
    submit_vote(data)

    data = {
        "vote_obj": "班干部",
        "username": "userC",
        "vote": {
            "teacher1": Paillier.encrypt(pubkey["班干部"], 7),
            "teacher2": Paillier.encrypt(pubkey["班干部"], 8),
            "teacher3": Paillier.encrypt(pubkey["班干部"], 9),
        },
        "pubkey": pubkey["班干部"],
    }
    submit_vote(data)

    data = {
        "vote_obj": "班委",
        "username": "userA",
        "vote": {
            "teacher1": Paillier.encrypt(pubkey["班委"], 1),
            "teacher2": Paillier.encrypt(pubkey["班委"], 2),
            "teacher3": Paillier.encrypt(pubkey["班委"], 3),
        },
        "pubkey": pubkey["班委"],
    }
    submit_vote(data)

    data = {
        "vote_obj": "班委",
        "username": "userB",
        "vote": {
            "teacher1": Paillier.encrypt(pubkey["班委"], 4),
            "teacher2": Paillier.encrypt(pubkey["班委"], 5),
            "teacher3": Paillier.encrypt(pubkey["班委"], 6),
        },
        "pubkey": pubkey["班委"],
    }
    submit_vote(data)

    print(get_vote_result())
