import os
import sqlite3

SQL_PATH = '.'
SQL_NAME = 'tennis'

def create_db(path=SQL_PATH, name=SQL_NAME):
    db_name = name + '.db'
    db = os.path.join(path, db_name)
    connection = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    
    cursor.execute('''
        create table if not exists players (
          id        integer               PRIMARY KEY,
          name      text                  not null,
          dob       timestamp,
          hand      text
        )'''
    )
    
    cursor.execute('''
        create table if not exists matches (
            date        timestamp,
            score       text,
            
            winner_id   integer    not null,
            winner_rank real,
            winner_age  integer,

            loser_id    integer    not null,
            loser_rank  real,
            loser_age   integer,

            FOREIGN KEY (winner_id) REFERENCES players (id),
            FOREIGN KEY (loser_id)  REFERENCES players (id)
        )'''
      )
    
    connection.commit()

    return {
        'cursor': cursor,
        'connection': connection
    }


def predict(one, other):
    return {
        'train_set_length': 0,
        'train_set_thrown_data_persentage': 0,
        'score': 0
    }
