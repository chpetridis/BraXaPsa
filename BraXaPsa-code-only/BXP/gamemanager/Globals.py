"""  Used for Globals that communicate with a lot of files """


class Globals:
    active_sounds = True     # Checking if sounds are on/off
    sounds = []              # List of all the sounds in game
    hold = True              # for synchronization between Item objects (used in both swap() and play())
    found_triad = False      # for checking if no one found triad in play()
