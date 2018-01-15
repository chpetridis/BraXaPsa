
class Player:
    lives = 3
    total_score = 0

    def add_to_total(self, level_score, total_score_label):     # Add score and update the GUI
        self.total_score = self.total_score + level_score
        total_score_label.text = str(self.total_score)

    def reduce_lives(self):
        self.lives = self.lives - 1
