
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.listview import ListItemButton, ListItemLabel, CompositeListItem, ListView
from kivy.adapters.listadapter import ListAdapter
from kivy.core.text.markup import MarkupLabel
from kivy.app import App

from GUI.table.rowdetailview import RowDetailView

from kivy.lang import Builder

Builder.load_file('GUI/table/table.kv')

#####################################################################################
## TABLE
#####################################################################################

''' object row that will be inserted in the listview '''
class Row(object):

    def __init__(self, chunk='', found='', score=0, is_selected=False):
        self.chunk = chunk
        self.found = found
        self.score = score
        self.is_selected = is_selected

'''
class for a single elemnent inside my list, each element is a particular button
'''
class Cell(ListItemButton):

    def __init__(self, **kwargs):

        super(Cell, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def on_touch_down(self, touch):

        super(Cell, self).on_touch_down(touch)

''' table object '''
class Table(BoxLayout):

    def __init__(self, data_ap, **kwargs):

        super(Table, self).__init__(**kwargs)
        self.app = App.get_running_app()

        ## first check if len data = 0 add label to alert user
        if len(data_ap) is 0:
            self.add_widget(Label(text="No Data", font_size='32dp'))
            return

        ########################
        ## HEADER
        ########################

        self.container_header = GridLayout(cols=3, size_hint_y=None, height=(self.app.row_height*0.55), spacing=10)

        listview_header_widgets = [Label(text="CHUNK"),
                                   Label(text="FOUND"),
                                   Label(text="SCORE",
                                          size_hint_x=0.2)]

        for x in range(3):
            self.container_header.add_widget(listview_header_widgets[x])

        self.add_widget(self.container_header)

        ########################
        ## GRID
        ########################

        self.container_table = GridLayout(cols=2)

        # This is quite an involved args_converter, so we should go through the
        # details. A CompositeListItem instance is made with the args
        # returned by this converter. The first three, text, size_hint_y,
        # height are arguments for CompositeListItem. The cls_dicts list contains
        # argument sets for each of the member widgets for this composite:
        # ListItemButton and ListItemLabel.
        args_converter = \
            lambda row_index, obj: \
                {'text': obj.chunk,
                 'value': obj.chunk,
                 'size_hint_y': None,
                 'height': self.app.row_height * 0.5,
                 'cls_dicts': [{'cls': Cell,
                                'kwargs': {'text': obj.chunk,
                                           'id': obj.chunk}},
                               {'cls': Cell,
                                'kwargs': {'text': obj.found,
                                           'id': obj.chunk,
                                           'is_representing_cls': True}},
                               {'cls': Cell,
                                'kwargs': {'text': str(obj.score),
                                           'id': obj.chunk,
                                           'size_hint_x': 0.2}}]}

        self.list_adapter = ListAdapter(
                                   data=self.first_fill(data_ap),
                                   args_converter=args_converter,
                                   selection_mode='single',
                                   propagate_selection_to_data=True,
                                   allow_empty_selection=False,
                                   cls=CompositeListItem)

        # Use the adapter in our ListView:
        self.list_view = ListView(adapter=self.list_adapter)

        print 'chunck selezionato: ', self.list_adapter.selection[0].children[2].text

        chunk = MarkupLabel(self.list_adapter.selection[0].children[2].text).markup

        print 'selected: ', self.list_adapter.selection[0].children[2].id
        self.detail_view = RowDetailView(chunk=self.list_adapter.selection[0].children[2].id)

        self.list_adapter.bind(on_selection_change=self.detail_view.row_changed)

        self.container_table.add_widget(self.list_view)
        self.add_widget(self.container_table)
        self.add_widget(self.detail_view)

    def update(self, rows):

        d = []
        for row in rows:
            d.append(Row(chunk=row.chunk, found=row.found, score=row.score))

        self.list_adapter.data = d
        self.list_view.populate()

    def first_fill(self, rows):

        d = []
        for row in rows:
            d.append(Row(chunk=row.chunk, found=row.found, score=row.score))

        return d

    ######################################################
    #######################################################

