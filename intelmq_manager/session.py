"""Session support for IntelMQ-Manager

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>
"""

import os
import string
import typing
from contextlib import contextmanager
import json

import sqlite3


INIT_DB_SQL = """
CREATE TABLE version (version INTEGER);
INSERT INTO version (version) VALUES (1);
CREATE TABLE session (
    session_id TEXT PRIMARY KEY,
    modified TIMESTAMP,
    data BLOB
);
"""

LOOKUP_SESSION_SQL = """
SELECT data FROM session WHERE session_id = ?;
"""

STORE_SESSION_SQL = """
INSERT OR REPLACE INTO session (session_id, modified, data)
VALUES (?, CURRENT_TIMESTAMP, ?);
"""

class SessionStore:
    """Session store based on SQLite
    """

    def __init__(self, dbname):
        self.dbname = dbname
        if not os.path.isfile(self.dbname):
            self.init_sqlite_db()

    def get_con(self):
        return sqlite3.connect(self.dbname)

    def init_sqlite_db(self):
        with self.get_con() as con:
            con.executescript(INIT_DB_SQL)

    def query(self, stmt, params):
        return self.get_con().execute(stmt, params)

    def transaction(self, stmt, params):
        with self.get_con() as con:
            con.execute(stmt, params)


    #
    # Methods for hug's SessionMiddleware
    #

    def get(self, session_id):
        row = self.query(LOOKUP_SESSION_SQL, (session_id,)).fetchone()
        if row is not None:
            return json.loads(row[0])
        return None

    def exists(self, session_id):
        return self.get(session_id) is not None

    def set(self, session_id, session_data):
        self.transaction(STORE_SESSION_SQL,
                         (session_id, json.dumps(session_data)))

