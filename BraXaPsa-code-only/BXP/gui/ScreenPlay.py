from functools import partial

from kivy.core.audio import SoundLoader
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton

from BXP.gamemanager.Globals import Globals
from BXP.gamemanager.Level import Level

back_sound = SoundLoader.load('Sounds/pressed_sound.mp3')
Globals.sounds.append(back_sound)


class ScreenPlay(Screen):
    play_layout = FloatLayout()             # Basic layout of the Screen
    parent_manager = ScreenManager
    level = Level()
    heart_list = []
    score_bar = ProgressBar(pos_hint={'center_x': 0.9, 'center_y': 0.58}, size_hint=(.15, None))

    def build_layout(self):
        #  LAYOUTS  #
        hearts_layout = self.create_box_layout(0.9, 0.78, .15, .05)
        total_score_layout = self.create_box_layout(0.8,  0.02, .2, .05)
        play_area = GridLayout(cols=10, rows=10, size_hint=(.7, .7), pos=(120, 100), spacing=(2, 2),
                               pos_hint={'center_x': 0.45, 'center_y': 0.45})

        # BUTTONS #
        back = self.create_button('Images/back.jpg', 'Images/backpressed.jpg', 0.95, 0.95, .1, .1, False)
        restart_button = self.create_button('Images/restart.png', 'Images/restart.png', 0.85, 0.96, .038, .038, False)
        sound = self.create_button('Images/sound_on.png', 'Images/sound_off.png',  0.8, 0.96, .038, .038, True)

        # IMAGES #
        moves_left = Image(source='Images/moves_left.png', size_hint=(.2, None), pos=(0, 530))
        heart_1 = Image(source='Images/heart.jpg')
        heart_2 = Image(source='Images/heart.jpg')
        heart_3 = Image(source='Images/heart.jpg')

        # LABELS #
        total_score_text = Label(text='Total Score:')
        total_score_number = Label(text="0", halign='left')
        level_text = self.create_label("[size=30][b]LEVEL:[/b][/size]", 0.16, 0.85)
        level_number = self.create_label("[size=25][b]1[/b][/size]", 0.25, 0.85)
        level_number.id = '1'
        score_text = self.create_label("[size=25][b]SCORE:[/b][/size]", 0.9, 0.73)
        score_number = self.create_label("[size=20][b]0[/b][/size]", 0.9, 0.67)
        moves_count = Label(text="[size=25][color=#b40000][b]" + self.level.get_starting_moves() + "[/b][/color][/size]",
                            markup=True, size_hint=(.2, None), pos=(95, 530))

        #  GUI for Popup after Level Defeat  #
        try_again_button = Button(text='Try Again.', size_hint=(.4, .4))
        defeat_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        defeat_anchor.add_widget(try_again_button)
        defeat_popup = self.create_popup('No more moves!', .3, .3, defeat_anchor, 25)

        #  GUI for Popup after Level Victory  #
        next_level_button = Button(text='Next Level!', size_hint=(.5, .4), pos_hint={'center_x': 0.5})
        level_victory_score_label = Label(text='0')
        victory_box_layout = BoxLayout(orientation='vertical')
        victory_box_layout.add_widget(level_victory_score_label)
        victory_box_layout.add_widget(next_level_button)
        victory_popup = self.create_popup('You Won!', .3, .3, victory_box_layout, 25)

        #  GUI for popup for game end/restart  #
        end_game_button = Button(text='OK', size_hint=(.4, .35), pos_hint={'center_x': 0.5})
        end_game_score = Label(text="[size=20][b]Final Score: 0[/b][/size]", markup=True, )
        end_game_box = BoxLayout(orientation='vertical')
        end_game_box.add_widget(end_game_score)
        end_game_box.add_widget(end_game_button)
        end_game_popup = self.create_popup('Game Ended!!!', .35, .35, end_game_box, 20)

        #  Bind Buttons  #
        sound.on_press = self.toggle_sound
        back.on_release = (partial(self.change_screen, 'menu'))
        restart_button.on_release = partial(self.reload_level, defeat_popup, play_area, moves_count, score_number, True)
        try_again_button.fbind('on_release', self.reload_level, defeat_popup, play_area, moves_count, score_number,
                               False)
        next_level_button.fbind('on_press', self.load_next_level, level_number, moves_count, victory_popup,
                                score_number, play_area)
        end_game_button.fbind('on_release', self.restart_game, end_game_popup, level_number, moves_count,
                              score_number, play_area, total_score_number)

        #  Passing GUI components that Level needs to know  #
        self.level.set_score_bar(self.score_bar)
        self.pass_label_components(moves_count, score_number, end_game_score,
                                   total_score_number, level_victory_score_label)
        self.pass_popup_components(defeat_popup, victory_popup, end_game_popup)

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

        if Globals.active_sounds:
            back_sound.play()
        self.parent_manager.current = screen

    @staticmethod
    def toggle_sound(*largs):
        if Globals.active_sounds is True:
            for sound in Globals.sounds:
                sound.unload()
            Globals.active_sounds = False
        else:
            for sound in Globals.sounds:
                sound.load()
            Globals.active_sounds = True

    @staticmethod
    def create_box_layout(x, y, size_x, size_y):
        box_layout = BoxLayout(orientation='horizontal')
        box_layout.size_hint = (size_x, size_y)
        box_layout.pos_hint = {'center_x': x, 'center_y': y}

        return box_layout

    @staticmethod
    def create_button(image_normal, image_down, x, y, size_x, size_y, toggle_button):
        if toggle_button:
            button = ToggleButton(background_normal=image_normal, background_down=image_down)
        else:
            button = Button(background_normal=image_normal, background_down=image_down)
        button.size_hint = (size_x, size_y)
        button.pos_hint = {'center_x': x, 'center_y': y}

        return button

    @staticmethod
    def create_label(label_text, x, y):
        label = Label(text=label_text)
        label.markup = True
        label.pos_hint = {'center_x': x, 'center_y': y}

        return label

    @staticmethod
    def create_popup(popup_title, size_x, size_y, layout, title_size):
        popup = Popup(title=popup_title)
        popup.size_hint = (size_x, size_y)
        popup.content = layout
        popup.title_size = title_size
        popup.title_align = 'center'
        popup.auto_dismiss = False

        return popup

    def pass_label_components(self, moves_count, score_number, end_game_score,
                              total_score_number, level_victory_score_label):

        self.level.set_label(moves_count, 'moves_count')
        self.level.set_label(score_number, 'score_number')
        self.level.set_label(end_game_score, 'end_game_score')
        self.level.set_label(total_score_number, 'total_score_number')
        self.level.set_label(level_victory_score_label, 'level_victory_score_label')

    def pass_popup_components(self, defeat_popup, victory_popup, end_game_popup):
        self.level.set_popup(defeat_popup, 'defeat_popup')
        self.level.set_popup(victory_popup, 'victory_popup')
        self.level.set_popup(end_game_popup, 'end_game_popup')

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
        self.level.file_commander.reset_file_pointer()
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
