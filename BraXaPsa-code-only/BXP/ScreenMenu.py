from functools import partial
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from BXP.Globals import Globals


class ScreenMenu(Screen):
    parent_manager = ScreenManager
    menu_layout = AnchorLayout(anchor_x='center', anchor_y='center')    # Basic layout of the Screen
    transition_sound = SoundLoader.load('Sounds/transition.mp3')
    Globals.sounds.append(transition_sound)

    def build_layout(self):
        sub_layout = BoxLayout(orientation='vertical', size_hint=(.5, .5))
        logo = Image(source='Images/logo.png')

        play_button = self.create_button("""[size=35]Play[/size]""", 'play')
        how_button = self.create_button("""[size=32]How To Play[/size]""", 'how_to_play')
        high_scores_button = self.create_button("""[size=32]HighScores[/size]""", 'high_scores')

        sub_layout.add_widget(logo)
        sub_layout.add_widget(play_button)
        sub_layout.add_widget(high_scores_button)
        sub_layout.add_widget(how_button)
        self.menu_layout.add_widget(sub_layout)

    def create_button(self, button_title, screen_name):
        button = Button(text=button_title, on_release=partial(self.change_screen, screen_name))
        button.markup = True
        button.background_color = (0, 0, 0, 0)
        button.pos_hint = {'center_x': 0.5}
        button.size_hint = (.5, .5)

        return button

    def set_screen_manager(self, manager):
        self.parent_manager = manager
        self.build_layout()

        return self.add_widget(self.menu_layout)

    def change_screen(self, screen, *largs):
        if Globals.active_sounds:
            self.transition_sound.play()
        self.parent_manager.current = screen
