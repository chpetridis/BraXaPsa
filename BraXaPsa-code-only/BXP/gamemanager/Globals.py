"""  Used for Globals that communicate with a lot of files """


class Globals:
    active_sounds = True
    sounds = []
    hold = True              # for synchronization between Item objects (used in both swap() and play())
    found_triad = False
