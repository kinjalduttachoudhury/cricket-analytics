from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class Runs(BaseModel):
    batter: int
    extras: int
    non_boundary: Optional[bool] = None
    total: int


class Extras(BaseModel):
    byes: Optional[int] = None
    wides: Optional[int] = None
    legbyes: Optional[int] = None
    noballs: Optional[int] = None
    penalty: Optional[int] = None


class Fielder(BaseModel):
    name: Optional[str] = None


class Wicket(BaseModel):
    player_out: str
    fielders: Optional[List[Fielder]] = None
    kind: str


class Delivery(BaseModel):
    batter: str
    bowler: str
    non_striker: str
    runs: Runs
    extras: Optional[Extras] = None
    wickets: Optional[List[Wicket]] = None


class Over(BaseModel):
    over: int
    deliveries: List[Delivery]


class Target(BaseModel):
    overs: int
    runs: int


class Innings(BaseModel):
    team: str
    overs: List[Over]
    target: Optional[Target] = None


class Info(BaseModel):
    match_type: str
    match_type_number: Optional[int] = None
    dates: List[date]
    teams: List[str]


class MatchBallByBall(BaseModel):
    innings: List[Innings]
    info: Info
