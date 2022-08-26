import json
import boto3
import datetime

from decimal import *
from classes.decoder import *
from classes.player_profile import *
from profile import find_uploaded_matches_for_user_id
from lib.item_definitions import get_item_dict
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
table = dynamodb.Table('xodat')
queue = []
uploader = 0
players = {}

def upload_matches(event, context):
    uploader = event['uploader_uid']
    previously_uploaded_match = find_uploaded_matches_for_user_id(uploader)
    item_dict = get_item_dict()

    # with table.batch_writer(overwrite_by_pkeys=['partition_key', 'sort_key']) as batch:
    for build in event['build_list']:
        upload_build(build)

    for match in event['match_list']:
        if match['match_id'] not in previously_uploaded_match:
            upload_match(match)

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(queue, default=vars)
    }

def upload_match(match):
    for round in match['rounds']:
        roundID = str(round['round_start'])
        for player in round['players']:
            upload_player_round_attributes(roundID, match, round, player)
    return 

def upload_upload_record(match):
    item = {
        'pk': 'USER#' + str(uploader),
        'sk': 'UPLOAD#' + str(match['match_id'])
    }
    queue.append(item)
    return

def build_player_profile(match, round, player):
    if player['uid'] in players:
        profile = players[player['uid']]
        profile.uploads += 1 if uploader == player['uid'] else 0
        profile.games += 1
        profile.rounds += 1
        profile.duration += (datetime.datetime.strptime(round['round_end'], '%Y-%m-%dT%H:%M:%S.%fZ') -datetime.datetime.strptime(round['round_start'], '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds()
        profile.kills += player['kills']
        profile.assists += player['assists']
        profile.drone_kills += player['drone_kills']
        profile.deaths += player['deaths']
        profile.score += player['score']
        profile.damage += player['damage']
        profile.cabin_damage += player['cabin_damage']
        profile.damage_recieved += player['damage_taken']

        if player['kills'] >  profile.max_kills:
            profile.max_kills = player['kills']

        if player['assists'] >  profile.max_assists:
            profile.max_assists = player['assists']

        if player['drone_kills'] >  profile.max_drone_kills:
            profile.max_drone_kills = player['drone_kills']
        
        if player['deaths'] >  profile.max_deaths:
            profile.max_deaths = player['deaths']

        if player['score'] >  profile.max_score:
            profile.max_score = player['score']

        if player['damage'] >  profile.max_damage:
            profile.max_damage = player['damage']
        
        if player['cabin_damage'] >  profile.max_cabin_damage:
            profile.max_cabin_damage = player['cabin_damage']

        if player['damage_taken'] >  profile.max_damage_recieved:
            profile.max_damage_recieved = player['damage_taken']

        if round['round_id'] == 0:
            if round['winning_team'] == -1 or round['team'] <= 0:
                profile.unfinished += 1
            elif round['winning_team'] == 0:
                profile.draws += 1
            elif round['winning_team'] == round['team']:
                profile.wins += 1
            else:
                profile.losses += 1

        if round['round_winning_team'] == -1 or round['team'] <= 0:
            profile.round_unfinished += 1
        elif round['round_winning_team'] == 0:
            profile.round_draws += 1
        elif round['round_winning_team'] == round['team']:
            profile.round_wins += 1
        else:
            profile.round_losses += 1
    else:
        profile = player_profile()
        profile.uid = player['uid']
        profile.nickname = player['nickname']
        profile.match_type = match['match_type']
        profile.uploads = 1 if uploader == player['uid'] else 0
        profile.games = 1
        profile.rounds = 1
        profile.duration = (datetime.datetime.strptime(round['round_end'], '%Y-%m-%dT%H:%M:%S.%fZ') -datetime.datetime.strptime(round['round_start'], '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds()
        profile.wins = 0
        profile.losses = 0 
        profile.draws = 0
        profile.unfinished = 0
        profile.round_wins = 0
        profile.round_losses = 0
        profile.round_draws = 0
        profile.round_unfinished = 0
        profile.mmr = 1600
        profile.kills = player['kills']
        profile.assists = player['assists']
        profile.drone_kills = player['drone_kills']
        profile.deaths = player['deaths']
        profile.score = player['score']
        profile.damage = player['damage']
        profile.cabin_damage = player['cabin_damage']
        profile.damage_recieved = player['damage_taken']
        profile.max_kills = player['kills']
        profile.max_assists = player['assists']
        profile.max_drone_kills = player['drone_kills']
        profile.max_deaths = player['deaths']
        profile.max_score = player['score']
        profile.max_damage = player['damage']
        profile.max_cabin_damage = player['cabin_damage']
        profile.max_damage_recieved = player['damage_taken']
        players.append(player['uid'], profile)

        if round['winning_team'] == -1 or round['team'] <= 0:
            profile.unfinished = 1
        elif round['winning_team'] == 0:
            profile.draws = 1
        elif round['winning_team'] == round['team']:
            profile.wins = 1
        else:
            profile.losses = 1

        if round['round_winning_team'] == -1 or round['team'] <= 0:
            profile.round_unfinished = 1
        elif round['round_winning_team'] == 0:
            profile.round_draws = 1
        elif round['round_winning_team'] == round['team']:
            profile.round_wins = 1
        else:
            profile.round_losses = 1

def upload_player_round_attributes(roundID, match, round, player):

    build_player_profile(match, round, player)
    
    item = {
        'pk': 'ROUND#' + str(roundID),
        'sk': 'USER#' + str(player['uid']),
        'match_id' : player['match_id'],
        'round_id' : roundID,
        'bot' : player['bot'],
        'nickname' : player['nickname'],
        'team' : player['team'],
        'build_hash' : player['build_hash'],
        'power_score' : player['power_score'],
        'kills' : player['kills'],
        'assists' : player['assists'],
        'drone_kills' : player['drone_kills'],
        'deaths' : player['deaths'],
        'score' : player['score'],
        'damage' : str(player['damage']),
        'cabin_damage' : str(player['cabin_damage']),
        'damage_taken' : str(player['damage_taken']),
        'scores' : player['scores'],
        'medals' : player['medals'],
        'round_start' : round['round_start'],
        'round_end' : round['round_end'],
        'round_winning_team' : round['winning_team'],
        'match_type' : match['match_type'],
        'match_classification' : match['match_classification'],
        'match_start' : match['match_start'],
        'match_end' : match['match_end'],
        'map_name' : match['map_name'],
        'map_display_name' : match['map_display_name'],
        'match_winning_team' : match['winning_team'],
        'win_condition' : match['win_conidtion'],
        'client_version' : match['client_version'],
        'co_driver_version' : match['co_driver_version'],
        'host_name' : match['host_name'],
        'resources' : match['resources']
    }
    queue.append(item)
    return

def upload_build(build):
    item = {
        'pk': 'BUILD#' + str(build['build_hash']),
        'sk': 'POWER_SCORE#' + str(build['power_score']),
        'parts' : build['parts']
    }
    queue.append(item)
    return 