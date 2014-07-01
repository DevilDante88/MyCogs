__author__ = 'matteo'

from background.mailengine.connector import Connector
import mmap
from StringIO import StringIO

'''
        Connector class with a function to manipulate forwarded emails.
        If it finds that the selected emails is a forwarded one, it clean the text and retrieve as
        sender the original one
'''


class MessageRetriever(Connector):
    def __init__(self, imap_host='imap.gmail.com'):
        Connector.__init__(self, imap_host)


    ''' get the cleaned text corpus of the email '''

    def getMessage(self, id, IDtype='uid'):

        found = False
        good = []

        #if it finds that this is a forwarded email, must be cleaned the first 8 lines

        # firstly retrieve the entire message
        text = Connector.getMessage(self, id, IDtype)

        pos = text.find('Subject:')
        if pos:

            text = text[pos+8:]
            pos = text.find('\n')

            return text[pos+1:].decode('utf-8', errors='ignore')
        else:
            return text.decode('utf-8', errors='ignore')


    ''' get the Sender both if it's a forwarded or an original mail
        also compatible with preamble first of the forwarded message '''
    def getSender(self, id, IDtype='uid'):

        # firstly retrieve the entire message
        text = Connector.getMessage(self, id, IDtype)

        # now parse the message to check if it is a forwarded one
        if text.find('Forwarded by'):

            buf = StringIO(text)

            lookup = 'From: '
            while True:

                ln = buf.readline()
                if ln == '':
                    break
                if lookup in ln.strip('\n'):
                    return ln.strip('\n')[8:]


        else:
            # case this is not a forwarded message
            return Connector.getSender(id, IDtype)






