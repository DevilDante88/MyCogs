__author__ = 'matteo'

import time
from threading import Thread

from background.db.manager import Manager
from background.conceptnet5.conceptnet5 import ConceptNet5
from wikipedia.WikiConnector import WikiConnector

from kivy.app import App

class AddThread(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=False):
        Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=None)
        self.args = args
        self.kwargs = kwargs
        self.app = App.get_running_app()
        self.meaning = {}
        self.db = None
        self.wiki = WikiConnector(verbose=False)
        self.conceptnet = ConceptNet5()

    def run(self):

        """
        Run cycle for AddThread
        :return:
        """
        self.meaning = {}
        chunk = self.kwargs['chunk']
        popup = self.kwargs['parent']

        self.app.root.pb_add_value = 0

        self.db = Manager()

        # get list of possible meanings, url and disambiguation status
        self.getmeaning(chunk)

        self.app.root.pb_add_value = 50

        ## query conceptnet for categories (it will set result on the ui)
        categories = self.conceptnet.search_nofill(chunk.lower().encode('utf8'))

        self.app.root.pb_add_value = 100

        #store data in the foundslide
        self.app.root.foundslide.meaning = self.meaning
        #self.app.root.foundslide.new_category.text = categories
        self.app.root.foundslide.new_chunk.text = chunk

        time.sleep(0.5)
        popup.dismiss()

        return

    ###########################################################################################
    ## FUNCTION MEANING RESEARCH
    ###########################################################################################

    ''' function to retrieve the meaning '''
    def getmeaning(self, phrase):

        ngram = phrase.split(' ')

        # check if present in DB knowledge
        if len(self.db.existchunk_kl(phrase)) > 0:

            rows = self.db.getchunk_kl(phrase)
            for val in rows:
                self.meaning[val.found] = [val.url, val.disambiguation_url]
            return

        # chunk not present in the DB, check wikipedia
        else:

            ## query wikipedia to obtain meanings
            best = []
            if len(ngram) > 1:
                best = self.wiki.searchphrase(phrase)
            else:
                best = self.wiki.searchword(phrase)

            for found in best:

                url, dis = self.wiki.geturl(found)
                ## update hashtable
                self.meaning[found] = [url, dis]
                return
