__author__ = 'Matteo Renzi'

import re
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.app import App

from background.db.manager import Manager
from background.conceptnet5.conceptnet5 import ConceptNet5
from GUI.utils.utils import (TextInputH50, BoxLayoutH50,
                             CheckBoxH50, IconButtonDel, IconButtonPlus, GridLayout1)

Builder.load_file('GUI/add/foundslide.kv')


class FoundSlide(BoxLayout):

    bl_found = ObjectProperty()
    addmore = ObjectProperty()
    save = ObjectProperty()

    # original chunk inserted by user
    new_chunk = ObjectProperty()
    #object used by the thread to set meanings
    meaning = ObjectProperty()
    #object used by the thread to set categories
    new_category = ObjectProperty()

    def __init__(self, verbose=False, **kwargs):

        super(FoundSlide, self).__init__(**kwargs)

        self.verbose = verbose
        self.id = 'foundslide'
        self.found_numb = 0
        self.counter = 0
        self.db = Manager()
        self.app = App.get_running_app()
        self.grid_row = None
        self.scroll = None
        self.conceptnet = ConceptNet5()

    def fill_data(self):

        """
        Function called each time this slide is current
        :return:
        """
        self.found_numb = 0
        self.counter = 0
        self.bl_found.clear_widgets()
        self.grid_row = GridLayout1()
        self.bl_found.add_widget(self.grid_row)
        self.save.bind(on_press=self.save_data)

        print 'data retrieved'
        print 'meaning: ', self.meaning
        print 'category: ', self.new_category.text

        ## iterate the dictionary of values
        for k, v in self.meaning.iteritems():
            self.add_meaning_full(k, v[0], v[1])

        self.addmore = IconButtonPlus(id='addmore', spacing=20, size_hint_y=None, height=self.app.row_height)
        self.addmore.bind(on_press=self.add_meaning_empty)
        self.grid_row.add_widget(self.addmore)

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
        al = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=self.app.row_height)
        al.add_widget(IconButtonDel(id='btn'+str(self.found_numb), on_press=self.remove_line))
        bl.add_widget(al)
        bl.add_widget(TextInputH50(id='found'+str(self.found_numb), text='', size_hint_x=0.3))
        bl.add_widget(TextInputH50(id='url'+str(self.found_numb), text='', size_hint_x=0.3))
        bl.add_widget(CheckBoxH50(id='dis'+str(self.found_numb), size_hint_x=0.15))
        bl.add_widget(CheckBoxH50(id='approved'+str(self.found_numb), size_hint_x=0.1))
        if self.found_numb == 1:
            bl.add_widget(CheckBoxH50(id='chosen'+str(self.found_numb),
                                   group='chosen', size_hint_x=0.1, active=True))
        else:
            bl.add_widget(CheckBoxH50(id='chosen'+str(self.found_numb),
                                   group='chosen', size_hint_x=0.1))
        self.grid_row.add_widget(bl)
        self.grid_row.add_widget(self.addmore)

    def add_meaning_full(self, found, url, dis):

        """
        Add a meaning row on the GUI to let the user add his own meaning
        :param instance:
        :return:
        """

        self.found_numb += 1
        self.counter += 1
        bl = BoxLayoutH50(id='bl'+str(self.found_numb))
        al = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.05, size_hint_y=None, height=self.app.row_height)
        al.add_widget(IconButtonDel(id='btn'+str(self.found_numb), on_press=self.remove_line))
        bl.add_widget(al)
        bl.add_widget(TextInputH50(id='found'+str(self.found_numb), text=found, size_hint_x=0.3))
        bl.add_widget(TextInputH50(id='url'+str(self.found_numb), text=url, size_hint_x=0.3))
        if dis == 1:
            bl.add_widget(CheckBoxH50(id='dis'+str(self.found_numb), size_hint_x=0.15, active=True))
        else:
            bl.add_widget(CheckBoxH50(id='dis'+str(self.found_numb), size_hint_x=0.15))
        bl.add_widget(CheckBoxH50(id='approved'+str(self.found_numb), size_hint_x=0.1, active=True))
        if self.found_numb == 1:
            bl.add_widget(CheckBoxH50(id='chosen'+str(self.found_numb),
                                   group='chosen', size_hint_x=0.1, active=True))
        else:
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

    def update_cat(self):

        """
        function to automatically update the category from the original chunk
        :return:
        """
        print 'update category'
        print 'chunk: ', self.new_chunk.text
        self.conceptnet.search_addnew(self.new_chunk.text)

    def save_data(self, instance):

        """
        callback function called after "SAVE" button pressed
        need to check consistency of inserted data and if it's all OK dump new data
        :param instance:
        :return:
        """

        ##############################################################################
        ## DATA CHECK AND EXTRACTION
        ##############################################################################

        if self.new_chunk.text == "":
            # no meaning for that chunk
            popup = Popup(title='Alert!!', content=Label(text="Chunk Empty! Please fill chunk"),
                          size_hint=(0.5, 0.3), font_size='38sp')
            popup.open()
            return

        if self.counter == 0:
            # no meaning for that chunk
            popup = Popup(title='Alert!!', content=Label(text="No meaning for this chunk\nInsert at least one!"),
                          size_hint=(0.5, 0.3), font_size='38sp')
            popup.open()
            return

        meanings = []
        for bl in self.bl_found.children:

            #parse all meanings inserted

            chosen = bl.children[1].children[0].active
            approved = bl.children[1].children[1].active
            dis = bl.children[1].children[2].active
            url = bl.children[1].children[3].text
            found = bl.children[1].children[4].text

            if found == '':
                popup = Popup(title='Alert!!', content=Label(text="Empty found label not allowed!"),
                          size_hint=(0.5, 0.3), font_size='38sp')
                popup.open()
                return

            if chosen is True and approved is False:
                popup = Popup(title='Alert!!', content=Label(text="A meaning can't be chosen if not approved!"),
                          size_hint=(0.5, 0.3), font_size='38sp')
                popup.open()
                return

            dis_int = 0
            if dis:
                dis_int = 1

            if approved:
                meanings.append([found, url, dis_int, chosen])

        chosen_table = 0
        l = ToggleButtonBehavior.get_widgets('table')
        for toggle in l:
            if toggle.state == 'down':
                if toggle.text == 'Approved':
                    chosen_table = 1
                elif toggle.text == 'Unapproved':
                    chosen_table = 2

        del l

        ##############################################################################
        ## SAVE DATA
        ##############################################################################

        rows = self.db.existchunk_kl(self.new_chunk.text)

        # no control of chunk already present because I use INSERT OR REPLACE
        for x in meanings:

            ngram = len(self.new_chunk.text.split(" "))
            self.db.insert_single_kl(chunk=self.new_chunk.text, found=x[0],
                                     category=self.new_category.text, url=x[1], dis=int(x[2]), ngram=ngram)

            if x[3] is True:
                #case CHOSEN, need to add it to the UD
                self.db.insert_single_ud(userid=self.app.root.userID,
                                         senderid=self.app.root.senderID,
                                         chunk=self.new_chunk.text,
                                         found=x[0], status=chosen_table, score=1)

        ##############################################################################

        self.app.root.carousel.load_slide(self.app.root.approved)




