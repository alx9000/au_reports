#!/home/common/scripts/python/bin/python3

from datetime import datetime
from fnmatch import fnmatch
import os
import os.path
import sys
import re

prefix = '/usr/local/DATASET/datasets'

def ds_get_name(dset):
    with open(os.path.join(prefix,str(dset),'.matrics.properties')) as f:
        for line in f:
            if re.search('DS_name',line):
                return line.split('=>')[1].strip(", '\n")


