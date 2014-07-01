__author__ = 'matteo'

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import NumericProperty

from GUI.table.table import Table
from background.db.manager import Manager


class Unapproved(BoxLayout):

    clicked = NumericProperty(0)    #clicked for the arrow up and down
    len_rows = NumericProperty(0)

    def __init__(self, **kwargs):

        super(Unapproved, self).__init__(**kwargs)

        self.id = 'unapproved'

    def fill_table(self):

        self.clear_widgets()    #clean all widgets

        app = App.get_running_app()
        id_user = app.root.userID
        id_sender = app.root.senderID
        self.clicked = 0

        db = Manager()

        ##INSERT TABLE
        up = Table(db.getall_ud(id_user, id_sender, 2))
        self.add_widget(up)

        return
