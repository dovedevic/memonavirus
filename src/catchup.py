import os
import praw
import json


with open('creds.json', 'r') as fp:
    credentials = json.load(fp)

print("Authenticating with Reddit...")
_reddit = praw.Reddit(
    client_id=credentials["CLIENT_ID"],
    client_secret=credentials["CLIENT_SECRET"],
    user_agent=credentials["CLIENT_AGENT"],
    username=credentials["CLIENT_USERNAME"],
    password=credentials["CLIENT_PASSWORD"]
)
try:
    if _reddit.user.me().name != credentials["CLIENT_USERNAME"]:
        raise AssertionError("Authenticated unexpectedly!")
except Exception as ex:
    print("Authentication failed. Check the password, ID, or secret. Goodbye...")
    raise ex
print("Authenticated as {}".format(_reddit.user.me().name))


past_infection_files = ["../data/" + f for f in os.listdir("../data") if f.startswith("memes_infections") and f.endswith(".log")]
subbie = _reddit.subreddit("memes")
for pif in past_infection_files:
    with open(pif, "r") as fp:
        for line in fp.readlines():
            try:
                # TSV Format: Timestamp, Contractor Name, Contractor Comment ID, Commented on User, Commented on Item, Item Type
                subbie.flair.set(_reddit.redditor(line.split('\t')[1]), flair_template_id='0e8e4996-604b-11ea-bd19-0eedcb93a73d')
                print(_reddit.redditor(line.split('\t')[1]).name, "infected")
            except:
                print(line, "error in infection")
