from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class Event(BaseModel):
    name: str
    match_number: Optional[int] = None


class By(BaseModel):
    runs: Optional[int] = None
    wickets: Optional[int] = None


class Outcome(BaseModel):
    winner: Optional[str] = None
    by: Optional[By] = None
    result: Optional[str] = None
    method: Optional[str] = None


class Toss(BaseModel):
    decision: str
    winner: str


class MatchResult(BaseModel):
    dates: List[date]
    event: Optional[Event] = None
    gender: str
    match_type: str
    match_type_number: Optional[int] = None
    outcome: Outcome
    season: str
    teams: List[str]
    toss: Toss
    venue: Optional[str] = None
