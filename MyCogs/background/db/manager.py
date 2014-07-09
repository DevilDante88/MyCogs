__author__ = 'Matteo Renzi'

from background.db.connector import Connector

class Manager(Connector):

    def __init__(self, verbose=False):
        Connector.__init__(self, verbose=verbose)

    ##################################################################################################
    ## USER TABLE
    ##################################################################################################

    ''' add an user to the system, return the ID assigned to the user '''
    def addUser(self, email, pwd):

        cur = self.con.cursor()
        cur.execute("INSERT INTO user (email, password) VALUES (?,?)", (email, pwd))

        return cur.lastrowid

    ''' retrive the user ID if the user exist, if not create a new one '''
    def getUserID(self, email, pwd):

        cur = self.con.cursor()
        cur.execute("SELECT id FROM user WHERE email=:email AND password=:pwd",
                    {"email": email, "pwd": pwd})

        row = cur.fetchone()
        if row is None:
            id = self.addUser(email, pwd)
            return id

        else:
            return row[0]

    ''' retrieve the user login account '''
    def getUserAccount(self, id_user):

        cur = self.con.cursor()
        cur.execute("SELECT email, password FROM user WHERE id=:ID",
                    {"ID": id_user})

        return cur.fetchone()

    ##################################################################################################
    ## USER TABLE
    ##################################################################################################

    def getuser_mail(self, id):

        return self.selectSql("SELECT uid FROM user_mail WHERE id=:id_user",
                              dict(id_user=id))

    def add_user_mail(self, id, uids):

        SQL_INSERT = """
            INSERT OR IGNORE INTO user_mail
                (id,uid)
            VALUES
                (:id,:uid)
            """

        data = [(id, x) for x in uids]

        cur = self.con.cursor()
        cur.executemany(SQL_INSERT, data)
        self.con.commit()

    ##################################################################################################
    ## SENDER TABLE
    ##################################################################################################

    ''' add an user to the system, return the ID assigned to the user '''
    def addSender(self, id_user, email, name):

        cur = self.con.cursor()
        cur.execute("INSERT INTO sender (id_user, email, name) VALUES (?,?,?)",
                        (id_user, email, name))

        return cur.lastrowid

    def getSenders(self, id_user):

        cur = self.con.cursor()
        cur.execute('SELECT id, email, name FROM sender WHERE id_user=:ID', {'ID': id_user})

        row = cur.fetchall()
        return row

    ''' retrive the user ID if the user exist
        possible returns of multiple values
    '''
    def getSenderID(self, id_user, email, name):

        cur = self.con.cursor()
        cur.execute("SELECT id FROM sender WHERE email=:email AND name=:name",
                    {"email": email, "name": name})

        row = cur.fetchone()
        if row is None:
            id = self.addSender(id_user, email, name)
            return id
        else:
            return row[0]

    ##################################################################################################
    ## SENDER MAIL TABLE
    ##################################################################################################

    def addsender_mail(self, id, userid, uid):

        ##isparsed is set to default to 0

        SQL_INSERT = """
            INSERT OR IGNORE INTO sender_mail
                (id,userid,uid)
            VALUES
                (:id,:userid,:uid)
            """
        return self.execSql(SQL_INSERT, dict(id=id, userid=userid, uid=uid))

    ''' retrieve the list of the parsed or unparsed UID by a sender
        :param isparsed - if 0 get unparsed list if 1 get parsed list
    '''
    def getsender_uids(self, id, userid, isparsed=0):

        SQL_SELECT = "SELECT uid FROM sender_mail WHERE id=:id AND userid=:userid AND isparsed=:isparsed"

        return self.selectSql(SQL_SELECT, dict(id=id, userid=userid, isparsed=isparsed))

    ''' set the uid to parsed '''
    def setparsed(self, uid):

        SQL_UPDATE = "UPDATE sender_mail SET isparsed=1 WHERE uid=:uid"

        return self.execSql(SQL_UPDATE, dict(uid=uid))

    ##################################################################################################
    ## KNOWLEDGE
    ##################################################################################################

    def insert_kl(self, function):

        SQL_INSERT = """
            INSERT OR IGNORE INTO knowledge
                (chunk,found,category,url,disambiguation_url,ngram)
            VALUES
                (:chunk,:found,:category,:url,:disambiguation_url,:ngram)
            """

        cur = self.con.cursor()
        cur.executemany(SQL_INSERT, function())
        self.con.commit()

    def insert_single_kl(self, chunk, found, category, url, dis, ngram):

        SQL_INSERT = """
            INSERT OR IGNORE INTO knowledge
                (chunk,found,category,url,disambiguation_url,ngram)
            VALUES
                (:chunk,:found,:category,:url,:disambiguation_url,:ngram)
            """

        return self.execSql(SQL_INSERT, dict(chunk=chunk,
                                             found=found,
                                             category=category,
                                             url=url,
                                             disambiguation_url=dis,
                                             ngram=ngram))

    def insert_kl_nocat(self, chunk, found, url, dis, ngram):

        SQL_INSERT = """
            INSERT OR IGNORE INTO knowledge
                (chunk,found,url,category,disambiguation_url,ngram)
            VALUES
                (:chunk,:found,:url,:category,:disambiguation_url,:ngram)
            """

        return self.execSql(SQL_INSERT, dict(chunk=chunk,
                                             found=found,
                                             url=url,
                                             category='',
                                             disambiguation_url=dis,
                                             ngram=ngram))

    ''' retrieve the chunk if exist '''
    def existchunk_kl(self, chunk):

        #this is the fastest query to retrieve if an element exist or not
        QUERY = "SELECT chunk FROM knowledge WHERE chunk=:chunk LIMIT 1"
        return self.selectSql(QUERY, dict(chunk=chunk))

    def getchunk_kl(self, chunk):

        QUERY = "SELECT found, category, url, disambiguation_url, ngram FROM knowledge WHERE chunk=:chunk"
        chunk = chunk.decode('utf-8', errors='ignore')
        return self.selectSql(QUERY, dict(chunk=chunk))

    ''' retrieve the meanings for that list '''
    def getfound_kl(self, chunk):

        QUERY = "SELECT found FROM knowledge WHERE chunk=:chunk"
        return self.selectSql(QUERY, dict(chunk=chunk))

    def del_row_kl(self, chunk, found):

        QUERY = "DELETE FROM knowledge WHERE chunk=:chunk AND found=:found"
        chunk = chunk.decode('utf-8', errors='ignore')
        found = found.decode('utf-8', errors='ignore')
        return self.execSql(QUERY, dict(chunk=chunk, found=found))

    def update_cat(self, chunk, cat):

        QUERY = "UPDATE knowledge SET category=:category WHERE chunk=:chunk"
        #chunk = chunk.decode('utf-8', errors='ignore')
        cat = cat.decode('utf-8', errors='ignore')
        return self.execSql(QUERY, dict(chunk=chunk, category=cat))


    ##################################################################################################
    ## USERDATA
    ##################################################################################################

    ''' retrieve the chunk if exist '''
    def existchunk_ud(self, chunk, userid, senderid):

        #this is the fastest query to retrieve if an element exist or not
        QUERY = "SELECT chunk FROM userdata WHERE chunk=:chunk AND userid=:userid AND senderid=:senderid"
        chunk = chunk.decode('utf-8', errors='ignore')
        return self.selectSql(QUERY, dict(chunk=chunk, userid=userid, senderid=senderid))

    def getchunk_ud(self, chunk, userid, senderid):

        #this is the fastest query to retrieve if an element exist or not
        QUERY = "SELECT * FROM userdata WHERE chunk=:chunk AND userid=:userid AND senderid=:senderid"
        chunk = chunk.decode('utf-8', errors='ignore')
        return self.selectSql(QUERY, dict(chunk=chunk, userid=userid, senderid=senderid))

    def getall_ud(self, userid, senderid, status):

        QUERY = """SELECT chunk, found, score
            FROM userdata
            WHERE userid=:userid AND senderid=:senderid AND status=:status
            ORDER BY score DESC
        """
        return self.selectSql(QUERY, dict(userid=userid, senderid=senderid, status=status))

    def updatescore(self, score, chunk, userid, senderid):

        QUERY = "UPDATE userdata SET score = score + :score WHERE " \
                "chunk=:chunk AND userid=:userid AND senderid=:senderid"
        chunk = chunk.decode('utf-8', errors='ignore')
        return self.execSql(QUERY, dict(userid=userid, senderid=senderid, score=score, chunk=chunk))

    def update_ud(self, userid, senderid, chunk, found, status, score):
        QUERY = "UPDATE userdata SET chunk=:chunk, found=:found, status=:status, score=:score WHERE " \
                "chunk=:chunk AND userid=:userid AND senderid=:senderid"
        chunk = chunk.decode('utf-8', errors='ignore')
        return self.execSql(QUERY, dict(userid=userid, senderid=senderid, chunk=chunk,
                                        found=found, status=status, score=score))

    def insert_ud(self, function):

        SQL_INSERT = """
            INSERT INTO userdata
                (userid,senderid,chunk,found,status,score)
            VALUES
                (:userid,:senderid,:chunk,:found,:status,:score)
            """

        cur = self.con.cursor()
        cur.executemany(SQL_INSERT, function())
        self.con.commit()

    def insert_single_ud(self, userid, senderid, chunk, found, status, score):

        SQL_INSERT = """
            INSERT INTO userdata
                (userid,senderid,chunk,found,status,score)
            VALUES
                (:userid,:senderid,:chunk,:found,:status,:score)
            """

        return self.execSql(SQL_INSERT, dict(userid=userid,
                                             senderid=senderid,
                                             chunk=chunk,
                                             found=found,
                                             status=status,
                                             score=score))

    def del_chunk_ud(self, userid, senderid, chunk):

        QUERY = "DELETE FROM userdata WHERE chunk=:chunk AND userid=:userid AND senderid=:senderid"
        chunk = chunk.decode('utf-8', errors='ignore')
        return self.execSql(QUERY, dict(userid=userid, senderid=senderid, chunk=chunk))







