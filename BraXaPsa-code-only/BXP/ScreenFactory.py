from BXP.ScreenMenu import ScreenMenu
from BXP.ScreenPlay import ScreenPlay
from BXP.HowToPlayScreen import HowToPlayScreen
from BXP.ScreenHighScores import ScreenHighScores


class ScreenFactory:

    @staticmethod
    def create_screen(sm, screen_name):
        if screen_name is 'menu':
            screen = ScreenMenu(name=screen_name)
        elif screen_name is 'play':
            screen = ScreenPlay(name=screen_name)
        elif screen_name is 'high_scores':
            screen = ScreenHighScores(name=screen_name)
        elif screen_name is 'how_to_play':
            screen = HowToPlayScreen(name=screen_name)
        else:
            return None

        screen.set_screen_manager(sm)
        return screen
