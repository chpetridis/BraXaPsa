from functools import partial
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from BXP.Globals import Globals


class ScreenMenu(Screen):
    parent_manager = ScreenManager                                      # The Screen Manager this screen is attached to
    menu_layout = AnchorLayout(anchor_x='center', anchor_y='center')    # Basic layout of the Screen
    transition_sound = SoundLoader.load('Sounds/transition.mp3')
    Globals.sounds.append(transition_sound)                             # Add sound to list for  on/off management

    def build_layout(self):
        sub_layout = BoxLayout(orientation='vertical', size_hint=(.5, .5))
        logo = Image(source='Images/logo.png')

        #  Buttons for changing between the 4 Screens #
        play_button = Button(text="""[size=35]Play[/size]""", markup=True, size_hint=(.5, .5),
                             background_color=(0, 0, 0, 0), pos_hint={'center_x': 0.5},
                             on_release=partial(self.change_screen, 'play'))

        how_button = Button(text="""[size=32]How To Play[/size]""", markup=True, background_color=(0, 0, 0, 0),
                            pos_hint={'center_x': 0.5}, size_hint=(.5, .5),
                            on_release=partial(self.change_screen, 'how_to_play'))

        high_scores_button = Button(text="""[size=32]HighScores[/size]""", markup=True, size_hint=(.5, .5),
                                    background_color=(0, 0, 0, 0), pos_hint={'center_x': 0.5},
                                    on_release=partial(self.change_screen, 'high_scores'))

        #  Load everything up! #
        sub_layout.add_widget(logo)
        sub_layout.add_widget(play_button)
        sub_layout.add_widget(high_scores_button)
        sub_layout.add_widget(how_button)
        self.menu_layout.add_widget(sub_layout)

    def set_screen_manager(self, manager):
        self.parent_manager = manager
        self.build_layout()

        return self.add_widget(self.menu_layout)

    def change_screen(self, screen, *largs):
        if Globals.active_sounds:           # If sounds are on play sound else silence
           self.transition_sound.play()
        self.parent_manager.current = screen
