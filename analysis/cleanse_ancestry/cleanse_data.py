#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas
import glob
import re
import sys
import logging
import praw
import json

from collections import namedtuple
from datetime import datetime


# In[ ]:


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

# with open('creds.json', 'r') as fp:
#     credentials = json.load(fp)

credentials = {
    "CLIENT_ID": None,
    "CLIENT_SECRET": None,
    "CLIENT_AGENT": None,
}

logger.info("Authenticating with Reddit...")
_reddit = praw.Reddit(
    client_id=credentials["CLIENT_ID"],
    client_secret=credentials["CLIENT_SECRET"],
    user_agent=credentials["CLIENT_AGENT"],
#     username=credentials["CLIENT_USERNAME"],
#     password=credentials["CLIENT_PASSWORD"]
)


# In[1]:


all_files = glob.glob('../../data/memes_infections*.log')
def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)
all_files = natural_sort(all_files)

get_file = lambda fname: pandas.read_csv(
    fname,
    sep='\t',
    header=None,
    names=['post_dt',
            'infectee_name',
            'infectee_post_id',
            'infector_name',
            'infector_post_id',
            'comment_or_submission']
)

PATIENT_0 = 'u/woodendoors7'
FIRST_FILE = '../../data/memes_infections.20.19.log'


# In[2]:


all_files


# In[9]:


# memes_infections.20.19.log - add row for patient 0 infection

# with open(FIRST_FILE, 'w') as f:
#     f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
#             '2020-03-20 19:59:59.0',
#             PATIENT_0,
#             '',
#             '',
#             '',
#             ''
#         ))


# In[3]:


# fix ancestry

# 'post_dt',
# 'infectee_name',
# 'infectee_post_id',
# 'infector_name',
# 'infector_post_id',
# 'comment_or_submission'

InfectionLog = namedtuple(
    'InfectionLog',
    ['post_dt', 'infectee_name', 'infectee_post_id', 'infector_name', 'infector_post_id', 'comment_or_submission']
)

def get_missing_infection_logs(user, infectee_data):
    # i1->i2, i2->i3, i3->i4 ... i5->i6 (i2<-i11<-i5)
    if user in infectee_data:
        # this shouldn't happen?
        raise Exception(f"Failed to find missing links for infector '{user}' due to some weird issue")
    possible_infections = []
    for comment in _reddit.redditor(user).comments.new(limit=None):
        if comment.subreddit.name == 'memes':
            parent = comment.parent()
            if parent.author.name in infectee_data or (parent.author_flair_text and "INFECTED" in parent.author_flair_text):
                type_ = "C" if type(parent) is models.Comment else "S"
                possible_infections.append(InfectionLog(datetime.parse(comment.created), comment.author.name, comment.id, parent.author.name, parent.id, type_))
    if not possible_infections:
        # could not find missing link
        raise Exception(f"Failed to find missing links for infector '{user}'")
    # best guess is that it's the infector with the earliest infection date
    best_likely_infection = next(iter(sorted(possible_infections, key=lambda x: x.post_dt)))
    infectee_data[user] = best_likely_infection.infector_name
    if best_likely_infector.infector_name not in infectee_data:
        # there are other missing links
        logs = get_missing_infection_logs(best_likely_infection.infector_name, infectee_data)
        return logs + [best_likely_infection]
    else:
        return [best_likely_infection]

def get_patient_0(user):
    if user not in infectee_infector or user == PATIENT_0:
        return user
    else:
        return get_patient_0(infectee_infector[user])

def fix_ancestry():
    infectee_data = {}
    missing_infectors = set()
    for _fname in all_files:
        print(_fname)
        df = get_file(_fname)
        df.sort_values('post_dt', inplace=True)

        removal_indexes = []
        for index, row in df.iterrows():
            if row.infectee_name in infectee_data:
                # duplicate infection
                removal_indexes.append(index)
                continue
            if row.infectee_name in missing_infectors:
                # a loop was detected in conjunction with missing data, this gets handled later
                continue
            infectee_data[row.infectee_name] = row.infector_name
            if row.infector_name and row.infector_name not in infectee_data:
                # missing infector infection
                missing_infectors.add(row.infector_name)

        # remove rows and write new log
        if removal_indexes:
            df.sort_index(inplace=True)
            df.drop(removal_indexes, inplace=True)
            df.to_csv(_fname, sep='\t', header=None, index=False)
            print(f"{len(removal_indexes)} indexes removed")

    for infector_name in missing_infectors:
        try:
            infection_logs = get_missing_infection_logs(infector_name, infectee_data)
        except Exception as e:
            infectees = [k for k,v in infectee_data.items() if v == infector_name]
            print(e.message)
            # TODO: remove sub-tree from log files :(
            pass
        else:
            # TODO: add logs to corresponding log files :)
            for log in infection_logs:
                pass


# In[4]:


fix_ancestry()


