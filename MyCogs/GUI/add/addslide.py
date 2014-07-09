__author__ = 'Matteo Renzi'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.app import App

from GUI.progressbar.progressbar_add import AddPopup
from background.db.manager import Manager

Builder.load_file('GUI/add/addslide.kv')

class AddSlide(BoxLayout):

    """
    AddSlide class is a slide when user can add a new chunk simply by writing the chunk needed
    """

    ti_chunk = ObjectProperty()
    search_btn = ObjectProperty()

    def __init__(self, verbose=False, **kwargs):
        super(AddSlide, self).__init__(**kwargs)

        self.id = 'addslide'
        self.app = App.get_running_app()
        self.db = Manager()

    def fill_data(self):

        """
        function called each time this slide will be "current"
        need to binf the button 'search' to its proper function
        :return:
        """
        self.ti_chunk.text = ''
        self.search_btn.bind(on_press=self.search_start)

    def search_start(self, instance):

        """
        Function to start the retrieval of possible meanings from the inserted chunk.
        Check first if the label is empty and then if the chuck is already present in the DB
        :param instance:
        :return:
        """

        if self.ti_chunk.text == '':
            # if chunk is empty alert user
            popup = Popup(title='Alert!!', content=Label(text="Empty chunk inserted, retry!"),
                          size_hint=(0.5, 0.3), font_size='38sp')
            popup.open()
            return

        rows = self.db.existchunk_ud(userid=self.app.root.userID,
                                     senderid=self.app.root.senderID, chunk=self.ti_chunk.text)
        if len(rows) > 0:
            # if chunk is already present in the UD table
            popup = Popup(title='Alert!!',
                          content=Label(text="Chunk already present!\nYou can modify it pressing on the edit button!"),
                          size_hint=(0.5, 0.3), font_size='38sp')
            popup.open()
        else:
            # add popup with the chosen text which will start the thread
            p = AddPopup(self.ti_chunk.text)
            p.bind(on_dismiss=self.callback_add)
            p.open()

    def callback_add(self, instance):

        """
        When the progressbar will end, open a new slide to edit all data for new chunk
        :return:
        """

        self.app.root.carousel.load_slide(self.app.root.foundslide)







