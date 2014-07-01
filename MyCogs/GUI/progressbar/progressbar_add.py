__author__ = 'matteo'

'''
Example to show a Popup usage with the content from kv lang.
'''
from kivy.uix.popup import Popup
from kivy.lang import Builder

from GUI.threads.addthread import AddThread


Builder.load_string('''
<AddPopup>:
    size_hint: .5, .5
    auto_dismiss: False
    title: 'Searching data for new chunk...'

    canvas.before:
        Color:
            rgba: 0.12, 0.13, 0.14, 1
        Rectangle:
            # self here refers to the widget i.e FloatLayout
            pos: self.pos
            size: self.size

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

        Knob:
            size: 200, 200
            min: 0
            max: 100
            value: app.root.pb_add_value
            show_label: True
            font_size: '38sp'
            font_color: 1, 1, 1,1
            show_marker: True
            knobimg_source: ""
            knobimg_color: 0, 0, 0, 0
            knobimg_bgcolor: 0.17, 0.18, 0.19, 1
            marker_img: "GUI/knob/img/bline.png"
            markeroff_color: 0, 0, 0, 0
            marker_inner_color: 0, 0, 0, 0

''')


class AddPopup(Popup):

    def __init__(self, chunk, **kwargs):

        super(AddPopup, self).__init__(**kwargs)

        #do the login and check how many mails to parse
        addt = AddThread(args=(), kwargs={'parent': self, 'chunk': chunk}, verbose=False)
        addt.start()
