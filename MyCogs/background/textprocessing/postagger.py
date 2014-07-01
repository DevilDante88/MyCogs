__author__ = 'matteo'

import nltk
import string
import re
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.metrics import TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from background.textprocessing.replacers import RegexpReplacer


''' this Class elaborate text obtaing POS tags '''
class PosTagger:

    def __init__(self, text='', verbose=False):
        self.text = text
        self.verbose = verbose
        pattern = r'''(?x)    # set flag to allow verbose regexps
                 ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
          | \w+(-\w+)*        # words with optional internal hyphens
          | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
          | \.\.\.            # ellipsis
          | [][.,;"'?():-_`]  # these are separate tokens
    '''

        self.tokenizer = RegexpTokenizer("\s+", gaps=True)

    ''' set the text inside the class and check if is string '''
    def setText(self, text):
        '''
        set mail text
        '''
        if isinstance(text, basestring):
            self.text = text
            return True
        else:
            return False

    ''' retrieve the pos tag list '''
    def getSimpleTag(self, text):

        if self.setText(text):
            # eliminate english contraction
            regr = RegexpReplacer()
            self.text = regr.replace(self.text)
            # sentence segmenter
            sentences = nltk.sent_tokenize(self.text)
            # word segmenter
            #sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [self.tokenizer.tokenize(sent) for sent in sentences]
            # prefiltering to join bad tokenized words
            sentences = self.prefiltering_v2(sentences)
            # pos tagging
            sentences = [nltk.pos_tag(sent) for sent in sentences]

            if self.verbose:
                print 'POSTAG SENTENCE: ', sentences
            return sentences

        else:
            print 'ERROR: data in getTags not a string'
            return []

    def getBigrams(self):

        words = [w.lower() for w in nltk.word_tokenize(self.text)]
        bcf = BigramCollocationFinder.from_words(words)
        stopset = set(stopwords.words('english'))
        filter_stops = lambda w: len(w) < 3 or w in stopset
        bcf.apply_word_filter(filter_stops)
        return bcf.nbest(BigramAssocMeasures.likelihood_ratio, 4)

    def getTrigrams(self):

        words = [w.lower() for w in nltk.word_tokenize(self.text)]
        tcf = TrigramCollocationFinder.from_words(words)
        stopset = set(stopwords.words('english'))
        filter_stops = lambda w: len(w) < 3 or w in stopset
        tcf.apply_word_filter(filter_stops)
        tcf.apply_freq_filter(1)
        return tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 6)

    ''' prefiltering function to deal with particular words:
        - emails
        - links
        - special character
        - punctuation
        it union token that must be treated as a single entity
    '''
    def prefiltering(self, sentences):

        # filtering with regular expressing
        regex = re.compile(r'[\!\?\-\(\)\,\"]*')    #regular expression for special character
        regex1 = re.compile(r'\w*\s*@\s*\w*')   #regular expression for emails
        regex2 = re.compile(r'[\.\:\/]*')           #regular expression for punctuation
        regex3 = re.compile(r'http*')           #regular expression for hyperlink

        good = []
        for sent in sentences:
            sent2 = []
            for token in sent:

                token = regex.sub('', token)

                if regex1.search(token) or regex3.search(token):
                    sent2.append(token)
                else:
                    token = regex2.sub('', token)
                    if len(token) > 0:
                        sent2.append(token)

            good.append(sent2)

        return good


    def prefiltering_v2(self, sentences):

        # filtering with regular expressing
        regex = re.compile(r'[\<\>\[\]\!\?\-\(\)\,\"]*')    #regular expression for special character not for url
        regex2 = re.compile(r'[\<\>\[\:\/\]\!\?\-\(\)\,\"]*')    #regular expression for special character not for url

        mail = re.compile(r'\w*\s*@\s*\w*')   #regular expression for emails
        url = re.compile(r'http*')           #regular expression for hyperlink
        r = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))

        good = []
        for sent in sentences:
            sent2 = []
            for token in sent:
                # if http
                if url.search(token):
                    # elimination special character
                    sent2.append(regex.sub('', token))
                # if email
                elif mail.search(token):
                    # elimination special character
                    sent2.append(regex2.sub('', token))
                else:
                    #if a normal token delete punctuation at the begging or end
                    token = token.strip(string.punctuation)
                    token = r.split(token)
                    for t in token:
                        sent2.append(t)

            good.append(sent2)

        return good





