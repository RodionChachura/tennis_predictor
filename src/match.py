from random import choice
from .converter import score_to_ratio, hand_to_int

class Match:
    def __init__(self, date, score, winner, loser):
        self.date = date
        self.score = score
        self.winner = winner
        self.loser = loser
        self.hash = int(date) + winner.id + loser.id
        self.players = [ winner, loser ]

    def to_ml_data_label(self):
        first_winner = choice([True, False])
        ratio = score_to_ratio(self.score)
        if ratio is None: return None, None

        data = self.winner.get_ml_data() + self.loser.get_ml_data() if first_winner else self.loser.get_ml_data() + self.winner.get_ml_data()
        label = ratio if first_winner else 1 / ratio

        return data, label

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self,):
        return self.hash