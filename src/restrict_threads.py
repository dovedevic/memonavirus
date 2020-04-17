import sys
import datetime
import logging
import praw
import json

from praw import models

logger = logging.getLogger(__name__)
handler = logging.FileHandler('../logs/{}.log'.format(str(datetime.datetime.now()).replace(' ', '_').replace(':', 'h', 1).replace(':', 'm').split('.')[0][:-2]))
formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

with open('creds.json', 'r') as fp:
    credentials = json.load(fp)

logger.info("Authenticating with Reddit...")
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
    logger.error("Authentication failed. Check the password, ID, or secret. Goodbye...")
    logger.debug("Clearing presence...")
    raise ex
logger.info("Authenticated as {}".format(_reddit.user.me().name))

# Variables
_debug = True
infected_thread_id = "t3_fesexv" if _debug else "t3_tbd"
noninfected_thread_id = "t3_fesexv" if _debug else "t3_tbd"
# End Variables


def on_comment(comment: models.Comment):
    try:
        if comment.link_id == infected_thread_id:
            if not (comment.author and comment.author_flair_text and "INFECTED" in comment.author_flair_text):
                logger.debug("Removing comment by u/{} as they are not infected".format("deleted" if not comment.author or not hasattr(comment.author, "name") else comment.author.name))
                comment.mod.remove()
        elif comment.link_id == noninfected_thread_id:
            if not (comment.author and ((comment.author_flair_text and "INFECTED" not in comment.author_flair_text) or (not comment.author_flair_text))):
                logger.debug("Removing comment by u/{} as they are infected".format("deleted" if not comment.author or not hasattr(comment.author, "name") else comment.author.name))
                comment.mod.remove()

    except Exception as ex:
        logger.info("ERROR IN ON_COMMENT")
        logger.info(str(ex))
        pass


logger.info("Starting comment streams...")

while True:
    try:
        for cmt in _reddit.subreddit('memes').stream.comments(skip_existing=True):
            on_comment(cmt)
    except Exception as ex:
        logging.info("An error occurred in the comment thread. It was:\n{}".format(str(ex)))

# We should never get here...
