__author__ = 'Matteo Renzi'

from kivy.uix.popup import Popup
from kivy.lang import Builder

from GUI.threads.senderthread import SenderThread


Builder.load_string('''
<SenderPopup>:

    size_hint: .5, .5
    auto_dismiss: False
    title: app.root.pb_sender_label

    BoxLayout:
        orientation: 'vertical'

        AnchorLayout:
            size_hint_y: 0.8
            anchor_x: 'center'
            anchor_y: 'center'

            Knob:
                width: self.parent.height - 10
                height: self.parent.height - 10
                min: 0
                max: 100
                value: app.root.pb_sender_value
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

        Button:
            size_hint_y: 0.2
            text: '[b]STOP[/b]'
            markup: True
            on_press: root.stop_thread()

''')


class SenderPopup(Popup):

    def __init__(self, **kwargs):

        super(SenderPopup, self).__init__(**kwargs)

        #do the login and check how many mails to parse
        self.st = SenderThread(args=(), kwargs={'parent': self}, verbose=True)
        self.st.start()

    def stop_thread(self):

        print 'stop pressed'
        self.st.stop()
        self.dismiss()



