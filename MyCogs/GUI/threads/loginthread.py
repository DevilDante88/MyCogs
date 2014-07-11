__author__ = 'Matteo Renzi'

import re
import time
from threading import Thread

from background.mailengine.messageretriever import MessageRetriever
from background.db.manager import Manager

from kivy.app import App
from kivy.uix.popup import Popup


class LoginThread(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=False):
        Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=None)
        self.args = args
        self.kwargs = kwargs
        self.mr = MessageRetriever()
        self.db = None
        self.verbose = verbose
        self.email = ''
        self.pwd = ''
        self.rx = re.compile('\W+')
        self.status = 'OK'

        self.app = App.get_running_app()    #app instance

        return

    ###########################################################################################
    ## RUN
    ###########################################################################################

    def run(self):

        self.app.root.pb_login_value = 0

        self.email = self.kwargs['email']
        self.app.root.pwd = self.kwargs['pwd']
        popup = self.kwargs['parent']
        popup.status = 'OK'

        #necessary to create a connecton to DB inside the thread
        self.db = Manager(self.verbose)

        #do the login
        uids = self.loginGUI()

        if self.status != 'OK':
            popup.status = self.status
            popup.dismiss()

        if len(uids) != 0:
            #append new UID to the user table as "readed"
            self.db.add_user_mail(self.app.root.userID, uids)

            #update the list of senders
            self.update_senders(uids)
        else:
            #do NOT update the user table
            #do NOT update the sender list
            for x in range(101):
                time.sleep(0.005)
                self.app.root.pb_login_value = x #only set the progressbar to MAX

        time.sleep(0.5)
        popup.dismiss() #close the popup

    ###########################################################################################

    ''' check the correct format of an email '''
    def checkEmail(self, email):

        if re.match(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return True
        else:
            return False

    ''' manage all the login process.
    1) check new mails with subject ingest
    2) retrieve all uids for that mails
    3) get the user ID or create a new one
    4) set uids for that user
    '''
    def loginGUI(self):

        if self.checkEmail(self.email):

            self.mr.connect()
            if self.mr.login(self.email):
                self.mr.setFolder()

                #retrieve the list of IDs for that user account
                new_uid = self.mr.getUID('ingest')

                #check if user is present in the DB, or create a new one
                user_id = self.db.getUserID(self.email)

                #add user ID to the global variables
                self.app.root.userID = user_id

                if self.verbose:
                    print 'USER ID: ', user_id

                #get list of readed messages
                old_uid = self.db.getuser_mail(user_id)

                data_to_add = []
                if len(old_uid) == 0:
                    data_to_add = new_uid
                else:
                    old_uid = [x.uid for x in old_uid]
                    data_to_add = [x for x in new_uid if x not in old_uid]

                if self.verbose:
                    print 'NEW DATA: ', new_uid
                    print 'OLD DATA: ', old_uid
                    print 'DATA TO ADD: ', data_to_add

                #the new data not already in the DB
                return data_to_add

            else:
                self.status = 'login failed, check your email and password'
                return []

        else:
            self.status = 'ERROR: incorrect email format'
            return []

    '''
    class for manage the sender table
    5) parse sender and create or update sender if necessary
    6) set unparsed uid to sender
    '''
    def update_senders(self, uids):

        if self.verbose:
            print 'UPDATE SENDERS & UID'
            print 'TOTAL UIDS to ADD: ', len(uids)

        self.mr.connect()
        if self.mr.login(self.email):
            self.mr.setFolder()

            #parse new uids
            for index, uid in enumerate(uids):

                name = ''
                email = ''

                #retrive the original sender for each email
                sender = self.mr.getSender(uid, IDtype='uid')

                #parse the sender and divide, if exist the name by the mail
                match = re.search(r'[\w\.-]+@[\w\.-]+', sender)

                if match is None:
                    name = sender
                else:
                    email = match.group(0)
                    name = [x for x in sender.split() if not re.search(r'[\w\.-]+@[\w\.-]+', x)]
                    name = ' '.join(name)

                name = self.rx.sub(' ', name).strip()

                if self.verbose:
                    print 'UID: ', uid
                    print 'NAME: ', name
                    print 'EMAIL: ', email

                #now check the sender (creates one if is not present)
                id_sender = self.db.getSenderID(self.app.root.userID, email, name)

                #add the uid to the sender unparsed uids
                self.db.addsender_mail(userid=self.app.root.userID, id=id_sender, uid=uid)

                self.app.root.pb_login_value = (100 * (index + 1)) / len(uids)
                if self.verbose:
                    print 'PROGRESSBAR: ', (100 * (index + 1)) / len(uids)

            return True

        else:
            print 'login failed'

        return False






