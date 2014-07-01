__author__ = 'matteo'

import sqlite3 as lite
import sys
import os.path
from kivy.app import App
from collections import namedtuple
from background.db.initializer import Initializer


''' namedtuple to retrieve CHUNKS
    used to replace the classic row of sqlite
'''

def namedtuple_factory(cursor, row):
    """
    Usage:
    con.row_factory = namedtuple_factory
    """
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)

class Connector:

    def __init__(self, verbose=False):

        self.verbose = verbose
        self.app = App.get_running_app()
        self.path = self.app.user_data_dir
        self.dbname = 'mycogs.sqlite3'
        self.con = None
        self.checkDBexist()

    def checkDBexist(self):

        if self.verbose:
            print self.path + '/' + self.dbname

        if os.path.exists(self.path + '/' + self.dbname):
            print 'DB found'
            self.con = self.connect()
        else:
            print 'DB not found'
            self.con = self.connect()
            init = Initializer(con=self.con)
            init.initAll()

    ''' connection to database '''
    def connect(self):

        try:
            self.con = lite.connect(self.path + '/' + self.dbname)
            self.con.row_factory = namedtuple_factory
            return self.con

        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    ''' close the connection to the database '''
    def close(self):

        if self.con:
            self.con.close()

    ''' execute an sql statement '''
    def execSql(self, sql, params=None):

        c = self.con.cursor()
        if params:
            c.execute(sql, params)
        else:
            c.execute(sql)
        self.con.commit()

    ''' execute an sql select statement and retrieve data '''
    def selectSql(self, sql, params=None):

        c = self.con.cursor()
        if params:
            c.execute(sql, params)
        else:
            c.execute(sql)

        return c.fetchall()













