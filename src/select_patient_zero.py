import praw
import json
import random

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

print("Getting sticky comment...")
# Link is https://www.reddit.com/r/memes/comments/fky5cz/rmemes_memonavirus_community_event/fkvgw7t/
volunteer_thread = _reddit.comment(url="https://www.reddit.com/r/memes/comments/fky5cz/rmemes_memonavirus_community_event/fkvgw7t/")
print("Getting comment replies...")
volunteer_thread.refresh()
volunteer_thread.replies.replace_more(limit=None)
volunteers = set()
print("Enumerating replies...")
for volunteer in volunteer_thread.replies:
    if volunteer.author:
        volunteers.add(volunteer.author.name)
print("There were", len(volunteers), "volunteers!")
volunteers = list(volunteers)
pick1 = random.choice(volunteers)
pick2 = random.choice(volunteers)
pick3 = random.choice(volunteers)
print("1st pick is u/{}".format(pick1))
print("2nd pick is u/{}".format(pick2))
print("3rd pick is u/{}".format(pick3))

