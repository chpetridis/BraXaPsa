from functools import partial
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from BXP.HighScores import HighScores
from BXP.Globals import Globals

back_sound = SoundLoader.load('Sounds/pressed_sound.mp3')        # Sound for going to previous Screen
Globals.sounds.append(back_sound)                                # Add sound to list for  on/off management


class ScreenHighScores(Screen):
    parent_manager = ScreenManager              # The Screen Manager this screen is attached to
    high_scores_layout = FloatLayout()          # Basic layout of the Screen
    high_scores = HighScores()

    def build_layout(self):
        #  General GUI of the Screen  #
        high_score_text = Label(text="[size=30][b][u]HIGH SCORES[/u][/b][/size]", markup=True,
                                pos_hint={'center_x': 0.5, 'center_y': 0.9})
        high_score_labels = BoxLayout(orientation='vertical', size_hint=(.2, .7),
                                      pos_hint={'center_x': 0.2, 'center_y': 0.5})
        high_scores_number_layout = BoxLayout(orientation='vertical', size_hint=(.2, .7),
                                              pos_hint={'center_x': 0.3, 'center_y': 0.5})
        back = Button(background_normal='Images/back.jpg', size_hint=(.1, .1), background_down='Images/backpressed.jpg',
                      pos_hint={'center_x': 0.95, 'center_y': 0.95}, on_release=partial(self.change_screen, 'menu'))

        #  Load Labels 1-10 for high score ordinance #
        for i in range(0, 10):
            label = Label(text="[size=30][b]" + str(i+1) + ".[/b][/size]", markup=True)
            high_score_labels.add_widget(label)

        #  Pass the layout reference for interaction #
        self.high_scores.set_high_scores_number_layout(high_scores_number_layout)

        #  Load everything up!  #
        self.high_scores.load_high_scores()
        self.high_scores_layout.add_widget(back)
        self.high_scores_layout.add_widget(high_score_labels)
        self.high_scores_layout.add_widget(high_score_text)
        self.high_scores_layout.add_widget(high_scores_number_layout)

    def set_screen_manager(self, manager):
        self.parent_manager = manager
        self.build_layout()

        return self.add_widget(self.high_scores_layout)

    def change_screen(self, screen, *largs):
        global back_sound

        if Globals.active_sounds:        # If sounds are on play sound else silence
            back_sound.play()
        self.parent_manager.current = screen
