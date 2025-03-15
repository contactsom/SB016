import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

from MLBDigitalPlatformEnhancement.MatchStatus import MatchStatus


class Match:
    def __init__(self, match_id: str, home_team_id: str, away_team_id: str,
                venue: str, scheduled_time: datetime.datetime):
        self.match_id = match_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.venue = venue
        self.scheduled_time = scheduled_time
        self.status = MatchStatus.SCHEDULED

        # Match statistics
        self.home_team_score = 0
        self.away_team_score = 0
        self.current_inning = 0
        self.is_inning_top = True  # True for top of inning, False for bottom

        # Weather and conditions
        self.weather = ""
        self.attendance = 0

    def update_match_status(self, status: MatchStatus):
        """Update the match status"""
        self.status = status

    def update_score(self, home_score: int, away_score: int):
        """Update the match score"""
        self.home_team_score = home_score
        self.away_team_score = away_score

    def update_inning(self, inning: int, is_top: bool):
        """Update the current inning information"""
        self.current_inning = inning
        self.is_inning_top = is_top

    def update_attendance(self, attendance: int):
        """Update the match attendance"""
        self.attendance = attendance

    def update_weather(self, weather: str):
        """Update the weather conditions"""
        self.weather = weather

    def get_match_details(self) -> Dict[str, Any]:
        """Return a dictionary of match details"""
        inning_half = "Top" if self.is_inning_top else "Bottom"

        return {
            "match_id": self.match_id,
            "home_team_id": self.home_team_id,
            "away_team_id": self.away_team_id,
            "venue": self.venue,
            "scheduled_time": self.scheduled_time.isoformat(),
            "status": self.status.value,
            "score": f"{self.home_team_score} - {self.away_team_score}",
            "current_inning": f"{inning_half} {self.current_inning}" if self.status == MatchStatus.LIVE else "",
            "weather": self.weather,
            "attendance": self.attendance
        }

    def __str__(self) -> str:
        return f"Match {self.match_id}: {self.home_team_id} vs {self.away_team_id} at {self.venue}"
