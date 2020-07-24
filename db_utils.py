#!/home/common/scripts/python/bin/python3

import .au_parse
import os
import os.path
import sqlite3 as sq
from fnmatch import fnmatch

def create_ds_db(sched)
    """Return connection to in-memory database for DS."""

    db = sq.connect(:memory:)
    c = db.cursor()
    db.executescript("""
        create table duties(
            d_no,
            depot,
            son,
            soff,
            on,
            off,
            spread,
            tod
        );
        
        create table meals(
            ix,
            d_no,
            depot,
            start,
            end,
            on,
            off
        );
        """)
            

def create_ts_db(sched)
    """Return connection to in-mem db for TS."""

    db = sq.connect(:memory:)
    c = db.cursor()
    db.executescript("""
        create table runs(
        
        );

        create table trips(

        );

        create table paths(

        );

        create table zpaths(

        );
        """)

            
