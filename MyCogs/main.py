__author__ = 'matteo'

from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty, NumericProperty, StringProperty)

from GUI.login import login
from GUI.senderlist import senderlist
from GUI.approved import approved
from GUI.unapproved import unapproved
from GUI.undefined import undefined
from GUI.add import addslide
from GUI.add import foundslide
from GUI.edit import editslide

from background.db.initializer import Initializer
from background.db.connector import Connector

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

    #initialize global variables for sender e user ID
    userID = NumericProperty(0)
    senderID = NumericProperty(0)

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

    pb_login_value = NumericProperty(0)   #login progressbar value
    pb_sender_value = NumericProperty(0)    #sender data progressbar value
    pb_sender_label = StringProperty('Loading Data...')
    pb_nltk_value = NumericProperty(0)  #nltk download progressbar value
    pb_add_value = NumericProperty(0)

    # BEGIN INIT
    def __init__(self, **kwargs):
        super(MyCogsRoot, self).__init__(**kwargs)

        self.app = App.get_running_app()

    # END INIT

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

    ''' logout function '''
    def logout(self):

        self.app.root.senderID = 0
        self.app.root.userID = 0
        self.app.root.senderlist.clear_widgets()

        self.app.root.carousel.load_slide(self.app.root.login)


class MyCogs(App):

    def build(self):
        self.settings_cls = SettingsWithSidebar

    def build_config(self, config):
        config.setdefaults('General', {'db_data': False, 'nltk_data': False})

    def build_settings(self, settings):
        settings.add_json_panel("MyCogs Settings", self.config, data="""
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
                }
            ]"""
            )

    def on_config_change(self, config, section, key, value):
        if config is self.config and key == "db_data":
            try:
                if int(value) == 1:
                    conn = Connector()
                    init = Initializer(conn, verbose=True)
                    init.initAll()
                    self.root.logout()
                    #self.root.carousel.load_slide(self.root.login)
            except AttributeError:
                pass
        if config is self.config and key == "ntlk_data" and value == 1:
            try:
                pass
            except AttributeError:
                pass

if __name__ == '__main__':
    MyCogs().run()
