#!/home/common/scripts/python/bin/python3

import sqlite3
import db_utils as db


class scheduleDB
    """Create schedule database object in memory."""

    def __init__(self,schedule)
        self.db = db.create_db(schedule)

