__author__ = 'matteo'

import re

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.popup import Popup

from background.db.manager import Manager
from GUI.utils.utils import (IconButtonOk, IconButtonPlus, IconButtonDel, ColorDownToggleButtonH50,
                             BoxLayoutH50, IconButtonRefresh,
                             ColorDownButtonH50, TextInputH50, LabelH50, CheckBoxH50)
from wikipedia.WikiConnector import WikiConnector
from background.conceptnet5.conceptnet5 import ConceptNet5

Builder.load_file('GUI/edit/editslide.kv')

class MyTextInputEdit(TextInput):
    pass

class MyLabelEdit(Label):
    pass

class EditSlide(BoxLayout):

    btn_close = ObjectProperty()
    btn_save = ObjectProperty()
    layout_kl = ObjectProperty()
    layout_chunk = ObjectProperty()
    layout_meaning = ObjectProperty()
    selected = ObjectProperty()
    approved = ObjectProperty()
    unapproved = ObjectProperty()
    undefined = ObjectProperty()

    chunk = ObjectProperty()  #chunk
    meaning = ListProperty([])  #found meaning
    category = ObjectProperty()
    score = ObjectProperty()

    def __init__(self, verbose=False, **kwargs):

        super(EditSlide, self).__init__(**kwargs)

        self.id = 'editslide'
        self.verbose = verbose
        self.db = Manager()
        self.app = App.get_running_app()
        self.popupedit = self
        self.rows_ud = None
        self.rows_kl = None
        self.meaning = []
        self.found_numb = 0
        self.counter = 0
        self.btn_split = None
        self.wiki = WikiConnector()
        self.conceptnet = ConceptNet5()

    def fill_data(self):

        self.layout_meaning.clear_widgets()
        if self.btn_split != None:
            self.layout_chunk.remove_widget(self.btn_split)
        self.grid_row = GridLayout(cols=1, spacing=5)
        self.layout_meaning.add_widget(self.grid_row)

        #CHUNK
        print 'current chunk: ', self.app.root.current_chunk
        self.chunk.text = self.app.root.current_chunk

        ##retrieve data from userdata e knowledge table
        self.rows_ud = self.db.getchunk_ud(self.app.root.current_chunk, self.app.root.userID, self.app.root.senderID)
        self.rows_kl = self.db.getchunk_kl(self.app.root.current_chunk)

        #check if it is a ngram and if so add split button
        if int(self.rows_kl[0].ngram) > 1:
            self.btn_split = ColorDownButtonH50(id='split', text="[b]SPLIT[/b]", markup=True, size_hint_x=0.25, on_press=self.split)
            self.layout_chunk.add_widget(self.btn_split)

        #insert list of possible meaning/url
        for idx, row in enumerate(self.rows_kl):
            self.add_meaning_full(row)

        #set by default the first meaning True
        self.grid_row.children[0].children[0].active = True

        self.addmore = IconButtonPlus(id='addmore', spacing=20, size_hint_y=None, height=50)
        self.addmore.bind(on_press=self.add_meaning_empty)
        self.grid_row.add_widget(self.addmore)

        #set categories
        self.category.text = self.rows_kl[0].category

        #set score
        self.score.text = str(self.rows_ud[0].score)

        #set table radio button
        if self.rows_ud[0].status == 0:
            self.undefined.state = 'down'
        elif self.rows_ud[0].status == 1:
            self.approved.state = 'down'
        else:
            self.unapproved.state = 'down'

    def add_meaning_empty(self, instance):

        """
        Add a meaning row on the GUI to let the user add his own meaning
        :param instance:
        :return:
        """
        self.grid_row.remove_widget(self.addmore)

        self.found_numb += 1
        self.counter += 1
        bl = BoxLayoutH50(id='bl'+str(self.found_numb))
        al = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=50)
        al.add_widget(IconButtonDel(id='btn'+str(self.found_numb), on_press=self.remove_line))
        bl.add_widget(al)
        al2 = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=50)
        btn_ref = IconButtonRefresh(id='btn_ref'+str(self.found_numb))
        btn_ref.bind(on_press=self.update_wiki)
        al2.add_widget(btn_ref)
        bl.add_widget(al2)
        bl.add_widget(TextInputH50(id='found'+str(self.found_numb), text='', size_hint_x=0.25))
        bl.add_widget(TextInputH50(id='url'+str(self.found_numb), text='', size_hint_x=0.3))
        bl.add_widget(CheckBoxH50(id='dis'+str(self.found_numb), size_hint_x=0.15))
        bl.add_widget(CheckBoxH50(id='approved'+str(self.found_numb), size_hint_x=0.1))
        bl.add_widget(CheckBoxH50(id='chosen'+str(self.found_numb), group='chosen', size_hint_x=0.1))
        self.grid_row.add_widget(bl)
        self.grid_row.add_widget(self.addmore)

    def add_meaning_full(self, row):

        """
        Add a meaning row on the GUI to let the user add his own meaning
        :param instance:
        :return:
        """

        self.found_numb += 1
        self.counter += 1
        bl = BoxLayoutH50(id='bl'+str(self.found_numb))
        al = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=50)
        al.add_widget(IconButtonDel(id='btn'+str(self.found_numb), on_press=self.remove_line))
        bl.add_widget(al)
        al2 = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=50)
        btn_ref = IconButtonRefresh(id='btn_ref'+str(self.found_numb))
        btn_ref.bind(on_press=self.update_wiki)
        al2.add_widget(btn_ref)
        bl.add_widget(al2)
        bl.add_widget(TextInputH50(id='found', text=row.found, size_hint_x=0.25))
        bl.add_widget(TextInputH50(id='url'+str(self.found_numb), text=row.url, size_hint_x=0.3))
        if row.disambiguation_url == 1:
            bl.add_widget(CheckBoxH50(id='dis'+str(self.found_numb), size_hint_x=0.15, active=True))
        else:
            bl.add_widget(CheckBoxH50(id='dis'+str(self.found_numb), size_hint_x=0.15))
        bl.add_widget(CheckBoxH50(id='approved'+str(self.found_numb), size_hint_x=0.1, active=True))
        bl.add_widget(CheckBoxH50(id='chosen'+str(self.found_numb), group='chosen', size_hint_x=0.1))
        self.grid_row.add_widget(bl)

    def remove_line(self, instance):

        """
        callback event on del button, must remove corresponding line
        :param instance:
        :return:
        """
        self.counter -= 1
        self.grid_row.remove_widget(instance.parent.parent)

    def update_wiki(self, instance):

        """
        function to automatically update the wikipedia url from the corresponding founded meaning
        :param instance:
        :return:
        """
        print 'update wiki'
        chunk = instance.parent.parent.children[4].text
        if chunk == '':
            return
        url, dis = self.wiki.geturl(chunk.lower())
        instance.parent.parent.children[3].text = url
        if dis == 1:
            instance.parent.parent.children[2].active = True
        else:
            instance.parent.parent.children[2].active = False

    def update_cat(self):

        """
        function to automatically update the category from the original chunk
        :return:
        """
        print 'update category'
        print 'chunk: ', self.chunk.text
        self.conceptnet.search_edit(self.chunk.text)

    def split(self, instance):
        """
        callback function after "split" button pressed,
        opens a popup to allow user split the phrase
        :return:
        """
        print 'split button pressed'
        sp = SplitPopup(self.chunk.text, len(self.chunk.text.split(" ")), self.rows_ud, self.rows_kl)
        sp.bind(on_dismiss=self.split_end)
        sp.open()

    def split_end(self, instance):
        """
        callback function when split popup close
        :param instance:
        :return:
        """
        self.app.root.carousel.load_slide(self.app.root.approved)

    def update(self):

        """
        callback function after save changes button pressed. Store the new data in the DB
        :return: void
        """
        ##########################################################
        ## INPUT CHECK
        ##########################################################

        if self.chunk.text == '' or self.score.text == '' or not self.is_number(self.score.text):

            popup = Popup(title='Alert!!', content=Label(text="Incomplete data, please re-check!"),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        if self.counter == 0:
            # no meaning for that chunk
            popup = Popup(title='Alert!!', content=Label(text="No meaning for this chunk\nInsert at least one!"),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        self.meaning = []
        chosen_mean = ''
        for bl in self.layout_meaning.children:

            for idx, elem in enumerate(bl.children):
                if idx == 0:
                    continue    #the first children is the ADD new button
                #parse all rows
                mean = elem.children[4].text
                url = elem.children[3].text
                dis = elem.children[2].active
                approved = elem.children[1].active
                chosen = elem.children[0].active

                if mean == '':
                    popup = Popup(title='Alert!!', content=Label(text="Empty meaning not allowed!"),
                              size_hint=(None, None), size=(400, 200))
                    popup.open()
                    return

                self.meaning.append(dict(found=mean, url=url, dis=dis, approved=approved, chosen=chosen))

        ## check at least 1 approved
        count_approved = 0
        for x in self.meaning:
            print x
            if x['approved'] is True:
                count_approved += 1
        if count_approved == 0:
            popup = Popup(title='Alert!!', content=Label(text="At least insert one approved meaning!"),
                              size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        chosen_table = 0
        l = ToggleButtonBehavior.get_widgets('table')
        for toggle in l:
            if toggle.state == 'down':
                if toggle.text == '[b]Approved[/b]':
                    chosen_table = 1
                elif toggle.text == '[b]Unapproved[/b]':
                    chosen_table = 2
        del l

        print 'chunk: ', self.chunk.text
        print 'rows: ', self.meaning
        print 'category: ', self.category.text
        print 'chosen table: ', chosen_table
        print 'score: ', self.score.text
        print 'old_chunk: ', self.app.root.current_chunk
        print 'old_found: ', self.rows_kl

        ##########################################################
        ## DATA DUMP
        ##########################################################

        ##delete section (no update because I can have multiple meanings)
        for row in self.rows_kl:
            print 'dentro elimina kl'
            self.db.del_row_kl(chunk=str(self.app.root.current_chunk), found=row.found)

        self.db.del_chunk_ud(userid=self.app.root.userID, senderid=self.app.root.senderID, chunk=self.rows_ud[0].chunk)

        ##insert section
        for row in self.meaning:
            print row
            if row['approved']:

                print 'pre inserimento DB KL'

                self.db.insert_single_kl(chunk=self.chunk.text, found=row['found'],
                                     category=self.category.text, url=row['url'],
                                     dis=row['dis'], ngram=len(self.chunk.text.split(" ")))

                if row['chosen']:

                    print 'pre inserimento DB UD'

                    self.db.insert_single_ud(
                        userid=self.app.root.userID, senderid=self.app.root.senderID, chunk=self.chunk.text,
                        found=row['found'], score=int(self.score.text), status=chosen_table)

        ##########################################################
        ## END
        ##########################################################

        self.app.root.carousel.load_slide(self.app.root.approved)

    def is_number(self, number):
        """
        function to check if a string represent a integer
        :param number:
        :return:
        """
        try:
            int(number)
            return True
        except ValueError:
            return False


class SplitPopup(Popup):

    split_layout = ObjectProperty()

    def __init__(self, chunk, ngram, rows_ud, rows_kl, **kwargs):

        super(SplitPopup, self).__init__(**kwargs)
        grid2sp = GridLayout(cols=2, spacing=5, padding=[0, 5, 0, 0])
        self.split_layout.add_widget(grid2sp)
        self.splitted = chunk.split(" ")
        self.db = Manager()
        self.app = App.get_running_app()
        self.rows_ud = rows_ud
        self.rows_kl = rows_kl
        self.chunk = chunk

        ## BIGRAM
        if ngram == 2:

            grid2sp.add_widget(IconButtonOk(id='1', group='split', state='down', size_hint_x=0.3))
            grid2sp.add_widget(LabelH50(text=str(self.splitted[0] + " + " + self.splitted[1]), size_hint_x=0.7))

        ## TRIRAM
        else:

            grid2sp.add_widget(IconButtonOk(id='2', group='split', state='down', size_hint_x=0.3))
            grid2sp.add_widget(LabelH50(
                text=str(self.splitted[0] + " / " + self.splitted[1] + " " + self.splitted[2]), size_hint_x=0.7))

            grid2sp.add_widget(IconButtonOk(id='3', group='split', size_hint_x=0.3))
            grid2sp.add_widget(LabelH50(
                text=str(self.splitted[0] + " " + self.splitted[1] + " / " + self.splitted[2]), size_hint_x=0.7))

            grid2sp.add_widget(IconButtonOk(id='4', group='split', size_hint_x=0.3))
            grid2sp.add_widget(LabelH50(
                text=str(self.splitted[0] + " / " + self.splitted[1] + " / " + self.splitted[2]), size_hint_x=0.7))


    def split(self):

        chosen_split = 0
        chunks = []

        ########################################################
        ## GETTING SPLIT ORDER
        ########################################################

        l = ToggleButtonBehavior.get_widgets('split')
        for toggle in l:
            if toggle.state == 'down':
                chosen_split = int(toggle.id)
                break
        del l

        if chosen_split == 1 or chosen_split == 4:
            chunks = self.splitted
        elif chosen_split == 2:
            chunks.append(self.splitted[0])
            chunks.append(str(self.splitted[1] + " " + self.splitted[2]))
        elif chosen_split == 3:
            chunks.append(str(self.splitted[0] + " " + self.splitted[1]))
            chunks.append(self.splitted[2])

        print 'chunks: ', chunks

        ########################################################
        ## UPDATE UD AND KL
        ########################################################

        ##loop splitted chunks
        for x in chunks:

            ##UPDATE UD
            ## in the case the chunk is already present, the trigger will update the value
            ## default table is UNDEFINED
            self.db.insert_single_ud(
                self.app.root.userID, self.app.root.senderID, x, self.rows_ud[0].found, 2, self.rows_ud[0].score)

            ## need to loop on each KL result
            for y in self.rows_kl:

                n = x.split(" ")

                ##UPDATE KL (use insert or ignore)
                self.db.insert_single_kl(
                    chunk=x, found=y.found, category=y.category, url=y.url, dis=y.disambiguation_url, ngram=len(n))

        ##REMOVE OLD LINE IN KL
        for z in self.rows_kl:
            self.db.del_row_kl(chunk=self.chunk, found=z.found)

        ##REMOVE OLD LINE IN UD
        self.db.del_chunk_ud(self.app.root.userID, self.app.root.senderID, self.chunk)

        ########################################################
        ## CLOSE POPUP
        ########################################################

        self.dismiss()

















