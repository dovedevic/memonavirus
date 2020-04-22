import praw, datetime, time, json
from praw import models

with open('../../src/creds.json', 'r') as fp:
    credentials = json.load(fp)

_reddit = praw.Reddit(
    client_id=credentials["CLIENT_ID"],
    client_secret=credentials["CLIENT_SECRET"],
    user_agent=credentials["CLIENT_AGENT"],
    username=credentials["CLIENT_USERNAME"],
    password=credentials["CLIENT_PASSWORD"]
)

after = "2020-03-20 19:59:59"
def utc2local (utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.datetime.fromtimestamp (epoch) - datetime.datetime.utcfromtimestamp (epoch)
    return utc + offset

while True:
    for cmt in _reddit.redditor(input("Redditor: ")).comments.new(limit=None):
        if str(utc2local(datetime.datetime.utcfromtimestamp(cmt.created_utc))) < after:
            break
        if cmt.subreddit != "memes":
            continue
        parent = cmt.parent()
        print([str(utc2local(datetime.datetime.utcfromtimestamp(cmt.created_utc))), str(cmt.id), str(parent.author.name) if hasattr(parent.author, "name") else "u/deleted", "C" if type(parent) == models.Comment else "S", str(parent.id)], "https://www.reddit.com" + cmt.permalink)
