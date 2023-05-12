import sys
import json
import datetime
import os

from decimal import *
from lib.response import *
from models.uploads import *
from models.builds import *
from models.matches import *
from models.rounds import *
from models.round_players import *
from models.round_player_scores import *
from models.round_player_medals import *
from models.round_player_damages import *

from lib.database import *
from sqlalchemy.exc import SQLAlchemyError


def upload_matches(data, context):
    try:
        body = json.loads(data.get('body'))
    except json.JSONDecodeError:
        return build_response(400, "Invalid JSON, upload aborted")
    except UnicodeDecodeError as e:
        return build_response(400, "Invalid encoding, upload aborted")

    uploader = body.get('uploader_uid')
    if uploader is None:
        return build_response(400, "Missing uploader_uid, upload aborted")

    db = Database()

    build_list = body.get('build_list', [])
    match_list = body.get('match_list', [])

    try:
        uploader = int(uploader)

        upload_build_list(db, build_list)
        process_match_list(db, uploader, match_list)

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return build_response(500, f"Internal Server Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        db.rollback()
        return build_response(500, f"An unexpected error occurred: {str(e)}")
    finally:
        db.close()

    return build_upload_response(get_uploads_by_user(db, uploader))


def process_match_list(db, uploader, match_list):
    print("process_match_list")
    uploaded_matches = set(get_uploads_by_user(db, uploader))
    for match in match_list:
        if match['match_id'] not in uploaded_matches:
            print("upload_upload_record")
            upload_upload_record(db, match, uploader)
            print("upload_match")
            upload_match(db, match)
            for round in match['rounds']:
                round_id = upload_round(db, match, round)
                for player in round['players']:
                    round_player_id = upload_round_players(
                        db, match, round_id, player)
                    upload_round_player_scores(
                        db, round_player_id, player['scores'])
                    upload_round_player_medals(
                        db, round_player_id, player['medals'])
                    upload_round_player_damages(
                        db, player['uid'], round_player_id, round['damage_records'])
