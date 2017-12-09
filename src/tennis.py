import os
import logging
from datetime import datetime
import time

from .data_keeper import DataKeeper
from .csv_helper import csv_to_dicts, csv_to_lists, get_matches_csvs
from .match import Match
from .player import Player
from .rank import Rank
from .logger import setup_logger
from .constants import CSVS, LAST_RANKS_CSV, PLAYERS_CSV, DATA_LOCATION
from .ml import get_forest_reg

logger = logging.getLogger(__name__)
setup_logger()

START_YEAR = 2000
END_YEAR = 2017

def csv_date_to_timestamp(csv_date):
    return int(time.mktime(datetime.strptime(csv_date[:4] + '/' + csv_date[4:-2] + '/' + csv_date[:2], '%Y/%m/%d').timetuple()))


def get_database_from_csv(start_year=START_YEAR, end_year=END_YEAR):
    years = range(start_year, end_year)
    all_files = []
    for year in years:
        all_files += get_matches_csvs(year)

    ranks = {}
    for fields in csv_to_lists(LAST_RANKS_CSV):
        date = csv_date_to_timestamp(fields[0])
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
        player_dob = csv_date_to_timestamp(needed_fields[4])
        rank_points = ranks[player_id].rank_points if player_id in ranks else None
        if rank_points is None:
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


def matches_players(matches):
    players = {}
    for match in matches:
        for player in match.players:
            if player.id not in players:
                players[player.id] = player

    return players

def get(unvisited_players, visited_players, get_player_matches, matches):
    player = unvisited_players[-1]
    new_matches = matches[:]
    new_unvisited_players = [x for x in unvisited_players if x != player]
    
    for match in get_player_matches(player):
        skip_match = False
        for player in match.players:
            if player in visited_players:
                if player not in new_unvisited_players:
                    new_unvisited_players.append(player)
                skip_match = True
                continue
        if not skip_match:
            new_matches.append(match)

    return (new_unvisited_players, new_matches)

def all_clustered_matches(db, one_player, other_player):
    unvisited_players = [ one_player, other_player ]
    visited_players = []
    matches = []
    while(len(unvisited_players) > 0):
        visited_players.append(unvisited_players.pop())
        for match in db.get_player_matches(one_player.id):
            skip_match = False
            for player in match.players:
                if player in visited_players:
                    skip_match = True
                    continue
                elif player not in unvisited_players:
                    unvisited_players.append(player)
            if not skip_match:
                matches.append(match)

    return matches
    


def predict(one_name, other_name):
    db = DataKeeper()
    one = db.get_player_by_name(one_name)
    other = db.get_player_by_name(other_name)
    cluster_matches = all_clustered_matches(db, one, other)
    data = []
    labels = []
    for match in cluster_matches:
        d, l = match.to_ml_data_label()
        
        no_points = False
        if d is None: continue
        for el in d:
            if el == '':
                no_points = True
        if no_points: continue
        data.append(d)
        labels.append(l)
    
    regressor = get_forest_reg(data, labels)
    prediction = regressor.predict([one.get_ml_data() + other.get_ml_data()])

