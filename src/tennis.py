import os
import logging
from datetime import datetime

from .data_keeper import DataKeeper
from .csv_helper import csv_to_dicts, csv_to_lists, get_matches_csvs
from .match import Match
from .player import Player
from .rank import Rank
from .logger import setup_logger
from .utils import years_from_timestamp
from .constants import CSVS, LAST_RANKS_CSV, PLAYERS_CSV, DATA_LOCATION

logger = logging.getLogger(__name__)
setup_logger()

START_YEAR = 2000
END_YEAR = 2017

def get_database_from_csv(start_year=START_YEAR, end_year=END_YEAR):
    years = range(start_year, end_year)
    all_files = []
    for year in years:
        all_files += get_matches_csvs(year)

    ranks = {}
    for fields in csv_to_lists(LAST_RANKS_CSV):
        date = datetime.strptime(fields[0][:4] + '/' + fields[0][4:-2] + '/' + fields[0][:2], '%Y/%m/%d')
        player_id = int(fields[2])
        rank_points = int(fields[3])
        rank = Rank(player_id, date, rank_points)

        exist = player_id in ranks
        if (exist and ranks[player_id].date < date) or not exist:
            ranks[player_id] = rank
    
    db = DataKeeper()

    logger.error('ranks: ' + str(len(ranks)))
    players = {}
    problematic_players = 0
    no_rank_players = 0  
    for fields in csv_to_lists(PLAYERS_CSV):
        needed_fields = fields[:-1]
        if len(needed_fields) < 5 or any(map(lambda x: len(x) < 1, fields)):
            problematic_players += 1
            continue
        player_id = int(needed_fields[0])
        player_name = needed_fields[1] + ' ' + needed_fields[2]
        player_dob = int(needed_fields[4])
        rank_points = ranks[player_id].rank_points if player_id in ranks else None
        if rank_points is None:
            # logger.error('''Player doesn't have rank
            #     id: {0}
            #     name: {1}
            #     age: {2}
            # '''.format(player_id, player_name, years_from_timestamp(player_dob)))
            no_rank_players += 1
        players[player_id] = Player(
            player_id,
            player_name,
            player_dob,
            needed_fields[3],
            rank_points
        )

    logger.error('normal: ' + str(len(players)))
    logger.error('problematic: ' + str(problematic_players))
    logger.error('no rank: ' + str(no_rank_players))
    for player in players.values():
        db.add_player(player)

    matches = []
    for csv_file in all_files:
        for match in csv_to_dicts(csv_file):
            winner_id = int(match['winner_id'])
            loser_id = int(match['loser_id'])
            winner = players.get(winner_id)
            loser = players.get(loser_id)

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


    for match in matches:
        db.add_match(match)

    return db


def predict(one_name, other_name):
    db = DataKeeper()
    one = db.get_player_by_name(one_name)
    other = db.get_player_by_name(other_name)
    one_matches = db.get_player_matches(one.id)
    other_matches = db.get_player_matches(other.id)
    logger.error('one matches: ' + str(len(one_matches)) + ' other matches: ' + str(len(other_matches)))
    return {
        'train_set_length': 0,
        'train_set_thrown_data_persentage': 0,
        'score': 0
    }
