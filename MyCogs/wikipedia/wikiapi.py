__author__ = 'Matteo Renzi'

import wikipedia
from background.textprocessing import cosine
import collections
from collections import defaultdict

class Wikiapi:

    '''
    Class that provides a connection to Wikipedia
    '''

    def __init__(self, verbose=False):

        self.phrase = ''
        self.verbose = verbose

    def getsummary(self, phrase):

        '''
        return the summary (provided by wikipedia) of a particural phrase
        particular attention has to be provided when we have to deal with a Disambiaguation of a phrase
        '''

        try:
            # encode in UTF-8 for wikipedia compatibility
            summary = wikipedia.summary(phrase)

        except wikipedia.DisambiguationError as e:
            # particular case where our phrase has a disambiguation
            #TODO catch the disambiguation problem and with a WSD find the correct link
            print 'WIKIPEDIA DISAMBIGUATION PAGE:', e.options
            return e.options

        except wikipedia.PageError as e:
            print 'WIKIPEDIA PAGE ERROR: ', e
            return e

        return summary.encode('utf-8')

    def searchphrase(self, phrase):

        '''
        return the suggested phrase by Wikipedia
        to filter the suggested phrase, I apply a cosine similarity in a vector space model
        between sentences to take off different words
        '''

        decided = []

        # else search for other possibilities, limit to 5 for performance
        suggested = wikipedia.search(phrase, results=5)
        d = defaultdict(list)

        for s in suggested:

            cos = cosine.get_cosine(phrase.lower(), s.encode('utf-8').lower())
            #add to dictionary
            d[cos].append(s.encode('utf-8').lower())

        # if dictionary is empty, return an empty list
        if len(d) == 0:
            return decided

        # reorder the dictionary and find the one with the best value
        od = collections.OrderedDict(sorted(d.items()))
        key = next(reversed(od))

        #retrive key only if greater than value
        if key > 0.70:
            decided.extend(od[key])

        return list(set(decided))

    def searchword(self, phrase):

        """
        return the suggested meaning from Wikipedia
        this function is used for a single word and returns the first result from Wikipedia
        :param phrase:
        :return:
        """

        # else search for other possibilities, limit to 3 for performance
        suggested = wikipedia.search(phrase, results=2)

        if len(suggested) > 0:
            if suggested[0].lower() == phrase:
                return suggested[:1]
            else:
                return suggested
        else:
            return []

    def geturl(self, phrase):

        '''
        return the url (if exist) of a noun, and also an integer that represent
        if that url is a disambiguation url or not
        :param phrase:
        :return: url, disambiguation
        '''
        url = ''

        try:
            url = wikipedia.page(phrase).url

        except wikipedia.DisambiguationError as e:
            # particular case where our phrase has a disambiguation
            #TODO catch the disambiguation problem and with a WSD find the correct link
            print 'WIKIPEDIA DISAMBIGUATION PAGE:', e.options
            return "http://en.wikipedia.org/wiki/" + phrase.replace(" ", "_"), 1

        except wikipedia.PageError as e:
            print 'WIKIPEDIA PAGE ERROR: ', e
            return '', 0

        except TypeError:
            print 'ERROR: type error wikipedia geturl'
            return '', 0

        except KeyError:
            print 'ERROR: keyerror'
            return '', 0

        return url, 0



