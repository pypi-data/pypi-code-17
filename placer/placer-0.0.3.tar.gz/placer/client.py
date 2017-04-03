import time
import sys
import getpass
import requests


def login(username, password):
    session = requests.Session()
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.1144"
    session.headers.update({"User-Agent": agent})

    payload = {'op': 'login', 'user': username, 'passwd': password}
    session.post("https://www.reddit.com/post/login", data=payload)

    data = session.get("https://reddit.com/api/me.json").json()
    try:
        modhash = session.get("https://reddit.com/api/me.json").json()["data"]["modhash"]
    except Exception as e:
        import pdb
        pdb.set_trace()

    session.headers.update({"x-modhash": modhash})

    return session


def get_instructions(session, leader_url):
    return requests.post(leader_url).json()


def draw(session, payload):
    return session.post("https://www.reddit.com/api/place/draw.json", data=payload)


def main(username, leader_url):
    password = getpass.getpass()
    session = login(username, password)
    while True:
        try:
            payload = get_instructions(session, leader_url)
            status = draw(session, payload["draw"])
            print(status.text)
            time.sleep(5 * 60)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            time.sleep(1 * 60)

if __name__ == "__main__":
    your_username = sys.argv[1]
    the_leader_url = sys.argv[2]
    main(your_username, the_leader_url)
