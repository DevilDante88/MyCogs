__author__ = 'Matteo Renzi'

from kivy.uix.popup import Popup
from kivy.lang import Builder

from GUI.threads.nltk_thread import DwnThread


Builder.load_string('''
<DwnPopup>:
    size_hint: .5, .5
    auto_dismiss: False
    title: 'Loading NLTK data...'

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

        Knob:
            width: self.parent.height - 10
            height: self.parent.height - 10
            min: 0
            max: 100
            value: app.root.pb_nltk_value
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


class DwnPopup(Popup):

    def __init__(self, **kwargs):

        super(DwnPopup, self).__init__(**kwargs)

        #do the login and check how many mails to parse
        dwt = DwnThread(args=(), kwargs={'parent': self}, verbose=True)
        dwt.start()