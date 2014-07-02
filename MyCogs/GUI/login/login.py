__author__ = 'matteo'

import os.path
import nltk

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from GUI.progressbar.progressbar_login import LoginPopup
from GUI.progressbar.progressbar_dwnnltk import DwnPopup

from kivy.app import App
from kivy.lang import Builder

Builder.load_file('GUI/login/login.kv')

class Login(BoxLayout):

    def __init__(self, verbose=False, **kwargs):

        super(Login, self).__init__(**kwargs)

        self.id = 'login'
        self.app = App.get_running_app()
        self.verbose = verbose
        self.path = self.app.user_data_dir
        self.nltk_dir = 'nltk_data'

    ''' check if the NLTK folder is present in the userdata '''
    def check_install(self):

        if os.path.exists(self.path + '/' + self.nltk_dir):
            if self.verbose:
                print 'nltk data found'
            nltk.data.path.append(self.path + '/' + self.nltk_dir)
            self.login()
        else:
            if self.verbose:
                print 'nltk data not found, start downloading'
            os.makedirs(self.path + '/' + self.nltk_dir)
            self.show_popup_dwn()   ##start the popup and the download data thread

    ''' fuction to start login in the account '''
    def login(self, *args):

        email = self.ids.email.text
        pwd = self.ids.pwd.text

        self.show_popup(email, pwd)

        #do the login and check how many mails to parse

    ''' popup for nltk download data '''
    def show_popup_dwn(self):

        p = DwnPopup()
        p.bind(on_dismiss=self.callback_nltk)
        p.open()

    def show_popup(self, email, pwd):

        p = LoginPopup(email, pwd)
        p.bind(on_dismiss=self.callback_login)
        p.open()

    def callback_nltk(self, instance):

        print('Popup', instance, 'is being dismissed')
        self.login()

    def callback_login(self, instance):

        if instance.status != "OK":
            popup = Popup(title='ERROR!!', content=Label(text=instance.status),
                          size_hint=(None, None), size=(400, 200))
            popup.bind(on_dismiss=self.callback_error)
            popup.open()
            return
        app = App.get_running_app()
        app.root.carousel.load_slide(app.root.senderlist)
        return False

    def callback_error(self, instance):

        app = App.get_running_app()
        app.root.carousel.load_slide(app.root.login)

