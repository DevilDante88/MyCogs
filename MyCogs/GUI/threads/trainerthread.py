__author__ = 'matteo'

from kivy.app import App
from threading import Thread

from nltk.tag import tnt
from nltk.tag import DefaultTagger
from nltk.corpus import treebank


class TrainerThread(Thread):

    """
    Thread that will train the tnt pos tagger.
    it will be used in the text processing
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=False):
        Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=None)

    def run(self):

        app = App.get_running_app()

        print 'start training TnT pos tagger'
        train_sents = treebank.tagged_sents()[:2000]
        unk = DefaultTagger('NN')
        app.root.tnt_tagger = tnt.TnT(unk=unk, Trained=True)
        app.root.tnt_tagger.train(train_sents)
        print 'end training TnT pos tagger'
