from functools import partial

from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

from BXP.gamemanager.Globals import Globals

back_sound = SoundLoader.load('Sounds/pressed_sound.mp3')       # Sound for going to previous Screen
Globals.sounds.append(back_sound)


class HowToPlayScreen(Screen):
    parent_manager = ScreenManager
    how_to_play_layout = FloatLayout()      # Basic layout of the Screen

    def build_layout(self):
        scroll_bar = ScrollView(do_scroll_x=False)
        how_to_play_image = Image(source='Images/how_to_play.jpg', size_hint=(1, 1.35))
        back = Button(background_normal='Images/back.jpg', size_hint=(.1, .1), background_down='Images/backpressed.jpg',
                      pos_hint={'center_x': 0.95, 'center_y': 0.95}, on_release=partial(self.change_screen, 'menu'))

        scroll_bar.add_widget(how_to_play_image)
        self.how_to_play_layout.add_widget(scroll_bar)
        self.how_to_play_layout.add_widget(back)

    def set_screen_manager(self, manager):
        self.parent_manager = manager
        self.build_layout()

        return self.add_widget(self.how_to_play_layout)

    def change_screen(self, screen, *largs):
        global back_sound

        if Globals.active_sounds:
            back_sound.play()
        self.parent_manager.current = screen
