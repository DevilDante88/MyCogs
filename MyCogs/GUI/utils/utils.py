__author__ = 'matteo'

from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_file('GUI/utils/utils.kv')

class ColorDownButton(Button):
    """
    Button with a possibility to change the color on on_press (similar to background_down in normal Button widget)
    """
    background_color_normal = ListProperty([0.07, 0.074, 0.078, 0.9])
    background_color_down = ListProperty([0.55, 0.54, 0.54, 1])

    def __init__(self, **kwargs):
        super(ColorDownButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = self.background_color_normal

    def on_press(self):
        self.background_color = self.background_color_down

    def on_release(self):
        self.background_color = self.background_color_normal


class ColorDownButtonH50(ColorDownButton):
    pass


class ColorDownToggleButton(ToggleButton):
    """
    Button with a possibility to change the color on on_press (similar to background_down in normal Button widget)
    """
    background_color_normal = ListProperty([0.07, 0.074, 0.078, 0.9])
    background_color_down = ListProperty([0.55, 0.54, 0.54, 0.9])

    def __init__(self, **kwargs):
        super(ColorDownToggleButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = self.background_color_normal

    def on_state(self, instance, value):

        if value == 'down':
            self.background_color = self.background_color_down
        else:
            self.background_color = self.background_color_normal


class ColorDownToggleButtonH50(ColorDownToggleButton):
    pass


class BoxLayoutH50(BoxLayout):
    """
    BoxLayout
    orientation horizontal
    height 50
    """
    pass


class TextInputH50(TextInput):
    """
    TextInput
    height 50
    multiline false
    """
    pass


class LabelH50(Label):
    pass


class CheckBoxH50(CheckBox):
    pass


class GridLayout1Scroll(GridLayout):
    pass


class GridLayout1(GridLayout):
    pass


class ToggleButtonH50(ToggleButton):
    pass


class IconButtonEdit(ButtonBehavior, Image):
    pass


class IconButtonPlus(ButtonBehavior, Image):
    pass


class IconButtonDel(ButtonBehavior, Image):
    pass


class IconButtonRefresh(ButtonBehavior, Image):
    pass


class IconButtonOk(ToggleButtonBehavior, Image):

    def __init__(self, **kwargs):
        super(IconButtonOk, self).__init__(**kwargs)

        if self.state == 'down':
            self.source = 'data/img/icon_ok_white.png'
        else:
            self.source = 'data/img/icon_ok_grey.png'

    def on_state(self, instance, value):

        if value == 'down':
            self.source = 'data/img/icon_ok_white.png'
        else:
            self.source = 'data/img/icon_ok_grey.png'