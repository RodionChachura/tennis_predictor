import sqlite3
import os

SQL_PATH = '.'
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
                winner_age          real,

                loser_id            integer    not null,
                loser_rank_points   real,
                loser_age           real,

                FOREIGN KEY (winner_id) REFERENCES players (id),
                FOREIGN KEY (loser_id)  REFERENCES players (id)
            )''')

        self.connection.commit()

    def create_player(self):
        pass

    def poppulate(self, players, matches):
        pass