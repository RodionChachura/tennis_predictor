import sqlite3
import os

SQL_PATH = '../data/'
SQL_NAME = 'tennis'


class DataKeeper:
    def __init__(self, path=SQL_PATH, name=SQL_NAME):
        db_name = name + '.db'
        db = os.path.join(path, db_name)
        self.connection = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            create table if not exists players (
                id          integer               PRIMARY KEY,
                name        text                  not null,
                dob         timestamp,
                hand        text,
                rank_points real              
            )''')

        self.cursor.execute('''
            create table if not exists matches (
                date                timestamp,
                score               text,
                
                winner_id           integer    not null,
                winner_rank_points  real,

                loser_id            integer    not null,
                loser_rank_points   real,

                FOREIGN KEY (winner_id) REFERENCES players (id),
                FOREIGN KEY (loser_id)  REFERENCES players (id)
            )''')

        self.connection.commit()

    def add_player(self, player):
        self.cursor.execute(
            'insert into players values (?, ?, ?, ?, ?)',
            (
                player.id,
                player.name,
                player.dob,
                player.hand,
                player.rank_points
            )
        )
        self.connection.commit()

    def add_match(self, match):
        self.cursor.execute(
            'insert into matches values (?, ?, ?, ?, ?, ?)',
            (
                match.date,
                match.score,
                match.winner.id,
                match.winner.rank_points,
                match.loser.id,
                match.loser.rank_points,
            )
        )
        self.connection.commit()