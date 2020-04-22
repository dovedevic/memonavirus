import praw, json, datetime, time

from praw import models

with open('../../../src/creds.json', 'r') as fp:
    credentials = json.load(fp)


_reddit = praw.Reddit(
    client_id=credentials["CLIENT_ID"],
    client_secret=credentials["CLIENT_SECRET"],
    user_agent=credentials["CLIENT_AGENT"],
    username=credentials["CLIENT_USERNAME"],
    password=credentials["CLIENT_PASSWORD"]
)


def utc2local (utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.datetime.fromtimestamp (epoch) - datetime.datetime.utcfromtimestamp (epoch)
    return utc + offset

while True:
    com = _reddit.comment(url=input("URL: "))
    print("\t".join(["u/" + com.author.name, com.id, "C", str(utc2local(datetime.datetime.utcfromtimestamp(com.created_utc)))]))
