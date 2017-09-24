from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class HighScores:
    high_scores_file = open("BXP/HighScores.txt", "r+")
    high_scores = []
    high_scores_layout = BoxLayout  # for GUI interaction

    def __init__(self):
        self.high_scores = self.high_scores_file.read().splitlines()    # Read file and keep the data
        self.high_scores_file.seek(0, 0)                                # Go to beginning of file

    def load_high_scores(self):                     # Load High Scores in GUI view
        self.high_scores_layout.clear_widgets()
        for i in range(0, 10):
            label = Label(text="[size=30][b]" + self.high_scores[i] + "[/b][/size]", markup=True)
            self.high_scores_layout.add_widget(label)

    def is_high_score(self, score):
        if score > int(self.high_scores[9]):
            return True
        return False

    def set_high_scores_number_layout(self, layout):    # Set the layout for the interaction with GUI
        self.high_scores_layout = layout

    def add_high_score(self, score):
        for i in range(0, 10):
            if score > int(self.high_scores[i]):
                for j in range(9, i, -1):
                    self.high_scores[j] = self.high_scores[j - 1]
                self.high_scores[i] = str(score)
                self.load_high_scores()
                self.update_file()
                break

    def update_file(self):
        for i in range(0, 10):
            if i is not 9:
                self.high_scores_file.write(self.high_scores[i] + "\n")
            else:
                self.high_scores_file.write(self.high_scores[i])
        self.high_scores_file.seek(0, 0)
        self.high_scores_file.flush()
