__author__ = 'matteo'

from kivy.app import App
import os.path
import nltk
import time
from threading import Thread

class DwnThread(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=False):
        Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=None)

        self.args = args
        self.kwargs = kwargs
        self.verbose = verbose
        self.app = App.get_running_app()
        self.path = self.app.user_data_dir
        self.nltk_dir = 'nltk_data'

    def run(self):

        if self.verbose:
            print 'DWN THREAD START'

        popup = self.kwargs['parent']

        packages = ['stopwords', 'wordnet', 'punkt', 'maxent_treebank_pos_tagger']
        directory = self.path + '/' + self.nltk_dir

        downloader = nltk.downloader.Downloader(download_dir=directory)

        downloader.download(packages[0])
        self.app.root.pb_nltk_value = 25 #only set the progressbar to MAX

        downloader.download(packages[1])
        self.app.root.pb_nltk_value = 50 #only set the progressbar to MAX

        downloader.download(packages[2])
        self.app.root.pb_nltk_value = 75 #only set the progressbar to MAX

        downloader.download(packages[3])
        self.app.root.pb_nltk_value = 100 #only set the progressbar to MAX

        nltk.data.path.append(directory)

        time.sleep(1)
        popup.dismiss() #close the popup

