import sqlite3
import os
import logging

from .player import Player
from .match import Match
from .constants import DATA_LOCATION, SQL_NAME

logger = logging.getLogger(__name__)

class DataKeeper:
    def __init__(self, path=DATA_LOCATION, name=SQL_NAME):
        db_name = name + '.db'
        db = os.path.join(path, db_name)
        self.connection = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            create table if not exists players (
                id          integer               PRIMARY KEY,
                name        text                  not null,
                dob         integer,
                hand        text,
                rank_points real              
            )''')

        self.cursor.execute('''
            create table if not exists matches (
                date                integer,
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
    
    def get_player_by_id(self, id):
        return Player(
            *self._get_one(
                'select * from players where id=?',
                (id,)
            )
        )

    def get_player_by_name(self, name):
        return Player(
            *self._get_one(
                'select * from players where name=?',
                (name,)
            )
        )

    def _match_entry_to_match(self, match_entry):
        winner = self.get_player_by_id(match_entry[2]).with_other_rank_points(match_entry[3])
        loser = self.get_player_by_id(match_entry[4]).with_other_rank_points(match_entry[5])

        return Match(match_entry[0], match_entry[1], winner, loser)

    def get_player_won_matches(self, player_id):
        return list(
            map(
                self._match_entry_to_match,
                self._get_all(
                    'select * from matches where winner_id=?',
                    (player_id,)
                )
            )
        )

    def get_player_losed_matches(self, player_id):
        return list(
            map(
                self._match_entry_to_match,
                self._get_all(
                    'select * from matches where loser_id=?',
                    (player_id,)
                )
            )
        )

    def get_player_matches(self, player_id):
        return self.get_player_losed_matches(player_id) + self.get_player_losed_matches(player_id)

    def _get_one(self, sql, tuples):
        self.cursor.execute(sql, tuples)
        return self.cursor.fetchone()

    def _get_all(self, sql, tuples):
        self.cursor.execute(sql, tuples)
        return self.cursor.fetchall()