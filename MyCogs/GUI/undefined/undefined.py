__author__ = 'matteo'

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import NumericProperty

from GUI.table.table import Table
from background.db.manager import Manager


class Undefined(BoxLayout):

    clicked = NumericProperty(0)    #clicked for the arrow up and down
    len_rows = NumericProperty(0)

    def __init__(self, **kwargs):

        super(Undefined, self).__init__(**kwargs)

        self.id = 'undefined'

    def fill_table(self):

        self.clear_widgets()    #clean all widgets

        app = App.get_running_app()
        id_user = app.root.userID
        id_sender = app.root.senderID
        self.clicked = 0

        db = Manager()

        ##INSERT TABLE
        ud = Table(db.getall_ud(id_user, id_sender, 0))
        self.add_widget(ud)

        return
