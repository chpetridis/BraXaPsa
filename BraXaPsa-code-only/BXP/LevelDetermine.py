
class LevelDetermine:
    red_bomb_threshold = orange_bomb_threshold = 0      # Information to be passed on Level class
    extra_moves = score_to_beat = 0                     # Information to be passed on Level class
    levels_file = open("BXP/LevelData.txt", "r")

    def read_next_level(self):
        """ False indicates that player reached the final level and beat it
            True indicates that there are still more levels to be played
        """
        line = self.levels_file.readline()
        if not line:
            return False

        #  Pass the information #
        data = line.split(" ")
        self.extra_moves = int(data[0])
        self.score_to_beat = int(data[1])
        self.orange_bomb_threshold = int(data[2])
        self.red_bomb_threshold = int(data[3])
        return True

    def reset_file(self):       # Go to beginning of file to start over level 1 again
        self.levels_file.seek(0, 0)
