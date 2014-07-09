__author__ = 'Matteo Renzi'

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.app import App

from background.db.manager import Manager

Builder.load_file('GUI/table/popups.kv')

class PopUpDel(Popup):

    btn_nodel = ObjectProperty()
    btn_yesdel = ObjectProperty()

    def __init__(self, **kwargs):
        super(PopUpDel, self).__init__(**kwargs)

        self.db = Manager()
        self.app = App.get_running_app()

        self.btn_nodel.bind(on_press=self.dismiss)
        self.btn_yesdel.bind(on_press=self.delete)

    def delete(self, instance):

        #remove from DB
        self.db.del_chunk_ud(self.app.root.userID, self.app.root.senderID, self.app.root.current_chunk)

        #refresh current table
        self.app.root.carousel.current_slide.fill_table()

        #close popup
        self.dismiss()





