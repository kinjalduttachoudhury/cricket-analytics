ddl_config = {
    "match_results":
        [
            "match_type varchar",
            "match_type_number integer",
            "match_date date",
            "season varchar",
            "gender varchar",
            "event_name varchar",
            "event_match_number integer",
            "team1 varchar",
            "team2 varchar",
            "venue varchar",
            "toss_winner varchar",
            "toss_decision varchar",
            "winner varchar",
            "win_by_runs integer",
            "win_by_wickets integer",
            "outcome_result varchar",
            "outcome_method varchar"
        ]
    ,
    "match_ball_by_ball":
        [
            "match_type varchar",
            "match_type_number integer",
            "match_date date",
            "batting_team varchar",
            "fielding_team varchar",
            "over integer",
            "batter varchar",
            "bowler varchar",
            "non_striker varchar",
            "runs_batter integer",
            "runs_extras integer",
            "non_boundary boolean",
            "runs_total integer",
            "wicket_player_out varchar",
            "wicket_kind varchar",
            "wicket_fielder_involved varchar",
            "extras_byes integer",
            "extras_legbyes integer",
            "extras_noballs integer",
            "extras_penalty integer",
            "extras_wides integer",
            "target_overs integer",
            "target_runs integer"
        ]
    ,
    "player_universe":
        [
            "match_type varchar",
            "match_type_number integer",
            "match_date date",
            "team varchar",
            "gender varchar",
            "name varchar",
            "unique_id varchar"
        ]
}
