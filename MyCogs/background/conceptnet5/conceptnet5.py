__author__ = 'matteo'

import urllib
from kivy.network.urlrequest import UrlRequest
from background.db.manager import Manager
from kivy.app import App

class ConceptNet5:

    BASE_LOOKUP_URL = 'http://conceptnet5.media.mit.edu/data/5.2'
    BASE_SEARCH_URL = 'http://conceptnet5.media.mit.edu/data/5.2/search'
    BASE_ASSOCIATION_URL = 'http://conceptnet5.media.mit.edu/data/5.2/assoc'

    def __init__(self, limit=5, rel='/r/IsA'):

        self.limit = limit
        self.rel = rel
        self.db = Manager()
        self.app = App.get_running_app()

        self.query_args = {}
        self.query_args['text'] = ''
        self.query_args['limit'] = self.limit
        self.query_args['rel'] = self.rel
        self.text = ''

    def search(self, text):

        '''
        function to start the process of categories retrieval
        I use an async request by the UrlRequest method provided by kivy
        :param text:
        :return:
        '''

        self.query_args['text'] = text.encode('ascii', 'ignore')
        self.text = text
        self.encoded_query_args = urllib.urlencode(self.query_args)
        url = ''.join(['%s%s' % (self.BASE_SEARCH_URL, '?')]) + self.encoded_query_args
        #print 'URL: ', url
        request = UrlRequest(url, self.found_categories)

    def found_categories(self, request, data):

        '''
        Callback function called after http response
        :param request:
        :param data:
        :return:
        '''

        res = ''

        if data['numFound'] != 0:

            cat = []
            for idx, node in enumerate(data['edges']):

                if node['end'][6:] != self.text:
                    cat.append(node['end'][6:].encode('utf-8', 'ignore'))

            res = ", ".join(cat)

        self.db.update_cat(chunk=self.text, cat=res)

    ###########################################################################

    def search_nofill(self, text):

        self.query_args['text'] = text.encode('ascii', 'ignore')
        self.text = text
        self.encoded_query_args = urllib.urlencode(self.query_args)
        url = ''.join(['%s%s' % (self.BASE_SEARCH_URL, '?')]) + self.encoded_query_args
        request = UrlRequest(url, self.found_categories_nofill)

    def found_categories_nofill(self, request, data):

        res = ''

        if data['numFound'] != 0:

            cat = []
            for idx, node in enumerate(data['edges']):

                if node['end'][6:] != self.text:
                    cat.append(node['end'][6:].encode('utf-8', 'ignore'))

            res = ", ".join(cat)

        self.app.root.foundslide.new_category.text = res

    ###########################################################################

    def search_edit(self, text):

        self.query_args['text'] = text.encode('ascii', 'ignore')
        self.text = text
        self.encoded_query_args = urllib.urlencode(self.query_args)
        url = ''.join(['%s%s' % (self.BASE_SEARCH_URL, '?')]) + self.encoded_query_args
        request = UrlRequest(url, self.found_categories_edit)

    def found_categories_edit(self, request, data):

        print request
        print data
        res = ''

        if data['numFound'] != 0:

            cat = []
            for idx, node in enumerate(data['edges']):

                if node['end'][6:] != self.text:
                    cat.append(node['end'][6:].encode('utf-8', 'ignore'))

            res = ", ".join(cat)

        self.app.root.editslide.category.text = res







