__author__ = 'Matteo Renzi'

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.label import Label


from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder

from background.db.manager import Manager
from GUI.table.popups import PopUpDel

Builder.load_file('GUI/table/rowdetailview.kv')


class IconButtonUP(ButtonBehavior, Image):

    """
    Image Button to go UP in the possible meaning list
    """

    def __init__(self, **kwargs):

        super(IconButtonUP, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def on_arrow_up_press(self, *args):
        if self.app.root.carousel.current_slide.clicked > 0:
            self.app.root.carousel.current_slide.clicked -= 1
            self.app.root.carousel.current_slide.children[0].children[0].redraw2()


class IconButtonDOWN(ButtonBehavior, Image):

    """
    Image Button to go DOWN in the possible meaning list
    """

    def __init__(self, **kwargs):

        super(IconButtonDOWN, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def on_arrow_down_press(self, *args):
        if self.app.root.carousel.current_slide.clicked < (self.app.root.carousel.current_slide.len_rows - 1):
            self.app.root.carousel.current_slide.clicked += 1
            self.app.root.carousel.current_slide.children[0].children[0].redraw2()

class MyLabel(Label):
    pass


''' class to show the details of the selected row'''
class RowDetailView(BoxLayout):

    chunk = StringProperty('', allownone=True)
    layout = ObjectProperty(None)
    button_layout = ObjectProperty(None)

    url = StringProperty('')
    dis = StringProperty('')
    category = StringProperty('')
    meaning = StringProperty('')

    def __init__(self, chunk, **kwargs):

        super(RowDetailView, self).__init__(**kwargs)

        self.chunk = chunk
        self.app = App.get_running_app()
        self.app.root.carousel.current_slide.len_rows = 0

        if self.chunk:
            self.redraw2()

    """ function to redraw the area """
    def redraw2(self, *args):

        found = []
        category = []
        url = []
        disambiguation = []

        if self.chunk:

            print 'chunk:', self.chunk

            ##DYNAMIC PART
            ##retrieve data from knowledge table
            db = Manager()
            rows = db.getchunk_kl(self.chunk)

            self.app.root.carousel.current_slide.len_rows = len(rows)
            if len(rows) == 0:
                # if I don't retrieve a result, no widget to be added
                return

            self.meaning = rows[self.app.root.carousel.current_slide.clicked].found
            self.category = rows[self.app.root.carousel.current_slide.clicked].category
            self.url = rows[self.app.root.carousel.current_slide.clicked].url

            if rows[self.app.root.carousel.current_slide.clicked].disambiguation_url == 1:
                self.dis = 'YES'
            else:
                self.dis = 'NO'

    """ function to be called when the selected row is changed """
    def row_changed(self, list_adapter, *args):

        if len(list_adapter.selection) == 0:
            self.chunk = None
        else:
            selected_object = list_adapter.selection[0]

            if type(selected_object) is str:
                self.chunk = selected_object
            try:
                self.chunk = selected_object.id
            except AttributeError:
                self.chunk = selected_object.children[2].id

        self.app.root.carousel.current_slide.clicked = 0 #reset click to 0
        self.redraw2()

    ''' event listener of delete button '''
    def on_del_press(self):

        print 'delete button pressed'
        self.app.root.current_chunk = self.chunk

        p = PopUpDel()
        #p.bind(on_dismiss=self.callback_nltk)
        p.open()

    ''' event listener for edit button '''
    def on_edit_press(self):

        print 'edit button pressed'

        self.app.root.current_chunk = self.chunk
        self.app.root.carousel.load_slide(self.app.root.editslide)

    ''' event listener for add button '''
    def on_add_press(self):

        print 'add button pressed'
        self.app.root.carousel.load_slide(self.app.root.addslide)

