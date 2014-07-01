__author__ = 'matteo'

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
                             BoxLayoutH50, ToggleButtonH50,
                             ColorDownButtonH50, TextInputH50, LabelH50, CheckBoxH50)

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
    dis_yes = ObjectProperty()
    dis_no = ObjectProperty()
    approved = ObjectProperty()
    unapproved = ObjectProperty()
    undefined = ObjectProperty()

    chunk = ObjectProperty()  #chunk
    meaning = ListProperty([])  #found meaning
    category = ObjectProperty()
    wikiurl = ObjectProperty()
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
        self.found_numb = 0
        self.counter = 0
        self.btn_split = None

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

        print 'rows_ud: ', self.rows_ud
        print 'rows_kl: ', self.rows_kl

        #check if it is a ngram and if so add split button
        if int(self.rows_kl[0].ngram) > 1:
            self.btn_split = ColorDownButtonH50(id='split', text="[b]SPLIT[/b]", markup=True, size_hint_x=0.25, on_press=self.split)
            self.layout_chunk.add_widget(self.btn_split)

        #insert list of possible meaning
        for idx, row in enumerate(self.rows_kl):
            self.add_meaning_full(row.found)

        self.addmore = IconButtonPlus(id='addmore', spacing=20, size_hint_y=None, height=50)
        self.addmore.bind(on_press=self.add_meaning_empty)
        self.grid_row.add_widget(self.addmore)

        #set categories
        self.category.text = self.rows_kl[0].category

        #set url
        self.wikiurl.text = self.rows_kl[0].url

        #set score
        self.score.text = str(self.rows_ud[0].score)

        #insert disambiguation status
        if self.rows_kl[0].disambiguation_url == 1:
            self.dis_yes.state = 'down'
        else:
            self.dis_no.state = 'down'

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
        bl = BoxLayoutH50(id='bl'+str(self.found_numb), spacing=5)
        bl.add_widget(LabelH50(text='Founded '+str(self.found_numb), size_hint_x=0.2))
        bl.add_widget(TextInputH50(id='found'+str(self.found_numb), text='', size_hint_x=0.6))
        btn_chosen = ColorDownToggleButtonH50(id='toggle'+str(self.found_numb), text='[b]CHOSEN[/b]',
                                                  markup=True, group='found', size_hint_x=0.15)
        bl.add_widget(btn_chosen)
        al = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=50)
        al.add_widget(IconButtonDel(id='btn'+str(self.found_numb), on_press=self.remove_line))
        bl.add_widget(al)
        self.grid_row.add_widget(bl)
        self.grid_row.add_widget(self.addmore)

    def add_meaning_full(self, found):

        """
        Add a meaning row on the GUI to let the user add his own meaning
        :param instance:
        :return:
        """
        self.found_numb += 1
        self.counter += 1
        bl = BoxLayoutH50(id='bl'+str(self.found_numb), spacing=5)
        bl.add_widget(LabelH50(text='Founded '+str(self.found_numb), size_hint_x=0.2))
        bl.add_widget(TextInputH50(id='found'+str(self.found_numb), text=found, size_hint_x=0.6))
        btn_chosen = ColorDownToggleButtonH50(id='toggle'+str(self.found_numb), text='[b]CHOSEN[/b]',
                                                  markup=True, group='found', size_hint_x=0.15)
        if found == self.rows_ud[0].found:
                btn_chosen.state = 'down'
        bl.add_widget(btn_chosen)
        al = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=50)
        al.add_widget(IconButtonDel(id='btn'+str(self.found_numb), on_press=self.remove_line))
        bl.add_widget(al)
        self.grid_row.add_widget(bl)

    def remove_line(self, instance):

        """
        callback event on del button, must remove corresponding line
        :param instance:
        :return:
        """
        self.counter -= 1
        self.grid_row.remove_widget(instance.parent.parent)

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

            print bl.children
            for idx, elem in enumerate(bl.children):
                if idx == 0:
                    continue
                #parse all meanings inserted
                mean = elem.children[2].text
                chosen = elem.children[1].state
                if mean == '':
                    popup = Popup(title='Alert!!', content=Label(text="Empty meaning not allowed!"),
                              size_hint=(None, None), size=(400, 200))
                    popup.open()
                    return
                if chosen == 'down':
                    chosen_mean = mean
                self.meaning.append(mean)

        chosen_table = 0
        l = ToggleButtonBehavior.get_widgets('table')
        for toggle in l:
            if toggle.state == 'down':
                if toggle.text == '[b]Approved[/b]':
                    chosen_table = 1
                elif toggle.text == '[b]Unapproved[/b]':
                    chosen_table = 2
        del l

        dis = 0
        l = ToggleButtonBehavior.get_widgets('dis')
        for toggle in l:
            if toggle.state == 'down':
                if toggle.text == '[b]YES[/b]':
                    dis = 1
                elif toggle.text == '[b]NO[/b]':
                    dis = 0
        del l

        print 'chunk: ', self.chunk.text
        print 'meaning: ', self.meaning
        print 'chosen_mean: ', chosen_mean
        print 'wikiurl: ', self.wikiurl.text
        print 'category: ', self.category.text
        print 'chosen table: ', chosen_table
        print 'disambiguation: ', dis
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
        for x in self.meaning:

            if x == chosen_mean:

                self.db.insert_single_ud(
                    userid=self.app.root.userID, senderid=self.app.root.senderID, chunk=self.chunk.text,
                    found=x, score=int(self.score.text), status=chosen_table)

            self.db.insert_single_kl(chunk=self.chunk.text, found=x,
                                     category=self.category.text, url=self.wikiurl.text,
                                     dis=dis, ngram=len(self.chunk.text.split(" ")))

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

















