from functools import partial
from random import choice, randint

from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.togglebutton import ToggleButton

from BXP.gamemanager.Globals import Globals
from BXP.gamemanager.Player import Player
from BXP.gamemanager.LevelDetermine import LevelDetermine
from BXP.gui.ScreenHighScores import ScreenHighScores as shs

play_grid = [[ObjectProperty(None) for i in range(10)] for j in range(10)]  # Relative view of the Grid
wait_item = None
play_area = GridLayout

scissors_sound = SoundLoader.load('Sounds/Scissor_Snip.mp3')
rock_sound = SoundLoader.load('Sounds/Falling_rocks_sound_effect.mp3')
paper_sound = SoundLoader.load('Sounds/Paper_Crumpling_Sound_Effect.mp3')
fail_sound = SoundLoader.load('Sounds/fail_sound.mp3')
new_high_score = SoundLoader.load('Sounds/new_high_score.mp3')
# Add sounds to list for  on/off management
Globals.sounds.append(paper_sound)
Globals.sounds.append(scissors_sound)
Globals.sounds.append(rock_sound)
Globals.sounds.append(fail_sound)
Globals.sounds.append(new_high_score)


class Item:
    pos_x = 0
    pos_y = 0
    item_type = " "
    super_item = False
    item_button = ToggleButton

    def __init__(self, parent_level, item_type, pos_x, pos_y):
        self.item_type = item_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        image, image_down = self.image_factory(item_type)
        self.item_button = ToggleButton(background_normal=image, background_down=image_down,
                                        on_release=partial(self.swap, parent_level))

    @staticmethod
    def image_factory(item_type):
        if item_type is 'rock':
            return 'Images/rock.png', 'Images/rock_pressed.png'
        elif item_type is 'paper':
            return 'Images/paper.png', 'Images/paper_pressed.png'
        elif item_type is 'scissors':
            return 'Images/scissors.png', 'Images/scissors_pressed.png'
        elif item_type is 'orange_bomb':
            return 'Images/orange_bomb.jpg', 'Images/orange_bomb_pressed.jpg'
        else:
            return 'Images/red_bomb.jpg', 'Images/red_bomb_pressed.jpg'

    def animate_swap(self, real_x, real_y, parent_level):
        swap_animation = Animation(pos=(real_x, real_y), duration=.25)
        swap_animation.fbind('on_complete', self.play, parent_level)
        swap_animation.start(self.item_button)

    def fall_animation(self, real_x, real_y, parent_level, single_time, fix_once, smooth_animation):
        global play_area

        if smooth_animation:  # So may the animation be smoother (only executed by items that were destroyed in triad)
            drop_animation = Animation(pos=(real_x, real_y+10000), duration=.3) + \
                             Animation(pos=(real_x, real_y), duration=.3)
        else:
            drop_animation = Animation(pos=(real_x, real_y), duration=.6)
        if single_time and fix_once:
            drop_animation.fbind('on_complete', parent_level.fix_play_area, True)
        drop_animation.start(self.item_button)

    def swap(self, parent_level, *largs):
        global wait_item, play_area

        if Globals.hold:                # If you were the first item to be selected wait
            wait_item = self
            Globals.hold = False
            return

        Globals.hold = True
        self.change_buttons_state_to_normal()

        if self.can_swap():
            self.make_animation(parent_level)
            self.make_swap(parent_level)
        else:
            wait_item = None

    def make_animation(self, parent_level):
        global wait_item

        self.animate_swap(wait_item.get_real_x(), wait_item.get_real_y(), parent_level)
        wait_item.animate_swap(self.get_real_x(), self.get_real_y(), parent_level)

    def make_swap(self, parent_level):
        global wait_item

        self.change_place_in_grid_with(wait_item)
        parent_level.reduce_current_moves_by(1)

    def change_buttons_state_to_normal(self):
        global wait_item

        self.item_button.state = 'normal'
        wait_item.item_button.state = 'normal'

    def can_swap(self):
        global wait_item

        if self.is_bomb() or wait_item.is_bomb():
            return False

        if (wait_item.pos_x is not 0) and (wait_item.pos_x-1 is self.pos_x and wait_item.pos_y is self.pos_y):
            return True
        elif (wait_item.pos_x is not 9) and (wait_item.pos_x+1 is self.pos_x and wait_item.pos_y is self.pos_y):
            return True
        elif (wait_item.pos_y is not 0) and (wait_item.pos_y-1 is self.pos_y and wait_item.pos_x is self.pos_x):
            return True
        elif (wait_item.pos_y is not 9) and (wait_item.pos_y+1 is self.pos_y and wait_item.pos_x is self.pos_x):
            return True
        else:
            return False

    def play(self, parent_level, *largs):
        global play_grid

        #  Make your calculations regardless and inform if u found anything  #
        triad_list = self.check_trinity()
        if len(triad_list) is not 0:
            parent_level.increase_score_by(30)
            self.play_sound(triad_list[0].item_type)
            self.check_quad(triad_list)
            for item in triad_list:
                if item.super_item is True:
                    item.destroy_line(item, self.find_direction(triad_list), parent_level)
                item.change_type_to('empty')
            Globals.found_triad = True
            self.destroy_nearby_bombs(triad_list, parent_level)

        #  If you are the first to complete calculations wait #
        if Globals.hold:
            Globals.hold = False
            return
        Globals.hold = True

        #  If someone(or even both) found a triad animate and fix  #
        #  else reduce another move  #
        if Globals.found_triad is True:
            fix_once = True  # SO MAY fix_play_area() IS CALLED ONCE #
            for i in range(9, -1, -1):       # Go from bottom to top until u find an empty item (for every column)
                found_start_point = False
                for j in range(9, -1, -1):
                    if play_grid[j][i].item_type is 'empty' and found_start_point is False:
                        found_start_point = True
                        animation_list = self.make_animation_list(j, i)
                        self.animate_fall(animation_list, parent_level, fix_once)
                        fix_once = False
        else:
            self.play_sound('fail')
            parent_level.reduce_current_moves_by(1)
            parent_level.check_endgame()

    def check_quad(self, triad_list):
        reference_x = triad_list[0].pos_x
        reference_y = triad_list[0].pos_y

        if self.find_direction(triad_list) is 'vertical':
            if reference_x < 9:
                if triad_list[0].item_type is play_grid[reference_x+1][reference_y].item_type:
                    play_grid[reference_x + 1][reference_y].change_item_to_super(triad_list)
                    return
            if reference_x-2 > 0:
                if triad_list[0].item_type is play_grid[(reference_x-2) - 1][reference_y].item_type:
                    play_grid[(reference_x-2) - 1][reference_y].change_item_to_super(triad_list)
                    return
        else:
            if reference_y > 0:
                if triad_list[0].item_type is play_grid[reference_x][reference_y-1].item_type:
                    play_grid[reference_x][reference_y-1].change_item_to_super(triad_list)
                    return
            if reference_y+2 < 9:
                if triad_list[0].item_type is play_grid[reference_x][(reference_y+2)+1].item_type:
                    play_grid[reference_x][(reference_y+2)+1].change_item_to_super(triad_list)
                    return

    def change_item_to_super(self, triad_list):
        super_image, super_image_down = self.identify_super_item(triad_list[0].item_type)
        play_grid[self.pos_x][self.pos_y].super_item = True
        play_grid[self.pos_x][self.pos_y].item_button.background_normal = super_image
        play_grid[self.pos_x][self.pos_y].item_button.background_down = super_image_down

    @staticmethod
    def identify_super_item(item_type):
        if item_type is 'paper':
            super_image = 'Images/scroll.png'
            super_image_down = 'Images/scroll_pressed.png'
        elif item_type is 'rock':
            super_image = 'Images/diamond.png'
            super_image_down = 'Images/diamond_pressed.png'
        else:
            super_image = 'Images/golden_scissors.png'
            super_image_down = 'Images/golden_scissors_pressed.png'

        return super_image, super_image_down

    def destroy_line(self, item, direction, parent_level):
        points_sum = 0
        doomed_type = self.find_which_type_should_destroy(item)
        x, y = self.initialize_start_point(direction)
		
        for i in range(0, 10):
            if play_grid[x][y].item_type is doomed_type:
                points_sum = points_sum + 10
                play_grid[x][y].change_type_to('empty')
            if play_grid[x][y].is_bomb():
                points_sum = points_sum + 15
                if play_grid[x][y].item_type is 'orange_bomb':
                    parent_level.orange_bomb_counter = parent_level.orange_bomb_counter - 1
                else:
                    parent_level.red_bomb_counter = parent_level.red_bomb_counter - 1
                play_grid[x][y].change_type_to('empty')
            if direction is 'vertical':
                x = x + 1
            else:
                y = y + 1
        parent_level.increase_score_by(points_sum)
		
	@staticmethod
	def initialize_start_point(direction):
		if direction is 'vertical':
			   return 0, item.pos_y
		   else:
			   return item.pos_x, 0
		
	@staticmethod
	def find_which_type_should_destroy(item):
		if item.item_type is 'paper':
			return 'rock'
		elif item.item_type is 'rock':
			return 'scissors'
		else:
			return 'paper'

    def check_trinity(self):
        triad_list = []
        if self.item_type is 'empty' or self.is_bomb():
            return triad_list

        if self.pos_x > 1:
            if (self.item_type == play_grid[self.pos_x - 1][self.pos_y].item_type
                               == play_grid[self.pos_x - 2][self.pos_y].item_type):
							   
                triad_list.append(self)
                triad_list.append(play_grid[self.pos_x - 1][self.pos_y])
                triad_list.append(play_grid[self.pos_x - 2][self.pos_y])
                return triad_list

        if self.pos_x < 8:
            if (self.item_type == play_grid[self.pos_x + 1][self.pos_y].item_type
                               == play_grid[self.pos_x + 2][self.pos_y].item_type):
							   
                triad_list.append(play_grid[self.pos_x + 2][self.pos_y])
                triad_list.append(play_grid[self.pos_x + 1][self.pos_y])
                triad_list.append(self)
                return triad_list

        if self.pos_y > 1:
            if (self.item_type == play_grid[self.pos_x][self.pos_y - 1].item_type
                               == play_grid[self.pos_x][self.pos_y - 2].item_type):
							   
                triad_list.append(play_grid[self.pos_x][self.pos_y - 2])
                triad_list.append(play_grid[self.pos_x][self.pos_y - 1])
                triad_list.append(self)
                return triad_list

        if self.pos_y < 8:
            if (self.item_type == play_grid[self.pos_x][self.pos_y + 1].item_type
                               == play_grid[self.pos_x][self.pos_y + 2].item_type):
							   
                triad_list.append(self)
                triad_list.append(play_grid[self.pos_x][self.pos_y + 1])
                triad_list.append(play_grid[self.pos_x][self.pos_y + 2])
                return triad_list

        if 9 > self.pos_y > 0:
            if (self.item_type == play_grid[self.pos_x][self.pos_y + 1].item_type
                               == play_grid[self.pos_x][self.pos_y - 1].item_type):
							   
                triad_list.append(play_grid[self.pos_x][self.pos_y - 1])
                triad_list.append(self)
                triad_list.append(play_grid[self.pos_x][self.pos_y + 1])
                return triad_list

        if 9 > self.pos_x > 0:
            if (self.item_type == play_grid[self.pos_x + 1][self.pos_y].item_type
                               == play_grid[self.pos_x - 1][self.pos_y].item_type):
							   
                triad_list.append(play_grid[self.pos_x + 1][self.pos_y])
                triad_list.append(self)
                triad_list.append(play_grid[self.pos_x - 1][self.pos_y])
                return triad_list

        return triad_list

    @staticmethod
    def find_direction(triad_list):
        if triad_list[0].pos_y is triad_list[1].pos_y:
            return 'vertical'
        return 'horizontal'

    @staticmethod
    def destroy_nearby_bombs(triad_list, parent_level):      # Destroy all the nearby bombs(distance 1 from triad given)
        global play_grid

        for item in triad_list:
            if item.pos_x > 0:
		self.check_for_bomb(parent_level, item.pos_x-1, item.pos_y)
            if item.pos_x > 0 and item.pos_y > 0:
		self.check_for_bomb(parent_level, item.pos_x-1, item.pos_y-1)
            if item.pos_x > 0 and item.pos_y < 9:
		self.check_for_bomb(parent_level, item.pos_x-1, item.pos_y+1)
            if item.pos_y > 0:
		self.check_for_bomb(parent_level, item.pos_x, item.pos_y-1)
            if item.pos_y < 9:
		self.check_for_bomb(parent_level, item.pos_x, item.pos_y+1)
            if item.pos_x < 9:
		self.check_for_bomb(parent_level, item.pos_x+1, item.pos_y)
            if item.pos_x < 9 and item.pos_y > 0:
		self.check_for_bomb(parent_level, item.pos_x+1, item.pos_y-1)
            if item.pos_x < 9 and item.pos_y < 9:
		self.check_for_bomb(parent_level, item.pos_x+1, item.pos_y+1)
					
	@staticmethod
	def check_for_bomb(parent_level, pos_x, pos_y):
	  if play_grid[pos_x][pos_y].is_bomb():
                    play_grid[pos_x][pos_y].detonate_bomb(parent_level)

    def detonate_bomb(self, parent_level):
        if self.item_type is 'orange_bomb':
            parent_level.increase_score_by(-40)
            parent_level.orange_bomb_counter = parent_level.orange_bomb_counter - 1
        else:
            parent_level.reduce_current_moves_by(randint(1, 5))
            parent_level.red_bomb_counter = parent_level.red_bomb_counter - 1

        self.change_type_to('empty')

    @staticmethod
    def animate_fall(animation_list, parent_level, fix_once):
        counter = len(animation_list)
        single_time = False

        for item in animation_list:
            counter = counter - 1
            if counter is 0:
                single_time = True
            if item.item_type is 'empty':
                #  Offset calculation  #
                offset = 0
                start_point = animation_list.index(item) + 1
                if not (start_point >= len(animation_list)):
                    for i in range(start_point, len(animation_list)-1):
                        if animation_list[i].item_type is not 'empty':
                            offset = offset + 1
                # Animate #
                item.fall_animation(play_grid[item.pos_x - offset][item.pos_y].get_real_x(),
                                    play_grid[item.pos_x - offset][item.pos_y].get_real_y(),
                                    parent_level, single_time, fix_once, True)
            else:
                #  Drop distance calculation  #
                drop_distance = 0
                start_point = animation_list.index(item) - 1
                if not (start_point < 0):
                    for i in range(start_point, -1, -1):
                        if animation_list[i].item_type is 'empty':
                            drop_distance = drop_distance + 1
                # Animate #
                item.fall_animation(play_grid[item.pos_x + drop_distance][item.pos_y].get_real_x(),
                                    play_grid[item.pos_x + drop_distance][item.pos_y].get_real_y(),
                                    parent_level, single_time, fix_once, False)

    @staticmethod
    def make_animation_list(start_point, column):
        animation_list = []

        for i in range(start_point, -1, -1):
            animation_list.append(play_grid[i][column])
        return animation_list

    @staticmethod
    def play_sound(sound_type):
        if Globals.active_sounds is False:
            return

        if sound_type is 'paper':
            paper_sound.play()
        elif sound_type is 'rock':
            rock_sound.play()
        elif sound_type is 'scissors':
            scissors_sound.play()
        else:
            fail_sound.play()

    def change_type_to(self, item_type):
        self.item_type = item_type
        if item_type is 'empty':
            self.item_button.background_normal = 'Images/black.png'

    def change_place_in_grid_with(self, other):
        global play_grid

        tmp = play_grid[self.pos_x][self.pos_y]
        play_grid[self.pos_x][self.pos_y] = play_grid[other.pos_x][other.pos_y]
        play_grid[other.pos_x][other.pos_y] = tmp
        self.change_x(other)
        self.change_y(other)

    def change_x(self, other):
        global play_grid

        tmp = self.pos_x
        self.pos_x = other.pos_x
        other.pos_x = tmp

    def change_y(self, other):
        global play_grid

        tmp = self.pos_y
        self.pos_y = other.pos_y
        other.pos_y = tmp

    def is_bomb(self):
        if self.item_type is 'orange_bomb' or self.item_type is 'red_bomb':
            return True
        return False

    def get_real_x(self):
        return self.item_button.pos[0]

    def get_real_y(self):
        return self.item_button.pos[1]


class Level:
    score_bar = ProgressBar
    moves_popup = Popup
    score_popup = Popup
    end_game_popup = Popup
    moves_label = Label
    score_label = Label
    total_score_label = Label
    end_game_score_label = Label
    level_victory_score_label = Label
    level_information_from_file = LevelDetermine()
    player = Player()
    starting_moves = 0
    current_score = score_to_beat = 0
    orange_bomb_counter = red_bomb_counter = None
    types = ['rock', 'paper', 'scissors', 'orange_bomb', 'red_bomb']

    def __init__(self):
        if not (self.level_information_from_file.read_next_level()):
            self.check_for_high()
            self.end_game_popup.open()
        self.current_moves = 5 + self.level_information_from_file.extra_moves
        self.starting_moves = self.current_moves
        self.score_to_beat = self.level_information_from_file.score_to_beat

    def load_level(self, area):
        global play_area, play_grid

        play_area = area
        tmp_types = self.types[:]
        self.orange_bomb_counter = self.red_bomb_counter = 0

        for i in range(0, 10):
            for j in range(0, 10):
                item_type = choice(tmp_types)
                self.check_bombs_limitation(item_type, tmp_types)
                item = Item(self, item_type, i, j)
                play_grid[i][j] = item

        self.fix_play_area(False)

    def reduce_current_moves_by(self, moves_lost):
        self.current_moves = self.current_moves - moves_lost
        if self.current_moves < 0:
            self.current_moves = 0
        self.moves_label.text = "[size=25][color=#b40000][b] " + str(self.current_moves) + "[/b][/color][/size]"

    def increase_score_by(self, points):
        self.current_score = self.current_score + points
        if self.current_score < 0:
            self.current_score = 0
        self.score_bar.value = self.current_score
        self.score_label.text = "[size=20][b]" + str(self.current_score) + "[/b][/size]"

    def update_scores_after_level_victory(self):
        self.current_score = self.current_score + self.current_moves * 50
        self.level_victory_score_label.text = str(self.current_moves) + '  X  50  = ' + str(self.current_moves * 50) + \
                                                                        '\nLevel Score:' + str(self.current_score)
        self.player.add_to_total(self.current_score, self.total_score_label)

    def check_for_high(self):
        if shs.high_scores.is_high_score(self.player.total_score):
            if Globals.active_sounds:
                new_high_score.play()
            shs.high_scores.add_high_score(self.player.total_score)
            self.end_game_score_label.text = "[size=25][b]" + "New HighScore!!!\n[/size]" + \
                                             "[size=20]    Final Score:" + str(self.player.total_score) + "[/b][/size]"
        else:
            self.end_game_score_label.text = "[size=20][b]Final Score:" + str(self.player.total_score) + "[/b][/size]"

    def check_endgame(self):
        if self.is_victorious():
            self.update_scores_after_level_victory()
            self.score_popup.open()
            return
        if self.is_defeated():
            self.player.reduce_lives()
            if self.lost_game():
                self.check_for_high()
                self.end_game_popup.open()
            else:
                self.moves_popup.open()

    def is_victorious(self):
        return self.current_score >= self.score_to_beat

    def is_defeated(self):
        return self.current_moves <= 0

    def lost_game(self):
        return self.player.lives <= 0

    def get_starting_moves(self):
        return str(self.starting_moves)

    def set_popup(self, popup, popup_id):
        if popup_id is 'defeat_popup':
            self.moves_popup = popup
        elif popup_id is 'victory_popup':
            self.score_popup = popup
        else:
            self.end_game_popup = popup

    def set_label(self, label, label_id):
        if label_id is 'moves_count':
            self.moves_label = label
        elif label_id is 'score_number':
            self.score_label = label
        elif label_id is 'total_score_number':
            self.total_score_label = label
        elif label_id is 'level_victory_score_label':
            self.level_victory_score_label = label
        else:
            self.end_game_score_label = label

    def set_score_bar(self, progress_bar):
        self.score_bar = progress_bar

    def fix_play_area(self, calculating_points, *largs):      # Destroy self formed triads until no triads are left
        global play_grid, play_area

        Globals.found_triad = False  # Reset to use again in play()
        points_sum = self.gather_points(calculating_points, 0)
        points_sum = points_sum + self.check_until_stable_grid_state(calculating_points, points_sum)

        if calculating_points:
            self.increase_score_by(points_sum)
            self.check_endgame()
        self.load_widgets(play_area)

    def gather_points(self, calculating_points, starting_sum):
        global play_grid
        gather_sum = starting_sum

        for i in range(0, 10):
            for item in play_grid[i]:
                triad = item.check_trinity()
                for triad_item in triad:
                    if triad_item.super_item is True:
                        triad_item.destroy_line(triad_item, triad_item.find_direction(triad), self)
                    triad_item.change_type_to('empty')
                if len(triad) is not 0 and calculating_points:
                    gather_sum = gather_sum + 30

        return gather_sum

    def check_until_stable_grid_state(self, calculating_points, points_sum):
        global play_grid
        final_sum = 0

        while self.check_for_empty_item():
            self.fill_gaps()
            final_sum = final_sum + self.gather_points(calculating_points, points_sum)

        return final_sum

    @staticmethod
    def check_for_empty_item():
        global play_grid

        for i in range(0, 10):
            for item in play_grid[i]:
                if item.item_type is 'empty':
                    return True
        return False

    @staticmethod
    def load_widgets(area):
        area.clear_widgets()
        for i in range(0, 10):
            for item in play_grid[i]:
                area.add_widget(item.item_button)

    def fill_gaps(self):
        global play_grid, play_area
        tmp_types = self.types[:]

        self. check_bombs_availability(tmp_types)

        for i in range(0, 10):              # If you find an empty item drop all the items above it one block
            for item in play_grid[i]:
                if item.item_type is 'empty':
                    random_type = choice(tmp_types)
                    self.check_bombs_limitation(random_type, tmp_types)
                    count = item.pos_x
                    while count > 0:
                        item.change_place_in_grid_with(play_grid[count-1][item.pos_y])
                        count = count-1
                    item.__init__(self, random_type, 0, item.pos_y)
                    play_grid[0][item.pos_y] = item

    def check_bombs_availability(self, tmp_types):
        self.check_orange_bombs_availability(tmp_types)
        self.check_red_bombs_availability(tmp_types)

    def check_bombs_limitation(self, random_type, tmp_types):
        if random_type is 'orange_bomb':
            self.orange_bomb_counter = self.orange_bomb_counter + 1
            self.check_orange_bombs_availability(tmp_types)
        if random_type is 'red_bomb':
            self.red_bomb_counter = self.red_bomb_counter + 1
            self.check_red_bombs_availability(tmp_types)

    def check_orange_bombs_availability(self, tmp_types):
        if self.orange_bomb_counter is self.level_information_from_file.orange_bomb_threshold:
            tmp_types.remove('orange_bomb')

    def check_red_bombs_availability(self, tmp_types):
        if self.red_bomb_counter is self.level_information_from_file.red_bomb_threshold:
            tmp_types.remove('red_bomb')
