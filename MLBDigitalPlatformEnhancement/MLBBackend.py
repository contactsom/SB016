import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

from MLBDigitalPlatformEnhancement.Booking import Booking
from MLBDigitalPlatformEnhancement.Match import Match
from MLBDigitalPlatformEnhancement.Player import Player
from MLBDigitalPlatformEnhancement.Position import Position
from MLBDigitalPlatformEnhancement.Schedule import Schedule
from MLBDigitalPlatformEnhancement.Team import Team
from MLBDigitalPlatformEnhancement.Ticket import Ticket
from MLBDigitalPlatformEnhancement.TicketStatus import TicketStatus
from MLBDigitalPlatformEnhancement.TicketType import TicketType


class MLBBackend:
    def __init__(self):
        self.teams: Dict[str, Team] = {}  # team_id -> Team
        self.players: Dict[str, Player] = {}  # player_id -> Player
        self.schedule = Schedule()
        self.tickets: Dict[str, Ticket] = {}  # ticket_id -> Ticket
        self.bookings: Dict[str, Booking] = {}  # booking_id -> Booking

        # For generating unique IDs
        self.team_counter = 1
        self.player_counter = 1
        self.match_counter = 1
        self.ticket_counter = 1
        self.booking_counter = 1

        # Thread locks
        self.team_lock = threading.Lock()
        self.player_lock = threading.Lock()
        self.match_lock = threading.Lock()
        self.ticket_lock = threading.Lock()
        self.booking_lock = threading.Lock()

    def generate_team_id(self) -> str:
        """Generate a unique team ID"""
        with self.team_lock:
            team_id = f"T{self.team_counter:04d}"
            self.team_counter += 1
            return team_id

    def generate_player_id(self) -> str:
        """Generate a unique player ID"""
        with self.player_lock:
            player_id = f"P{self.player_counter:04d}"
            self.player_counter += 1
            return player_id

    def generate_match_id(self) -> str:
        """Generate a unique match ID"""
        with self.match_lock:
            match_id = f"M{self.match_counter:04d}"
            self.match_counter += 1
            return match_id

    def generate_ticket_id(self) -> str:
        """Generate a unique ticket ID"""
        with self.ticket_lock:
            ticket_id = f"TK{self.ticket_counter:06d}"
            self.ticket_counter += 1
            return ticket_id

    def generate_booking_id(self) -> str:
        """Generate a unique booking ID"""
        with self.booking_lock:
            booking_id = f"B{self.booking_counter:06d}"
            self.booking_counter += 1
            return booking_id

    # Team Management
    def add_team(self, name: str, city: str, stadium: str, division: str) -> Team:
        """Add a new team"""
        team_id = self.generate_team_id()
        team = Team(team_id, name, city, stadium, division)
        self.teams[team_id] = team
        return team

    def get_team(self, team_id: str) -> Optional[Team]:
        """Get a team by ID"""
        return self.teams.get(team_id)

    def get_teams_by_division(self, division: str) -> List[Team]:
        """Get all teams in a specific division"""
        return [team for team in self.teams.values() if team.division == division]

    # Player Management
    def add_player(self, name: str, team_id: str, position: Position, jersey_number: int) -> Optional[Player]:
        """Add a new player"""
        team = self.get_team(team_id)
        if not team:
            return None

        player_id = self.generate_player_id()
        player = Player(player_id, name, team_id, position, jersey_number)

        self.players[player_id] = player
        team.add_player(player)

        return player

    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID"""
        return self.players.get(player_id)

    def get_players_by_team(self, team_id: str) -> List[Player]:
        """Get all players on a specific team"""
        return [player for player in self.players.values() if player.team_id == team_id]

    # Match Schedule Management
    def add_match(self, home_team_id: str, away_team_id: str, venue: str,
                 scheduled_time: datetime.datetime) -> Optional[Match]:
        """Add a new match"""
        home_team = self.get_team(home_team_id)
        away_team = self.get_team(away_team_id)

        if not home_team or not away_team:
            return None

        match_id = self.generate_match_id()
        match = Match(match_id, home_team_id, away_team_id, venue, scheduled_time)

        self.schedule.add_match(match)
        return match

    def get_match(self, match_id: str) -> Optional[Match]:
        """Get a match by ID"""
        return self.schedule.get_match(match_id)

    # Ticket Management
    def add_tickets_for_match(self, match_id: str, section: str, row: str,
                             seats: List[str], ticket_type: TicketType, price: float) -> List[Ticket]:
        """Add multiple tickets for a match"""
        match = self.get_match(match_id)
        if not match:
            return []

        tickets = []
        for seat in seats:
            ticket_id = self.generate_ticket_id()
            ticket = Ticket(ticket_id, match_id, section, row, seat, ticket_type, price)
            self.tickets[ticket_id] = ticket
            tickets.append(ticket)

        return tickets

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get a ticket by ID"""
        return self.tickets.get(ticket_id)

    def get_available_tickets(self, match_id: str, ticket_type: Optional[TicketType] = None) -> List[Ticket]:
        """Get all available tickets for a match"""
        tickets = [
            ticket for ticket in self.tickets.values()
            if ticket.match_id == match_id and ticket.status == TicketStatus.AVAILABLE
        ]

        if ticket_type:
            tickets = [ticket for ticket in tickets if ticket.ticket_type == ticket_type]

        return tickets

    # Booking Management
    def create_booking(self, customer_name: str, customer_email: str, customer_phone: str,
                      match_id: str, ticket_ids: List[str]) -> Optional[Booking]:
        """Create a new booking"""
        match = self.get_match(match_id)
        if not match:
            return None

        booking_id = self.generate_booking_id()
        booking_time = datetime.datetime.now()
        booking = Booking(booking_id, customer_name, customer_email, customer_phone, match_id, booking_time)

        # Add tickets to booking
        for ticket_id in ticket_ids:
            ticket = self.get_ticket(ticket_id)
            if ticket and ticket.status == TicketStatus.AVAILABLE:
                booking.add_ticket(ticket)

        if not booking.ticket_ids:  # No tickets were added
            return None

        self.bookings[booking_id] = booking
        return booking

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """Get a booking by ID"""
        return self.bookings.get(booking_id)

    def confirm_booking(self, booking_id: str, payment_reference: str) -> bool:
        """Confirm a booking"""
        booking = self.get_booking(booking_id)
        if not booking:
            return False

        # Mark all tickets as sold
        for ticket_id in booking.ticket_ids:
            ticket = self.get_ticket(ticket_id)
            if ticket:
                ticket.confirm_sale()

        return booking.confirm_booking(payment_reference)

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        booking = self.get_booking(booking_id)
        if not booking:
            return False

        # Release all tickets
        for ticket_id in booking.ticket_ids:
            ticket = self.get_ticket(ticket_id)
            if ticket:
                ticket.cancel_reservation()

        return booking.cancel_booking()

    # Report Generation
    def generate_player_stats_report(self, output_file: str, team_id: Optional[str] = None) -> bool:
        """Generate a player statistics report"""
        players_to_include = []

        if team_id:
            players_to_include = self.get_players_by_team(team_id)
        else:
            players_to_include = list(self.players.values())

        if not players_to_include:
            return False

        # Create a threaded report generator
        def thread_task():
            report = {
                "report_type": "Player Statistics",
                "generated_at": datetime.datetime.now().isoformat(),
                "player_count": len(players_to_include),
                "team_id": team_id if team_id else "All Teams",
                "players": [player.get_stats() for player in players_to_include]
            }

            with open(output_file, 'w') as file:
                json.dump(report, file, indent=2)

        # Run the report generation in a separate thread
        report_thread = threading.Thread(target=thread_task)
        report_thread.start()

        # Wait for completion
        report_thread.join()
        return True

    def generate_team_schedule_report(self, team_id: str, output_file: str) -> bool:
        """Generate a team's schedule report"""
        team = self.get_team(team_id)
        if not team:
            return False

        matches = self.schedule.get_matches_by_team(team_id)

        # Create a threaded report generator
        def thread_task():
            report = {
                "report_type": "Team Schedule",
                "generated_at": datetime.datetime.now().isoformat(),
                "team": team.get_team_details(),
                "match_count": len(matches),
                "matches": [match.get_match_details() for match in matches]
            }

            with open(output_file, 'w') as file:
                json.dump(report, file, indent=2)

        # Run the report generation in a separate thread
        report_thread = threading.Thread(target=thread_task)
        report_thread.start()

        # Wait for completion
        report_thread.join()
        return True

    def generate_ticket_sales_report(self, match_id: Optional[str] = None, output_file: str = None) -> bool:
        """Generate a ticket sales report"""
        if match_id:
            match = self.get_match(match_id)
            if not match:
                return False

        # Create a threaded report generator
        def thread_task():
            # Filter tickets based on match_id if provided
            match_tickets = [
                ticket for ticket in self.tickets.values()
                if not match_id or ticket.match_id == match_id
            ]

            # Count tickets by status
            available_count = sum(1 for ticket in match_tickets if ticket.status == TicketStatus.AVAILABLE)
            reserved_count = sum(1 for ticket in match_tickets if ticket.status == TicketStatus.RESERVED)
            sold_count = sum(1 for ticket in match_tickets if ticket.status == TicketStatus.SOLD)

            # Calculate revenue
            revenue = sum(ticket.price for ticket in match_tickets if ticket.status == TicketStatus.SOLD)

            report = {
                "report_type": "Ticket Sales",
                "generated_at": datetime.datetime.now().isoformat(),
                "match_id": match_id if match_id else "All Matches",
                "total_tickets": len(match_tickets),
                "available_tickets": available_count,
                "reserved_tickets": reserved_count,
                "sold_tickets": sold_count,
                "revenue": revenue
            }

            with open(output_file, 'w') as file:
                json.dump(report, file, indent=2)

        # Run the report generation in a separate thread
        report_thread = threading.Thread(target=thread_task)
        report_thread.start()

        # Wait for completion
        report_thread.join()
        return True

    def generate_all_reports(self, output_dir: str) -> bool:
        """Generate all reports in parallel"""
        # Create threads for each report
        threads = []

        # Player stats report - all teams
        player_stats_thread = threading.Thread(
            target=self.generate_player_stats_report,
            args=(f"{output_dir}/player_stats_all.json", None)
        )
        threads.append(player_stats_thread)

        # Team schedule reports - one per team
        for team_id, team in self.teams.items():
            team_schedule_thread = threading.Thread(
                target=self.generate_team_schedule_report,
                args=(team_id, f"{output_dir}/schedule_{team_id}.json")
            )
            threads.append(team_schedule_thread)

        # Ticket sales report - all matches
        ticket_sales_thread = threading.Thread(
            target=self.generate_ticket_sales_report,
            args=(None, f"{output_dir}/ticket_sales_all.json")
        )
        threads.append(ticket_sales_thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        return True


# Demo function to test the MLB Backend system
def run_mlb_system_demo():
    # Initialize the MLB Backend
    mlb = MLBBackend()
