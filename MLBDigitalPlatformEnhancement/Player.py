import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

from MLBDigitalPlatformEnhancement.Position import Position


class Player:
    def __init__(self, player_id: str, name: str, team_id: str, position: Position, jersey_number: int):
        self.player_id = player_id
        self.name = name
        self.team_id = team_id
        self.position = position
        self.jersey_number = jersey_number

        # Player statistics
        self.games_played = 0
        self.at_bats = 0
        self.hits = 0
        self.home_runs = 0
        self.runs_batted_in = 0
        self.stolen_bases = 0
        self.batting_average = 0.0

        # Pitching statistics (if applicable)
        self.innings_pitched = 0.0
        self.wins = 0
        self.losses = 0
        self.earned_run_average = 0.0
        self.strikeouts = 0
        self.walks = 0
        self.whip = 0.0  # Walks plus hits per inning pitched

    def update_batting_stats(self, games: int, at_bats: int, hits: int, home_runs: int,
                            runs_batted_in: int, stolen_bases: int):
        """Update player's batting statistics"""
        self.games_played += games
        self.at_bats += at_bats
        self.hits += hits
        self.home_runs += home_runs
        self.runs_batted_in += runs_batted_in
        self.stolen_bases += stolen_bases

        # Recalculate batting average
        if self.at_bats > 0:
            self.batting_average = round(self.hits / self.at_bats, 3)

    def update_pitching_stats(self, innings: float, wins: int, losses: int, earned_runs: float,
                             strikeouts: int, walks: int, hits_allowed: int):
        """Update player's pitching statistics"""
        self.innings_pitched += innings
        self.wins += wins
        self.losses += losses
        self.strikeouts += strikeouts
        self.walks += walks

        # Recalculate ERA
        if self.innings_pitched > 0:
            # ERA = (Earned Runs / Innings Pitched) * 9
            self.earned_run_average = round((earned_runs / self.innings_pitched) * 9, 2)

            # WHIP = (Walks + Hits) / Innings Pitched
            self.whip = round((walks + hits_allowed) / self.innings_pitched, 2)

    def get_stats(self) -> Dict[str, Any]:
        """Return a dictionary of player statistics"""
        stats = {
            "player_id": self.player_id,
            "name": self.name,
            "team_id": self.team_id,
            "position": self.position.value,
            "jersey_number": self.jersey_number,
            "batting_stats": {
                "games_played": self.games_played,
                "at_bats": self.at_bats,
                "hits": self.hits,
                "home_runs": self.home_runs,
                "runs_batted_in": self.runs_batted_in,
                "stolen_bases": self.stolen_bases,
                "batting_average": self.batting_average
            }
        }

        # Add pitching stats if player is a pitcher
        if self.position == Position.PITCHER:
            stats["pitching_stats"] = {
                "innings_pitched": self.innings_pitched,
                "wins": self.wins,
                "losses": self.losses,
                "earned_run_average": self.earned_run_average,
                "strikeouts": self.strikeouts,
                "walks": self.walks,
                "whip": self.whip
            }

        return stats

    def __str__(self) -> str:
        return f"{self.name} (#{self.jersey_number}, {self.position.value})"
