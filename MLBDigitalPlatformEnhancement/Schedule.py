import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

from MLBDigitalPlatformEnhancement.Match import Match
from MLBDigitalPlatformEnhancement.MatchStatus import MatchStatus


class Schedule:
    def __init__(self):
        self.matches: Dict[str, Match] = {}  # match_id -> Match

    def add_match(self, match: Match) -> bool:
        """Add a match to the schedule"""
        if match.match_id in self.matches:
            return False

        self.matches[match.match_id] = match
        return True

    def get_match(self, match_id: str) -> Optional[Match]:
        """Get a match by ID"""
        return self.matches.get(match_id)

    def update_match(self, match_id: str, **kwargs) -> bool:
        """Update match details"""
        match = self.get_match(match_id)
        if not match:
            return False

        for key, value in kwargs.items():
            if key == "status" and isinstance(value, MatchStatus):
                match.update_match_status(value)
            elif key == "score" and isinstance(value, tuple) and len(value) == 2:
                home_score, away_score = value
                match.update_score(home_score, away_score)
            elif key == "inning" and isinstance(value, tuple) and len(value) == 2:
                inning, is_top = value
                match.update_inning(inning, is_top)
            elif key == "attendance" and isinstance(value, int):
                match.update_attendance(value)
            elif key == "weather" and isinstance(value, str):
                match.update_weather(value)

        return True

    def get_matches_by_date(self, date: datetime.date) -> List[Match]:
        """Get all matches scheduled for a specific date"""
        return [
            match for match in self.matches.values()
            if match.scheduled_time.date() == date
        ]

    def get_matches_by_team(self, team_id: str) -> List[Match]:
        """Get all matches for a specific team"""
        return [
            match for match in self.matches.values()
            if match.home_team_id == team_id or match.away_team_id == team_id
        ]

    def get_matches_by_status(self, status: MatchStatus) -> List[Match]:
        """Get all matches with a specific status"""
        return [
            match for match in self.matches.values()
            if match.status == status
        ]
