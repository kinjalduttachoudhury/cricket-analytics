import os
import sqlite3
import json

from configs import DML
from pydantic import ValidationError
from models.match_results import MatchResult
from models.match_ball_by_ball import MatchBallByBall
from utils.base_logger import logger


def get_parsed_data_player_universe(data):
    """
    This function parses json data and returns list of players for each match
    :param data: contents of json files related to match info
    :type data: dict
    :rtype: list
    """
    values = []
    match_type = data['match_type']
    match_type_number = data['match_type_number']
    match_date = data['dates'][0]
    gender = data['gender']
    for team in data['teams']:
        for name, unique_id in data['registry']['people'].items():
            if name in data['players'][team]:
                values.append([match_type, match_type_number, match_date, team, gender, name, unique_id])

    return values


def get_parsed_data_match_ball_by_ball(data):
    """
    This function parses json data and returns ball by ball data for every inning
    :param data: contents of json files
    :type data: dict
    :rtype: list
    """
    values = []
    try:
        matchBallByBall = MatchBallByBall(**data)
    except ValidationError as e:
        logger.error(e.json())

    for inning in matchBallByBall.innings:
        for over in inning.overs:
            for delivery in over.deliveries:
                wicket_player_out = delivery.wickets[0].player_out if delivery.wickets else None
                wicket_kind = delivery.wickets[0].kind if delivery.wickets else None
                wicket_fielder_involved = delivery.wickets[0].fielders[0].name if delivery.wickets and delivery.wickets[
                    0].fielders else None

                extras_byes = delivery.extras.byes if delivery.extras and delivery.extras.byes else None
                extras_legbyes = delivery.extras.legbyes if delivery.extras and delivery.extras.legbyes else None
                extras_noballs = delivery.extras.noballs if delivery.extras and delivery.extras.noballs else None
                extras_penalty = delivery.extras.penalty if delivery.extras and delivery.extras.penalty else None
                extras_wides = delivery.extras.wides if delivery.extras and delivery.extras.wides else None

                values.append([matchBallByBall.info.match_type, matchBallByBall.info.match_type_number,
                               matchBallByBall.info.dates[0], inning.team,
                               [team for team in matchBallByBall.info.teams if team != inning.team][0], over.over,
                               delivery.batter, delivery.bowler, delivery.non_striker, delivery.runs.batter,
                               delivery.runs.extras, delivery.runs.non_boundary, delivery.runs.total, wicket_player_out,
                               wicket_kind, wicket_fielder_involved, extras_byes, extras_legbyes, extras_noballs,
                               extras_penalty, extras_wides, inning.target.overs if inning.target else None,
                               inning.target.runs if inning.target else None])

    return values


def get_parsed_data_match_results(data):
    """
    This function parses json data and returns data related to outcome of every match
    :param data: contents of json files related to match info
    :type data: dict
    :rtype: list
    """
    try:
        matchResult = MatchResult(**data)
    except ValidationError as e:
        logger.error(e.json())

    return [
        matchResult.match_type,
        matchResult.match_type_number,
        matchResult.dates[0],
        matchResult.season,
        matchResult.gender,
        matchResult.event.name if matchResult.event else None,
        matchResult.event.match_number if matchResult.event else None,
        matchResult.teams[0],
        matchResult.teams[1],
        matchResult.venue,
        matchResult.toss.winner,
        matchResult.toss.decision,
        matchResult.outcome.winner,
        matchResult.outcome.by.runs if matchResult.outcome.by else None,
        matchResult.outcome.by.wickets if matchResult.outcome.by else None,
        matchResult.outcome.result,
        matchResult.outcome.method
    ]


def insert_data_to_tables(path, db_file):
    """
    This function uploads data from json files to SQLite database after parsing them.
    The json files are deleted after their content is uploaded to the database.
    :param path: path to directory with json files
    :type path: str
    :param db_file: path of the database file for SQLite
    :type db_file: str
    """
    files = [file for file in os.listdir(path) if file.endswith('.json')]

    connection_obj = sqlite3.connect(db_file)

    for file in files:
        with open("{path}{file}".format(path=path, file=file), 'r') as json_file:
            data = json.load(json_file)
            for table in DML.dml_config.keys():
                try:
                    if table == 'match_results':
                        values = get_parsed_data_match_results(data['info'])
                        insert_query = "insert into {table} ({columns}) values(?{placeholder})".format(
                            table=table, columns=", ".join(DML.dml_config[table]), placeholder=",?" * (len(values) - 1))

                        connection_obj.execute(insert_query, values)

                        logger.info("File - {file} -> Match type - {match_type}, Match type number - {match_type_number}, Date - {date}".\
                                     format(file=file, match_type=values[0], match_type_number=values[1], date=values[2]))

                    if table == 'match_ball_by_ball':
                        values = get_parsed_data_match_ball_by_ball(data)
                        insert_query = "insert into {table} ({columns}) values(?{placeholder})".format(
                            table=table, columns=", ".join(DML.dml_config[table]), placeholder=",?" * (len(values[0]) - 1))
                        connection_obj.executemany(insert_query, values)

                    if table == 'player_universe':
                        values = get_parsed_data_player_universe(data['info'])
                        insert_query = "insert into {table} ({columns}) values(?{placeholder})".format(
                            table=table, columns=", ".join(DML.dml_config[table]), placeholder=",?" * (len(values[0]) - 1))
                        connection_obj.executemany(insert_query, values)
                except Exception as e:
                    logger.exception(e)
                    connection_obj.close()
                    raise
                else:
                    connection_obj.commit()
        os.remove("{path}{file}".format(path=path, file=file))

    connection_obj.close()
    logger.info("Data inserted for {counter} files".format(counter=len(files)))


if __name__ == "__main__":
    path_to_files = '../data/'
    db_file = '../cricket-analytics-sqlite.db'
    insert_data_to_tables(path_to_files, db_file)
