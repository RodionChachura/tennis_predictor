import re

def score_to_ratio(score):
  pattern = re.compile('^[0|1|2|3|4|5|6|7|8|9|\-|\ |\(|\)]+$')
  if not pattern.match(score): return

  winner_points = 0
  loser_points = 0

  for couple in score.split():
    points = points = list(map(int, couple.replace('(', ' ').replace(')', ' ').replace('-', ' ').split()))
    winner_points += points[0]
    loser_points += points[1]
    if (len(points) == 3):
      if (points[2] > points[0]):
        winner_points += points[0] + 2
        loser_points += points[2]
      else:
        winner_points += points[0]
        loser_points += points[2]
  
  return winner_points / loser_points if loser_points > 0 else winner_points

def hand_to_int(hand):
  mapper = {
    'R': 0,
    'L': 1,
    'U': 2
  }

  return mapper[hand]