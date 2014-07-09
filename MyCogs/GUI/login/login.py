__author__ = 'Matteo Renzi'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from GUI.progressbar.progressbar_login import LoginPopup

from kivy.app import App
from kivy.lang import Builder

Builder.load_file('GUI/login/login.kv')

class Login(BoxLayout):

    def __init__(self, verbose=False, **kwargs):

        super(Login, self).__init__(**kwargs)

        self.id = 'login'
        self.app = App.get_running_app()
        self.verbose = verbose

    def login(self, *args):

        """
        function to start the login process, retrieve argument inserted from user
        check for error and if no error start the login thread
        :param args:
        :return:
        """

        email = self.ids.email.text
        pwd = self.ids.pwd.text

        self.show_popup(email, pwd)

        #do the login and check how many mails to parse

    def show_popup(self, email, pwd):

        p = LoginPopup(email, pwd)
        p.bind(on_dismiss=self.callback_login)
        p.open()

    def callback_login(self, instance):

        if instance.status != "OK":
            popup = Popup(title='ERROR!!', content=Label(text=instance.status),
                          size_hint=(0.5, 0.3), font_size='38sp')
            popup.bind(on_dismiss=self.callback_error)
            popup.open()
            return
        app = App.get_running_app()
        app.root.carousel.load_slide(app.root.senderlist)
        return False

    def callback_error(self, instance):

        app = App.get_running_app()
        app.root.carousel.load_slide(app.root.login)

