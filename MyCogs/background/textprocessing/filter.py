__author__ = 'Matteo Renzi'

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.chunk import RegexpParser

'''
class for filter the chunked tree
'''
class Filter:

    def __init__(self, verbose=False):
        self.bad_tag = ['DT', 'CC', 'VB', 'IN', 'VBG', 'VBP', 'TO']
        self.good_tag = ['NN', 'NNS', 'JJ', 'NNP']
        self.verbose = verbose
        self.wnl = WordNetLemmatizer()   #istance of the stemmer based on WordNet English vocabulary
        self.english_stop = set(stopwords.words('english'))  #set of english stopwords

        #grammar used for chunking
        self.grammar = r"""
                          NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
                          PP: {<IN><NP>}               # Chunk prepositions followed by NP
                          VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
                          CLAUSE: {<NP><VP>}           # Chunk NP, VP
                          """
        self.cp = RegexpParser(self.grammar, loop=2)

    ''' retrieve the chunked tree for a single sentence '''
    def getChunkedTree(self, sent):

        if self.verbose:
            print 'CHUNCKED TREE: ', self.cp.parse(sent)
        return self.cp.parse(sent)

    ''' set the list of unwanted tag '''
    def setNAtags(self, tag_suffixes):
        self.bad_tag = tag_suffixes

    ''' get the list of unwanted tag '''
    def getNAtags(self):
        return self.bad_tag

    ''' set the list of approved tag '''
    def setAtags(self, tag_suffixes):
        self.good_tag = tag_suffixes

    ''' get the list of approved tag '''
    def getAtags(self):
        return self.good_tag

    def traverse(self, t):

        """
        traverse a tree, obatin NP
        subtrees: Generate all the subtrees of this tree, optionally restricted to trees matching the filter function.
        height: The height of this tree.  The height of a tree containing no children is 1;
        the height of a tree containing only leaves is 2;
        and the height of any other tree is one plus the maximum of its children's heights.
        :param t:
        :return:
        """

        good = []

        for s in t.subtrees(lambda t: t.height() == 2):
            good.append(s.leaves())

        return good

    ''' from the pos tagger tag retrieve the wordnet one
        NN -> n
        JJ -> a
    '''
    def getWordnetTag(self, tag):

        return {
            'NN': 'n',
            'NNP': 'n',
            'JJ': 'a'
        }.get(tag, 'n')

    '''
    filter a NP to extract significat nouns
    '''
    def filter_insignificant(self, data):

        filtered = []

        # parse a single NP
        for np in data:
            good = []

            #parse a single chunk
            for word, tag in np:

                #check if it is a not desired tag
                if tag in self.good_tag:

                    # filtering stopwords and words long less than 3
                    if word in self.english_stop or (len(word) < 3):
                        continue

                    word = word.lower()

                    #stemming (Wnl Lemmatizer) enhanched with the specific type of tag
                    word = self.wnl.lemmatize(word, pos=self.getWordnetTag(tag))

                    if len(word) > 2:
                        good.append((word, tag))

            # add the list only if not empty
            if len(good) > 0:
                filtered.append(good)

        if self.verbose:
            print 'After filter_insignificant'
            print filtered

        return filtered


















