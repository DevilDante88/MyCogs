__author__ = 'Matteo Renzi'

import nltk
import string
import re
from nltk.tag import tnt
from nltk.tag import DefaultTagger
from nltk.corpus import treebank
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.metrics import TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from kivy.app import App

from background.textprocessing.replacers import RegexpReplacer


''' this Class elaborate text obtaing POS tags '''
class PosTagger:

    def __init__(self, text='', verbose=False):
        self.text = text
        self.verbose = verbose

        #train set to be used in the TnT pos tagging
        #print 'start training TnT pos tagger'
        #train_sents = treebank.tagged_sents()[:3000]
        #unk = DefaultTagger('NN')
        #self.tnt_tagger = tnt.TnT(unk=unk, Trained=True)
        #self.tnt_tagger.train(train_sents)
        #print 'end training TnT pos tagger'

        self.app = App.get_running_app()
        self.tokenizer = RegexpTokenizer("\s+", gaps=True)

    def setText(self, text):

        """
        set the text inside the class and check if is string
        """

        if isinstance(text, basestring):
            self.text = text
            return True
        else:
            return False

    def getSimpleTag(self, text):

        """
        retrieve the pos tag list
        :param text:
        :return:
        """

        if self.setText(text):
            # eliminate english contraction
            regr = RegexpReplacer()
            self.text = regr.replace(self.text)
            # sentence segmenter
            sentences = nltk.sent_tokenize(self.text)
            # word segmenter
            #sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [self.tokenizer.tokenize(sent) for sent in sentences]
            # prefiltering to join bad tokenized words (like emails or url)
            sentences = self.prefiltering(sentences)
            # pos tagging
            try:
                sentences = [self.app.root.tnt_tagger.tag(sent) for sent in sentences]
            except AttributeError:
                print 'postagger non pronto'


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

    def prefiltering(self, sentences):

        """
        prefiltering function to deal with particular words:
        - emails
        - links
        - special character
        - punctuation
        it union token that must be treated as a single entity
        :param sentences:
        :return:
        """

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





