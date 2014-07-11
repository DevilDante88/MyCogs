__author__ = 'Matteo Renzi'
__version__ = 1.1

import nltk
import os
import shutil
from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty, NumericProperty, StringProperty)
from kivy.utils import platform

from GUI.login import login
from GUI.senderlist import senderlist
from GUI.approved import approved
from GUI.unapproved import unapproved
from GUI.undefined import undefined
from GUI.add import addslide
from GUI.add import foundslide
from GUI.edit import editslide

from GUI.progressbar.progressbar_dwnnltk import DwnPopup
from GUI.threads.trainerthread import TrainerThread

## Gotham font setting
from kivy.core.text import LabelBase
KIVY_FONTS = [
    {
        "name": "Gotham",
        "fn_regular": "data/fonts/Gotham-Light.ttf",
        "fn_bold": "data/fonts/Gotham-Black.ttf",
        "fn_italic": "data/fonts/Gotham-LightItalic.ttf",
        "fn_bolditalic": "data/fonts/Gotham-BlackItalic.ttf"
    }
]
for font in KIVY_FONTS:
    LabelBase.register(**font)


class MyCogsRoot(BoxLayout):

    '''
    Root class for the application, all kv files are loaded here.
    It manage the action bar and the carousel that keeps and load each slides
    '''

    #initialize global variables for sender and user ID and passoword
    userID = NumericProperty(0)
    senderID = NumericProperty(0)
    pwd = StringProperty('')

    current_chunk = StringProperty('')
    new_chunk = StringProperty('')

    carousel = ObjectProperty()
    approved = ObjectProperty()
    unapproved = ObjectProperty()
    undefined = ObjectProperty()
    senderlist = ObjectProperty()
    login = ObjectProperty()
    addslide = ObjectProperty()
    foundslide = ObjectProperty()

    tnt_tagger = ObjectProperty()

    pb_login_value = NumericProperty(0)   #login progressbar value
    pb_sender_value = NumericProperty(0)    #sender data progressbar value
    pb_sender_label = StringProperty('Loading Data...')
    pb_nltk_value = NumericProperty(0)  #nltk download progressbar value
    pb_add_value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MyCogsRoot, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def slide_update(self, value):

        """
        callback function each time the carousel changes the active slide
        :param value:
        """

        print 'slide current: ', value.id

        if value.id == 'senderlist':
            value.load_senders()

        elif value.id == 'approved':
            value.fill_table()

        elif value.id == 'unapproved':
            value.fill_table()

        elif value.id == 'undefined':
            value.fill_table()

        elif value.id == 'addslide':
            value.fill_data()

        elif value.id == 'foundslide':
            value.fill_data()

        elif value.id == 'editslide':
            value.fill_data()

    def menu_callback(self, instance):

        '''
        callback function for menu button, deal the particular case when no sender has been selected
        disable button in sender is not selected
        '''

        if instance.id == "approved":
            if self.app.root.senderID is 0:
                return
            else:
                self.app.root.carousel.load_slide(self.app.root.approved)

        elif instance.id == "unapproved":
            if self.app.root.senderID is 0:
                return
            else:
                self.app.root.carousel.load_slide(self.app.root.unapproved)

        elif instance.id == "undefined":
            if self.app.root.senderID is 0:
                return
            else:
                self.app.root.carousel.load_slide(self.app.root.undefined)

        elif instance.id == "senderlist":
            if self.app.root.userID is 0:
                return
            else:
                self.app.root.carousel.load_slide(self.app.root.senderlist)

    def logout(self):

        """
        logout function
        :return:
        """

        self.app.root.senderID = 0
        self.app.root.userID = 0
        self.app.root.pwd = ''
        self.app.root.senderlist.clear_widgets()

        self.app.root.login.ids.email.text = ''
        self.app.root.login.ids.pwd.text = ''
        self.app.root.carousel.load_slide(self.app.root.login)


class MyCogs(App):

    row_height = NumericProperty(100)

    def on_start(self):

        if platform == "linux" or platform == "win" or platform == "macosx":
            # linux
            # OS X
            # Windows...
            self._app_window.size = 1024, 768
            self._app_window.fullscreen = False

        self.row_height = int(self.config._sections['General']['row_height'])
        self.check_install()

    def on_pause(self):
        return True

    def build(self):

        self.icon = 'data/img/app-icon.png'
        self.settings_cls = SettingsWithSidebar

    def build_config(self, config):
        config.setdefaults('General', {'db_data': False, 'nltk_data': False, 'row_height': 100})

    def build_settings(self, settings):
        settings.add_json_panel("MyCogs", self.config, data="""
            [
                {
                    "type": "bool",
                    "title": "Clean DB",
                    "desc": "empty the DB, data can't be restored!!",
                    "section": "General",
                    "key": "db_data",
                    "true": "auto"
                },
                {
                    "type": "bool",
                    "title": "Clean NLTK data",
                    "desc": "empty the nltk data folder, data can't be restored!!",
                    "section": "General",
                    "key": "nltk_data",
                    "true": "auto"
                },
                {
                    "type": "numeric",
                    "title": "Row Height",
                    "desc": "standard dimension for GUI rows (may need to restart app)",
                    "section": "General",
                    "key": "row_height",
                    "true": "auto"
                }
            ]"""
            )

    def on_config_change(self, config, section, key, value):
        if config is self.config and key == "db_data":
            try:
                if int(value) == 1:
                    print 'cleaning DB'
                    os.remove(self.user_data_dir + '/' +'mycogs.sqlite3')
                    self.root.logout()
                    config._sections['General']['db_data'] = 0
            except AttributeError:
                pass
            except OSError:
                pass
        if config is self.config and key == "nltk_data":
            try:
                if int(value) == 1:
                    print 'cleaning NLTK DATA'
                    shutil.rmtree(self.user_data_dir + '/' + 'nltk_data')
                    self.root.logout()
                    config._sections['General']['nltk_data'] = 0
            except AttributeError:
                pass
            except OSError:
                pass
        if config is self.config and key == "row_height":
            try:
                self.row_height = int(value)
            except AttributeError:
                pass

    ''' check if the NLTK folder is present in the userdata '''
    def check_install(self):

        path = self.user_data_dir + '/' + 'nltk_data'

        if os.path.exists(path) and os.listdir(path) != []:
            print 'nltk data found'
            nltk.data.path.append(self.user_data_dir + '/' + 'nltk_data')
            trainer = TrainerThread()
            trainer.run()
        else:
            print 'nltk data not found, start downloading'
            try:
                os.makedirs(path)
                print 'make dir'
            except OSError:
                print 'dir already present'
            self.show_popup_dwn()   ##start the popup and the download data thread

    ''' popup for nltk download data '''
    def show_popup_dwn(self):

        p = DwnPopup()
        p.bind(on_dismiss=self.callback_nltk)
        p.open()

    def callback_nltk(self, instance):

        print('Popup', instance, 'is being dismissed')

        #when app start, train pos tagger
        trainer = TrainerThread()
        trainer.run()

if __name__ == '__main__':
    MyCogs().run()
