from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable', False)      # Has to be here or won't work
from BXP.ScreenMenu import ScreenMenu
from BXP.ScreenPlay import ScreenPlay
from BXP.HowToPlayScreen import HowToPlayScreen
from BXP.ScreenHighScores import ScreenHighScores
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import WipeTransition


class BraXaPsaApp(App):

    def build(self):

        self.icon = 'Images/app_image.png'
        sm = ScreenManager(transition=WipeTransition())

        #  Create the 4 Screens #
        menu_screen = ScreenMenu(name='menu')
        menu_screen.set_screen_manager(sm)
        play_screen = ScreenPlay(name='play')
        play_screen.set_screen_manager(sm)
        high_scores_screen = ScreenHighScores(name='high_scores')
        high_scores_screen.set_screen_manager(sm)
        how_to_play_screen = HowToPlayScreen(name='how_to_play')
        how_to_play_screen.set_screen_manager(sm)

        #  Add Screens in the Screen Manager widget #
        sm.add_widget(menu_screen)
        sm.add_widget(play_screen)
        sm.add_widget(high_scores_screen)
        sm.add_widget(how_to_play_screen)

        return sm

if __name__ == '__main__':
    Window.size = (800, 600)
    BraXaPsaApp().run()
