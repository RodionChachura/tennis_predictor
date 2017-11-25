import os
import logging

from .data_keeper import DataKeeper
from .csv_helper import csv_to_dicts, csv_to_lists, get_matches_csvs
from .match import Match
from .player import Player
from .rank import Rank
from .logger import setup_logger
from .utils import years_from_timestamp
from .constants import CSVS, LAST_RANKS_CSV, PLAYERS_CSV

logger = logging.getLogger(__name__)
setup_logger()

START_YEAR = 2000
END_YEAR = 2017
DATA_LOCATION = os.path.abspath('./data/')

def get_database_from_csv(start_year=START_YEAR, end_year=END_YEAR):
    logger.error(os.path.abspath(CSVS))
 
    years = range(start_year, end_year)
    all_files = []
    for year in years:
        all_files += get_matches_csvs(year)

    ranks = []
    for fields in csv_to_lists(LAST_RANKS_CSV):
        date = fields[0][:4] + '/' + fields[0][4:-2] + '/' + fields[0][:2]
        player_id = fields[2]
        rank_points = fields[3]
        rank = Rank(player_id, date, rank_points)

        player_rank_already_exists = False
        to_remove = None
        for r in ranks:
            if r.player_id == player_id:
                player_rank_already_exists = True
                if r.date < date:
                    to_remove = r
        if to_remove is not None:
            ranks.remove(to_remove)
        if (player_rank_already_exists and to_remove) or not player_rank_already_exists:
            ranks.append(rank)

    players = []
    for fields in csv_to_lists(PLAYERS_CSV):
        player_id = fields[0]
        player_name = fields[1] + ' ' + fields[2]
        player_dob = fields[4]
        player_rank = None
        for rank in ranks:
            if rank.player_id == player_id:
                player_rank = rank
        if player_rank is None:
            logger.error('''Player doesn't have rank
                id: {0}
                name: {1}
                age: {2}
            '''.format(player_id, player_name, years_from_timestamp(player_dob)))
            continue

        players.append(
            Player(
                player_id,
                player_name,
                fields[4],
                fields[3],
                player_rank.rank_points
            )
        )

    matches = []
    for csv_file in all_files:
        for match in csv_to_dicts(csv_file):
            winner_id = match['winner_id']
            loser_id = match['loser_id']
            winner = None
            loser = None
            for player in players:
                if player.id == winner_id:
                    winner = player
                if player.id == loser_id:
                    loser = player
            if loser is None or winner is None:
                logger.error('No loser or winner')
                continue

            matches.append(
                Match(
                    match['tourney_date'],
                    match['score'],
                    winner.with_other_rank_points(match['winner_rank_points']),
                    loser.with_other_rank_points(match['loser_rank_points'])
                )
            )

    db = DataKeeper()
    for player in players:
        db.add_player(player)
    for match in matches:
        db.add_match(match)

    return db

def predict(one, other):
    return {
        'train_set_length': 0,
        'train_set_thrown_data_persentage': 0,
        'score': 0
    }