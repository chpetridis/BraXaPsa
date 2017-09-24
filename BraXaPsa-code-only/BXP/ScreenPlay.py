from functools import partial
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
from BXP.Level import Level
from BXP.Globals import Globals

back_sound = SoundLoader.load('Sounds/pressed_sound.mp3')    # Sound for going to previous Screen
Globals.sounds.append(back_sound)                            # Add sound to list for  on/off management


class ScreenPlay(Screen):
    play_layout = FloatLayout()             # Basic layout of the Screen
    parent_manager = ScreenManager          # The Screen Manager this screen is attached to
    level = Level()                         # Level object that interacts with GUI of this Screen
    heart_list = []                         # Reference to the heart images
    score_bar = ProgressBar(pos_hint={'center_x': 0.9, 'center_y': 0.58}, size_hint=(.15, None))

    def build_layout(self):
        #  LAYOUTS  #
        play_area = GridLayout(cols=10, rows=10, size_hint=(.7, .7), pos=(120, 100), spacing=(2, 2),
                               pos_hint={'center_x': 0.45, 'center_y': 0.45})
        hearts_layout = BoxLayout(orientation='horizontal', size_hint=(.15, .05),
                                  pos_hint={'center_x': 0.9, 'center_y': 0.78})
        total_score_layout = BoxLayout(orientation='horizontal', pos_hint={'center_x': 0.8, 'center_y': 0.02},
                                       size_hint=(.2, .05))

        # BUTTONS #
        back = Button(background_normal='Images/back.jpg', size_hint=(.1, .1), background_down='Images/backpressed.jpg',
                      pos_hint={'center_x': 0.95, 'center_y': 0.95}, on_release=partial(self.change_screen, 'menu'))
        restart_button = Button(background_normal='Images/restart.png', size_hint=(.038, .038),
                                pos_hint={'center_x': 0.85, 'center_y': 0.96}, background_down='Images/restart.png')
        sound = ToggleButton(background_normal='Images/sound_on.png', size_hint=(.038, .038),
                             pos_hint={'center_x': 0.8, 'center_y': 0.96}, background_down='Images/sound_off.png')

        # IMAGES #
        moves_left = Image(source='Images/moves_left.png', size_hint=(.2, None), pos=(0, 530))
        heart_1 = Image(source='Images/heart.jpg')
        heart_2 = Image(source='Images/heart.jpg')
        heart_3 = Image(source='Images/heart.jpg')

        # LABELS #
        level_text = Label(text="[size=30][b]LEVEL:[/b][/size]", pos_hint={'center_x': 0.16, 'center_y': 0.85},
                           markup=True)
        level_number = Label(text='[size=25][b]1[/b][/size]', pos_hint={'center_x': 0.25, 'center_y': 0.85}, id='1',
                             markup=True)
        moves_count = Label(text="[size=25][color=#b40000][b]" + self.level.get_starting_moves() + "[/b][/color][/size]",
                            markup=True, size_hint=(.2, None), pos=(95, 530))
        score_text = Label(text="[size=25][b]SCORE:[/b][/size]", markup=True,
                           pos_hint={'center_x': 0.9, 'center_y': 0.73})
        score_number = Label(text="[size=20][b]0[/b][/size]", pos_hint={'center_x': 0.9, 'center_y': 0.67}, markup=True)
        total_score_text = Label(text='Total Score:')
        total_score_number = Label(text="0", halign='left')

        #  GUI for Popup after Level Defeat  #
        try_again_button = Button(text='Try Again.', size_hint=(.4, .4))
        defeat_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        defeat_anchor.add_widget(try_again_button)
        defeat_popup = Popup(title='No more moves!', size_hint=(.3, .3), content=defeat_anchor, auto_dismiss=False,
                             title_size=25, title_align='center')

        #  GUI for Popup after Level Victory  #
        next_level_button = Button(text='Next Level!', size_hint=(.5, .4), pos_hint={'center_x': 0.5})
        level_victory_score_label = Label(text='0')
        victory_box_layout = BoxLayout(orientation='vertical')
        victory_box_layout.add_widget(level_victory_score_label)
        victory_box_layout.add_widget(next_level_button)
        victory_popup = Popup(title='You Won!', size_hint=(.3, .3), content=victory_box_layout, auto_dismiss=False,
                              title_size=25, title_align='center')

        #  GUI for popup for game end/restart  #
        end_game_button = Button(text='OK', size_hint=(.4, .35), pos_hint={'center_x': 0.5})
        end_game_score = Label(text="[size=20][b]Final Score: 0[/b][/size]", markup=True, )
        end_game_box = BoxLayout(orientation='vertical')
        end_game_box.add_widget(end_game_score)
        end_game_box.add_widget(end_game_button)
        end_game_popup = Popup(title='Game Ended!!!', size_hint=(.35, .35), content=end_game_box, auto_dismiss=False,
                               title_size=20, title_align='center')

        #  Bind Buttons  #
        sound.fbind('on_press', self.toggle_sound)
        try_again_button.fbind('on_release', self.reload_level, defeat_popup, play_area, moves_count, score_number,
                               False)
        next_level_button.fbind('on_press', self.load_next_level, level_number, moves_count, victory_popup,
                                score_number, play_area)
        restart_button.fbind('on_release', self.reload_level, defeat_popup, play_area, moves_count, score_number, True)
        end_game_button.fbind('on_release', self.restart_game, end_game_popup, level_number, moves_count,
                              score_number, play_area, total_score_number)

        #  Passing GUI components that Level needs to know  #
        self.level.set_score_bar(self.score_bar)
        self.level.set_label(moves_count, 'moves_count')
        self.level.set_label(score_number, 'score_number')
        self.level.set_label(end_game_score, 'end_game_score')
        self.level.set_label(total_score_number, 'total_score_number')
        self.level.set_label(level_victory_score_label, 'level_victory_score_label')
        self.level.set_popup(defeat_popup, 'defeat_popup')
        self.level.set_popup(victory_popup, 'victory_popup')
        self.level.set_popup(end_game_popup, 'end_game_popup')

        '''     LOAD EVERYTHING UP!     '''
        # First load widgets to sub layouts
        self.heart_list.append(heart_1)
        self.heart_list.append(heart_2)
        self.heart_list.append(heart_3)
        hearts_layout.add_widget(heart_1)
        hearts_layout.add_widget(heart_2)
        hearts_layout.add_widget(heart_3)
        total_score_layout.add_widget(total_score_text)
        total_score_layout.add_widget(total_score_number)

        # Then load to main layout of the Screen
        self.level.load_level(play_area)
        self.score_bar.max = self.level.score_to_beat
        self.play_layout.add_widget(back)
        self.play_layout.add_widget(restart_button)
        self.play_layout.add_widget(sound)
        self.play_layout.add_widget(hearts_layout)
        self.play_layout.add_widget(level_text)
        self.play_layout.add_widget(level_number)
        self.play_layout.add_widget(score_text)
        self.play_layout.add_widget(score_number)
        self.play_layout.add_widget(total_score_layout)
        self.play_layout.add_widget(self.score_bar)
        self.play_layout.add_widget(moves_left)
        self.play_layout.add_widget(moves_count)
        self.play_layout.add_widget(play_area)

    def set_screen_manager(self, manager):
        self.parent_manager = manager
        self.build_layout()

        return self.add_widget(self.play_layout)

    def change_screen(self, screen, *largs):
        global back_sound

        if Globals.active_sounds:               # If sounds are on play sound else silence
            back_sound.play()
        self.parent_manager.current = screen

    @staticmethod
    def toggle_sound(*largs):
        if Globals.active_sounds is True:
            # Unload all the sounds from memory as they will probably not be used short term
            for sound in Globals.sounds:
                sound.unload()
            Globals.active_sounds = False
        else:
            # Sound is back on! Load again all the sounds in memory
            for sound in Globals.sounds:
                sound.load()
            Globals.active_sounds = True

    def reload_level(self, defeat_popup, play_area, moves_count, score_number, reduce_lives, *largs):
        # Level object components reset #
        self.level.load_level(play_area)                                    # Load new items
        self.level.current_moves = int(self.level.get_starting_moves())     # Current moves back to initial number
        self.level.current_score = 0                                        # Level Score back to 0
        if reduce_lives:                # If this function was called from pressing restart button reduce player lives
            self.level.player.reduce_lives()

        # GUI reset #
        if self.level.player.lives is 2:
            self.heart_list[2].source = 'Images/heart_empty.jpg'
        elif self.level.player.lives is 1:
            self.heart_list[1].source = 'Images/heart_empty.jpg'
        else:
            self.level.check_for_high()             # If game ended check for high score and show end game popup
            self.level.end_game_popup.open()
        self.score_bar.value = 0
        moves_count.text = "[size=25][color=#b40000][b]" + self.level.get_starting_moves() + "[/b][/color][/size]"
        score_number.text = "[size=20][b]0[/b][/size]"
        defeat_popup.dismiss()

    def load_next_level(self, level_number, moves_count, victory_popup, score_number, play_area, *largs):
        # Level object components re-initiate #
        level_number.id = str(int(level_number.id) + 1)
        self.level.__init__()                               # Read the next level information
        self.level.load_level(play_area)                    # Load new items
        self.score_bar.max = self.level.score_to_beat       # Update max number of score bar(different for every level)
        self.score_bar.value = 0                            # bar % back to 0
        self.level.current_score = 0                        # Level score back to 0

        # GUI re-initiate #
        level_number.text = '[size=25][b]' + level_number.id + '[/b][/size]'
        moves_count.text = "[size=25][color=#b40000][b]" + self.level.get_starting_moves() + "[/b][/color][/size]"
        score_number.text = "[size=20][b]0[/b][/size]"
        victory_popup.dismiss()

    def restart_game(self, end_game_popup, level_number, moves_count, score_number, play_area, total_score, *largs):
        # Level object components re-initiate #
        level_number.id = '1'
        self.level.file_commander.reset_file()
        self.level.__init__()                       # Same actions as in load_next_level()
        self.level.load_level(play_area)
        self.score_bar.max = self.level.score_to_beat
        self.score_bar.value = 0
        self.level.current_score = 0
        self.level.player.lives = 3                 # additionally reset the player data
        self.level.player.total_score = 0

        # GUI re-initiate #
        for heart in self.heart_list:
            heart.source = 'Images/heart.jpg'
        level_number.text = '[size=25][b]' + level_number.id + '[/b][/size]'
        moves_count.text = "[size=25][color=#b40000][b]" + self.level.get_starting_moves() + "[/b][/color][/size]"
        score_number.text = "[size=20][b]0[/b][/size]"
        total_score.text = '0'
        end_game_popup.dismiss()
