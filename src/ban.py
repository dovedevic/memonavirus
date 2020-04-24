import json
import praw
import random
import time

infections = open("../data/clean/total_infections.log", "r")
act_infections = [inf.strip().split("\t") for inf in infections.readlines()]
print(len(act_infections), "infections loaded")

infected_users = set()
for ai in act_infections:
    infected_users.add(ai[1])

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
    print("Clearing presence...")
    raise ex
print("Authenticated as {}".format(_reddit.user.me().name))

debug = False
recover = False
recover_at = ""

banned = set()

if not recover:
    for user in infected_users:
        if random.randint(0, 34) == 7:
            banned.add(user)

    with open("../logs/banned.tmp", "w") as fp:
        fp.write("\n".join(banned))
else:
    start = False
    with open("../logs/banned.tmp", "r") as fp:
        for line in fp.readlines():
            if line == recover_at:
                start = True
            if start:
                banned.add(line.strip())

print(len(banned), "users will be banned")

subbie = _reddit.subreddit("memes")
reason = """Memonavirus ban :: Hey {},
You were temporarily banned from r/memes because you fell into the 3% ban group for the Memonavirus event. **Please read**
* This is temporary, it will last 1 day 
* No you will not be unbanned before that 
* No this does not count against you anywhere or anyhow 
* Do not reply to this message 
"""
issues = set()
number = 0
for ban in banned:
    number += 1
    time.sleep(7)
    if not debug:
        try:
            subbie.banned.add(ban[2:], duration=1, ban_reason="Memonavirus Ban", ban_message=reason.format(ban))
            print("{}/{} BEANED".format(number, len(banned)), ban)
        except:
            issues.add(ban)
            print("{}/{} ISSUE BANNING".format(number, len(banned)), ban)

print("Issues were:")
print(issues)

print("Done.")
