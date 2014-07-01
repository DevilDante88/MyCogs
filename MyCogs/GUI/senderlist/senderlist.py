__author__ = 'matteo'

from kivy.network.urlrequest import UrlRequest
import json
import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from GUI.progressbar.progressbar_sender import SenderPopup
from GUI.utils.utils import ColorDownButton, GridLayout1Scroll
from background.db.manager import Manager

Builder.load_file('GUI/senderlist/senderlist.kv')

''' modified button appearance for pair numbers '''
class MyButtonPair(Button):

    pass

''' modified button appearance for spare numbers '''
class MyButtonSpare(Button):
    pass

class MyButtonUnicolor(BoxLayout):
    pass

class MyColorDownButton(ColorDownButton):
    pass

''' slide that contains the list of senders '''
class SenderList(BoxLayout):

    mylayout = ObjectProperty(None)

    def __init__(self, verbose=False, **kwargs):

        super(SenderList, self).__init__(**kwargs)
        self.verbose = verbose
        self.id = 'senderlist'

    def load_senders(self):

        if self.verbose:
            print 'load sender'

        self.clear_widgets() #clear previous widgets
        scroll = ScrollView()
        self.add_widget(scroll)
        grid = GridLayout1Scroll(spacing=8, padding=[5,0,5,0])
        scroll.add_widget(grid)

        db = Manager(verbose=self.verbose)
        app = App.get_running_app()
        rows = db.getSenders(app.root.userID)

        for index, row in enumerate(rows):

            text = ''
            if row[2] != '':
                text = str(row[2])
            else:
                text = str(row[1])
            if len(text) > 50:
                text = text[:50] + '...'
            text = '[b]' + text + '[/b]'

            button = MyColorDownButton()
            button.id = str(row[0])
            button.text = text

            button.bind(on_press=self.button_callback)
            grid.add_widget(button)

        return True

    ''' BUTTON callback function each time a sender in the sender list is selected '''
    def button_callback(self, instance):

        id = int(instance.id)
        print 'selected sender with ID: ', id

        #set the sender ID to the global variables
        app = App.get_running_app()
        app.root.senderID = id

        self.show_popup()   #instance the popup ui

    ''' function to launch the popup '''
    def show_popup(self):

        p = SenderPopup()
        p.bind(on_dismiss=self.popup_callback)
        p.open()

    ''' POPUP callback function when it close '''
    def popup_callback(self, instance):

        app = App.get_running_app()
        app.root.carousel.load_slide(app.root.approved)
        return False






