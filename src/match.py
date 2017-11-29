class Match:
    def __init__(self, date, score, winner, loser):
        self.date = date
        self.score = score
        self.winner = winner
        self.loser = loser
        self.hash = int(date) + winner.id + loser.id
        self.players = [ winner, loser ]

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self,):
        return self.hash