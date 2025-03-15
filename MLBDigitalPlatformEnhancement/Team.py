import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

from MLBDigitalPlatformEnhancement.Player import Player
from MLBDigitalPlatformEnhancement.Position import Position


class Team:
    def __init__(self, team_id: str, name: str, city: str, stadium: str, division: str):
        self.team_id = team_id
        self.name = name
        self.city = city
        self.stadium = stadium
        self.division = division
        self.roster: Dict[str, Player] = {}  # player_id -> Player
        self.wins = 0
        self.losses = 0

    def add_player(self, player: Player) -> bool:
        """Add a player to the team roster"""
        if player.player_id in self.roster:
            return False

        self.roster[player.player_id] = player
        return True

    def remove_player(self, player_id: str) -> bool:
        """Remove a player from the team roster"""
        if player_id not in self.roster:
            return False

        del self.roster[player_id]
        return True

    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID"""
        return self.roster.get(player_id)

    def get_players_by_position(self, position: Position) -> List[Player]:
        """Get all players at a specific position"""
        return [
            player for player in self.roster.values()
            if player.position == position
        ]

    def update_record(self, win: bool) -> None:
        """Update team's win-loss record"""
        if win:
            self.wins += 1
        else:
            self.losses += 1

    def get_team_details(self) -> Dict[str, Any]:
        """Return a dictionary of team details"""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "city": self.city,
            "stadium": self.stadium,
            "division": self.division,
            "record": f"{self.wins}-{self.losses}",
            "winning_percentage": round(self.wins / (self.wins + self.losses), 3) if (self.wins + self.losses) > 0 else 0,
            "roster_size": len(self.roster)
        }

    def __str__(self) -> str:
        return f"{self.city} {self.name} ({self.wins}-{self.losses})"
