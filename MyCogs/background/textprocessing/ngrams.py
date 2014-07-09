__author__ = 'Matteo Renzi'

from nltk import bigrams
from nltk import trigrams

class NgramsFilter:

    def __init__(self, verbose=False):

        self.verbose = verbose

    ''' extract a list of trigrams from a filtered sentence '''
    def getTrigrams(self, filtered_data):

        good = []

        # for every np
        for np in filtered_data:

            # if np contains only 2 element, skip
            if len(np) > 2:
                words = [word[0] for word in np]
                good.append(trigrams(words))
        if self.verbose:
            print 'TRIGRAMS: ', good
        return good

    ''' extract a list of bigrams from a filtered sentence '''
    def getBigrams(self, filtered_data):

        good = []

        # for every np
        for np in filtered_data:

            # if np contains only 1 element, skip
            if len(np) > 1:
                words = [word[0] for word in np]
                good.append(bigrams(words))
        if self.verbose:
            print 'BIGRAMS: ', good

        return good

    ''' extract a list of trigrams/bigrams from a filtered sentence '''
    def getBestngrams(self, filtered_data):

        good = []

        # for every np
        for np in filtered_data:

            # if np contains only 1 element, skip
            if len(np) > 2:
                words = [word[0] for word in np]
                good.extend(trigrams(words))
            elif len(np) == 2:
                words = [word[0] for word in np]
                good.extend(bigrams(words))
            else:
                continue

        if self.verbose:
            print 'NGRAMS: ', good

        return good

    ''' check if the passed ngram in avaible in our table '''
    def isavaible(self, ngram):

        ##TODO access our dataset of ngrams to check if the passed ngram is avaible

        ##TODO I need the sender and user id

        pass
