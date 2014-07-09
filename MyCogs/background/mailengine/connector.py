__author__ = 'Matteo Renzi'

import imaplib
import email

'''
Class for the connection to an mail IMAP account.
'''
class Connector:

    def __init__(self, imap_host = 'imap.gmail.com', verbose=False):
        self.imap_host = imap_host
        self.user = ''
        self.pwd = ''
        self.imap = None
        self.messagesID = ()    ##empty set of message ID
        self.verbose = verbose

    def setuser(self, user):
        self.user = user

    def getuser(self):
        return self.user

    def setpwd(self, pwd):
        self.pwd = pwd

    def getpwd(self):
        return self.pwd

    ''' function to connect to the selected imap host with SSL connection '''
    def connect(self):
        ''' open a connection '''

        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_host)
            if self.verbose:
                print 'EMAIL CONNECTION: OK'
            return True
        except imaplib.IMAP4.error:
            print "Gmail connection failed."
            return False

    ''' function to login with user data '''
    def login(self, user, password):
        ''' login '''

        self.user = user
        self.pwd = password

        try:
            self.imap.login(self.user, self.pwd)
            if self.verbose:
                print 'EMAIL LOGIN: OK'
            return True
        except imaplib.IMAP4.error:
            print "Log in failed."
            return False

    ''' retrieve the folders list '''
    def getFolderslist(self):
        ''' retrieve the folders list '''

        status, folders_list = self.imap.list()
        if self.verbose:
            print 'Folder list: ', folders_list
        return status, folders_list

    ''' set the folder where we are interested, default INBOX '''
    def setFolder(self, folder='INBOX'):
        ''' select a specific folder, default is selected INBOX '''

        try:
            status, data = self.imap.select(folder)
        except imaplib.IMAP4.error as e:
            print 'Set Folder failed, ', e

        return status, data

    ''' search for a particular list of emails '''
    def search(self, area, value):
        '''
            type can be SUBJECT, FROM, TO

            @return: a list of ID of corresponding mails
        '''
        ids = []

        if self.verbose:
            print 'EMAIL SEARCH for: ', area, 'value: ', value

        ## searching current folder using title keywords
        status, ids = self.imap.search(None, area, '"' + value + '"')

        return status, ids[0].split()

    ''' retrieve all emails '''
    def searchAll(self):
        '''
            retrieve all ID messages
        '''

        #searching current folder using title keywords
        status, ids = self.imap.search(None, 'ALL')

        return status, ids[0].split()

    ''' retrieve the list of UID with that subject '''
    def getUID(self, subject):

        status, data = self.imap.uid('search', None, '(HEADER Subject ' + subject + ')')

        datastring = data[0].split(' ')
        return [int(x) for x in datastring]

    ''' get sender '''
    def getSender(self, id, IDtype='id'):

        if IDtype == 'id':
            return self.getSenderID(id)
        else:
            return self.getSenderUID(id)


    ''' get sender from ID '''
    def getSenderID(self, id):

        status, sender = self.imap.fetch(id, "(BODY[HEADER.FIELDS (FROM)])")

        test = sender[0][1]
        #eliminate the From: and the newline at the end with the function rstrip()
        if self.verbose:
            print 'get SENDER: ', test[6:].rstrip()
        return test[6:].rstrip()

    ''' get sender from UID '''
    def getSenderUID(self, uid):

        status, sender = self.imap.uid('FETCH', uid, '(BODY.PEEK[HEADER.FIELDS (FROM)])')

        test = sender[0][1]
        #eliminate the From: and the newline at the end with the function rstrip()
        if self.verbose:
            print 'get SENDER: ', test[6:].rstrip()
        return test[6:].rstrip()


    ''' get message in raw text, exclude multipart form data
        @param: message ID or message UID
        @param: select the type of ID passed 0-id, 1-uid
    '''
    def getMessage(self, id, IDtype = 'uid'):

        body = ''

        typ = None
        data = None

        if IDtype == 'id':
            typ, data = self.imap.fetch(id, '(RFC822)')
        else:
            result, data = self.imap.uid('fetch', id, '(RFC822)')

        #puts message from list into string
        raw_email = data[0][1]
        # converts string to instance of message xyz is an email message so multipart and walk work on it.
        msg_string = email.message_from_string(raw_email)

        #Finds the plain text version of the body of the message.
        if msg_string.get_content_maintype() == 'multipart':
            #If message is multi part we only want the text version of the body, this walks the message and gets the body.
            for part in msg_string.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    break
                else:
                    continue
        else:
            #If message is not multi-part we directly retrieve the body
            body = msg_string.get_payload(decode=True)

        return body

    ''' close the connection '''
    def close(self):
        '''
        close the connection with the email server
        '''
        self.imap.close()
        self.imap.logout()
















