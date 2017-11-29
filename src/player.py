class Player:
    def __init__(self, id, name, dob, hand='U', rank_points=None):
        self.id = id
        self.name = name
        self.dob = dob
        self.hand = hand
        self.rank_points = rank_points
    
    def with_other_rank_points(self, rank_points):
        return Player(
            self.id,
            self.name,
            self.dob,
            self.hand,
            rank_points
        )
    
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id