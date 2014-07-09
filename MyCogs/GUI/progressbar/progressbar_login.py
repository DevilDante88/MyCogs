__author__ = 'Matteo Renzi'

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import StringProperty

from GUI.threads.loginthread import LoginThread
import GUI.knob


Builder.load_string('''
<LoginPopup>:
    size_hint: .5, .5
    auto_dismiss: False
    title: 'Loading Sender List...'

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

        Knob:
            width: self.parent.height - 10
            height: self.parent.height - 10
            min: 0
            max: 100
            value: app.root.pb_login_value
            show_label: True
            font_size: '38sp'
            font_color: 1, 1, 1, 1
            show_marker: True
            knobimg_source: ""
            knobimg_color: 0, 0, 0, 0
            knobimg_bgcolor: 0.17, 0.18, 0.19, 1
            marker_img: "GUI/knob/img/bline.png"
            markeroff_color: 0, 0, 0, 0
            marker_inner_color: 0, 0, 0, 0

''')


class LoginPopup(Popup):

    status = StringProperty('')

    def __init__(self, email, pwd, **kwargs):

        super(LoginPopup, self).__init__(**kwargs)

        #do the login and check how many mails to parse
        lt = LoginThread(args=(), kwargs={'email': email, 'pwd': pwd, 'parent': self}, verbose=True)
        lt.start()



