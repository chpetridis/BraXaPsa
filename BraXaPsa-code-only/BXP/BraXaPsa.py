from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable', False)      # Has to be here or won't work
from BXP.ScreenFactory import ScreenFactory
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import WipeTransition


class BraXaPsaApp(App):

    def build(self):
        sm = ScreenManager(transition=WipeTransition())
        factory = ScreenFactory()

        # Create Screens #
        menu_screen = factory.create_screen(sm, 'menu')
        play_screen = factory.create_screen(sm, 'play')
        high_scores_screen = factory.create_screen(sm, 'high_scores')
        how_to_play_screen = factory.create_screen(sm, 'how_to_play')

        #  Add Screens in the Screen Manager widget #
        sm.add_widget(menu_screen)
        sm.add_widget(play_screen)
        sm.add_widget(high_scores_screen)
        sm.add_widget(how_to_play_screen)

        return sm

if __name__ == '__main__':
    Window.size = (800, 600)
    BraXaPsaApp().run()
