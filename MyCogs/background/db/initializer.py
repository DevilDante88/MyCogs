__author__ = 'Matteo Renzi'

class Initializer:

    def __init__(self, con, verbose=False):

        self.verbose = verbose
        self.con = con

    ''' initialize user table '''
    def initUsers(self):

        if self.verbose:
            print 'START INIT USERS TABLE'

        with self.con:

            cur = self.con.cursor()
            cur.execute("DROP TABLE IF EXISTS user")
            cur.execute("CREATE TABLE user ( "
                        "id INTEGER PRIMARY KEY, "
                        "email CHAR(50) NOT NULL, "
                        "readed TEXT DEFAULT '')")

        if self.verbose:
            print 'END INIT USERS TABLE'

    ''' initialize sender table
        in relation 1 to n with user table
    '''
    def initSender(self):

        with self.con:

            cur = self.con.cursor()
            cur.execute("DROP TABLE IF EXISTS sender")
            cur.execute('CREATE TABLE sender ('
                        'id INTEGER PRIMARY KEY, '
                        'id_user INTEGER NOT NULL, '
                        'email CHAR(50), '
                        'name CHAR(50), '
                        'FOREIGN KEY(id_user) REFERENCES user(id) ON DELETE CASCADE)')

    def initusermails(self):

        with self.con:

            cur = self.con.cursor()
            cur.execute("DROP TABLE IF EXISTS user_mail")
            cur.execute('CREATE TABLE user_mail ('
                        'id INT NOT NULL, '
                        'uid INT NOT NULL, '
                        'PRIMARY KEY(id, uid), '
                        'FOREIGN KEY(id) REFERENCES user(id) ON DELETE CASCADE)')

    def initsendermails(self):

        with self.con:

            cur = self.con.cursor()
            cur.execute("DROP TABLE IF EXISTS sender_mail")
            cur.execute('CREATE TABLE sender_mail ('
                        'id INT NOT NULL, '
                        'userid INT NOT NULL, '
                        'isparsed INT DEFAULT 0, '
                        'uid INT NOT NULL, '
                        'PRIMARY KEY (id, userid, uid), '
                        'FOREIGN KEY(id) REFERENCES sender(id) ON DELETE CASCADE, '
                        'FOREIGN KEY(userid) REFERENCES user(id) ON DELETE CASCADE)')

    ''' initalize approved words table '''
    def initknowledge(self):

        with self.con:

            cur = self.con.cursor()
            cur.execute("DROP TABLE IF EXISTS knowledge")
            cur.execute('CREATE TABLE knowledge ('
                        'chunk TEXT NOT NULL,'
                        'found TEXT NOT NULL, '
                        'category TEXT,'
                        'url TEXT, '
                        'disambiguation_url INT DEFAULT 0, '
                        'ngram INT DEFAULT 1, '
                        'PRIMARY KEY (chunk, found)) ')

    def inituserdata(self):

        with self.con:

            cur = self.con.cursor()
            cur.execute("DROP TABLE IF EXISTS userdata")
            cur.execute('CREATE TABLE userdata ('
                        'userid INTEGER NOT NULL,'
                        'senderid INTEGER NOT NULL,'
                        'chunk TEXT NOT NULL,'
                        'found TEXT NOT NULL, '
                        'status INT, '
                        'score INT DEFAULT 0, '
                        'PRIMARY KEY (userid, senderid, chunk), '
                        'FOREIGN KEY(userid) REFERENCES user(id) ON DELETE CASCADE,'
                        'FOREIGN KEY(senderid) REFERENCES sender(id) ON DELETE CASCADE,'
                        'FOREIGN KEY(chunk) REFERENCES knowledge(chunk) ON DELETE CASCADE) ')

    def inittriggers(self):

        with self.con:

            cur = self.con.cursor()

            ## trigger for INSERT in USERDATA
            cur.execute("""CREATE TRIGGER t1
                BEFORE INSERT ON userdata
                 WHEN NEW.chunk IN (SELECT chunk FROM userdata WHERE userid=NEW.userid AND senderid=NEW.senderid)
                 BEGIN
                    UPDATE userdata
                     SET score=COALESCE(NEW.score, 0)+COALESCE((SELECT score
                                                                FROM userdata
                                                                WHERE userid=NEW.userid
                                                                    AND senderid=NEW.senderid
                                                                    AND chunk=NEW.chunk), 0)
                     WHERE chunk=NEW.chunk;
                    SELECT RAISE(IGNORE);
                 END""")

            '''cur.execute("""CREATE TRIGGER t3
                AFTER INSERT ON userdata FOR EACH ROW
                WHEN (SELECT url FROM knowledge WHERE chunk = NEW.chunk LIMIT 1) = ''
                BEGIN
                    UPDATE userdata
                    SET status = 2
                    WHERE chunk = NEW.chunk;
                END""")'''

            '''cur.execute("""CREATE TRIGGER t4
                AFTER INSERT ON userdata FOR EACH ROW
                WHEN (SELECT COUNT(chunk) FROM knowledge WHERE chunk = NEW.chunk) != 1
                BEGIN
                    UPDATE userdata
                    SET found = 'ambiguous', status = 0
                    WHERE chunk = NEW.chunk;
                END""")'''

    ''' initalize all tables and download NLTK data'''
    def initAll(self):

        if self.verbose:
            print 'START INIT ALL TABLES'

        self.initUsers()
        self.initusermails()
        self.initSender()
        self.initsendermails()
        self.inituserdata()
        self.initknowledge()
        self.inittriggers()

        if self.verbose:
            print 'END INIT ALL TABLES'









