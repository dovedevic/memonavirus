#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas
import glob
import re

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
FIX_FILE = '../../data/memes_infections.21.21.log'


# In[9]:


# memes_infections.20.19.log - add row for patient 0 infection

with open(FIRST_FILE, 'w') as f:
    f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
            '2020-03-20 19:59:59.0',
            PATIENT_0,
            '',
            '',
            '',
            ''
        ))


# In[8]:


# fix ancestry

def fix_ancestry(fname):
    infectee_log = set()
    for _fname in all_files:
        print(_fname)
        df = get_file(_fname)
        df.sort_values('post_dt', inplace=True)

        removal_indexes = []
        for index, row in df.iterrows():
            if row.infectee_name in infectee_log:
                removal_indexes.append(index)
            else:
                infectee_log.add(row.infectee_name)

        # remove rows and write new log
        if removal_indexes:
            print(len(removal_indexes))
            df.sort_index(inplace=True)
            df.drop(removal_indexes, inplace=True)
            df.to_csv(_fname, sep='\t', header=None, index=False)
        if _fname == fname:
            break


# In[10]:


fix_ancestry(FIX_FILE)

