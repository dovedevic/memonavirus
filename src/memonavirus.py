import datetime
import logging
import typing
import random
import asyncio

from praw import models

logger = logging.getLogger(__name__)
handler = logging.FileHandler('../logs/{}.log'.format(str(datetime.datetime.now()).replace(' ', '_').replace(':', 'h', 1).replace(':', 'm').split('.')[0][:-2]))
formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class MemonavirusManager:
    """Memonavirus Event Manager :: Integrated with discord.py and praw"""
    def __init__(self, bot, reddit, channel, debug):
        self._reddit = reddit
        self._bot = bot
        self._channel = bot.get_channel(channel)
        self._debug = debug
        today = datetime.datetime.today()
        self._hour = today.hour
        self._lock = False
        self._commentlog = open("../data/memes_comments.{}.{}.log".format(today.day, today.hour), "a")
        self._infectionlog = open("../data/memes_infections.{}.{}.log".format(today.day, today.hour), "a")

    def save_data_new_hour(self, force=False):
        today = datetime.datetime.today()
        if today.hour != self._hour or force:
            logger.info("Data files are being saved...")
            self._hour = today.hour
            self._lock = True
            self._commentlog.flush()
            self._commentlog = open("data/memes_comments.{}.{}.log".format(today.day, today.hour), "a")
            self._infectionlog.flush()
            self._infectionlog = open("data/memes_infections.{}.{}.log".format(today.day, today.hour), "a")
            self._lock = False
            logger.info("Done. `{}.{}` dataset is now live".format(today.day, today.hour))

    async def wait_for_lock(self):
        while self._lock:
            asyncio.sleep(0.1)

    async def on_comment(self, comment: models.Comment):
        try:
            parent = comment.parent()
            if type(parent) is models.Comment:
                # Did an uninfected person reply to an infected persons comment?
                if parent.author_flair_text and "INFECTED" in parent.author_flair_text and ((comment.author_flair_text and "INFECTED" not in comment.author_flair_text) or not comment.author_flair_text):
                    # infection!
                    await self.infect(comment, parent)
            else:  # if type(parent) is models.Submission
                # Did an uninfected person reply to an infected persons submission? Roll dice for a 1 in 100
                if parent.author_flair_text and "INFECTED" in parent.author_flair_text and ((comment.author_flair_text and "INFECTED" not in comment.author_flair_text) or not comment.author_flair_text) and random.randint(1, 100) == 69:
                    await self.infect(comment, parent)
            if self._debug:
                print(comment)
            # TSV Format: Timestamp, Commentor Name, Commentor Comment ID, Commented on User, Commented on Item ID, Item Type, Commented on ?Infected? User
            await self.wait_for_lock()
            self._commentlog.write("{}\tu/{}\t{}\tu/{}\t{}\t{}\t{}\n".format(
                str(datetime.datetime.now()),
                comment.author.name,
                comment.id,
                "deleted" if not parent.author else parent.author.name,
                parent.id,
                "C" if type(parent) is models.Comment else "S",
                "I" if (parent.author_flair_text and "INFECTED" in parent.author_flair_text) else "N"
            ))
        except Exception as ex:
            logger.info("ERROR IN ON_COMMENT")
            logger.info(str(ex))
            pass

    async def infect(self, comment: models.Comment, infected_by: typing.Union[models.Comment, models.Submission]):
        try:
            logger.info("Beginning to infect redditor u/{} because of the {} by u/{}".format(
                comment.author.name,
                "comment" if type(infected_by) is models.Comment else "submission",
                "deleted" if not infected_by.author else infected_by.author.name
            ))
            # TSV Format: Timestamp, Contractor Name, Contractor Comment ID, Commented on User, Commented on Item, Item Type
            await self.wait_for_lock()
            self._infectionlog.write("{}\tu/{}\t{}\tu/{}\t{}\t{}\n".format(
                str(datetime.datetime.now()),
                comment.author.name,
                comment.id,
                "deleted" if not infected_by.author else infected_by.author.name,
                infected_by.id,
                "C" if type(infected_by) is models.Comment else "S"
            ))

            if not self._debug:
                infected_by.subreddit.flair.set(comment.author, flair_template_id='0e8e4996-604b-11ea-bd19-0eedcb93a73d')
            #     await self._channel.send("☣ Redditor u/{} was infected because of the {} by u/{}".format(
            #         comment.author.name,
            #         "comment" if type(infected_by) is models.Comment else "submission",
            #         "deleted" if not infected_by.author else infected_by.author.name
            #     ))
            #     comment.author.message(
            #         "☣ You were infected by the r/memes Memonavirus ☣",
            #         "Hey u/{},\n\nYou contracted the r/memes Memonavirus from u/{}! You contracted it because you commented on their {}, [linked here](https://www.reddit.com{}).\n\n## Don't know what this is about?\n\n[Check out this announcement to see what this is about!](https://www.reddit.com/r/memes/comments/cu5ep9/community_awards_yes_please/)".
            #         format(
            #             comment.author.name,
            #             infected_by.author.name,
            #             "comment" if type(infected_by) is models.Comment else "submission",
            #             infected_by.permalink
            #         )
            #     )

        except Exception as ex:
            logger.info("ERROR IN INFECT")
            logger.info(str(ex))
            pass
