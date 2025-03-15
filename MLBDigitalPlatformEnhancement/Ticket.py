import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

from MLBDigitalPlatformEnhancement.TicketStatus import TicketStatus
from MLBDigitalPlatformEnhancement.TicketType import TicketType


class Ticket:
    def __init__(self, ticket_id: str, match_id: str, section: str, row: str, seat: str,
                ticket_type: TicketType, price: float):
        self.ticket_id = ticket_id
        self.match_id = match_id
        self.section = section
        self.row = row
        self.seat = seat
        self.ticket_type = ticket_type
        self.price = price
        self.status = TicketStatus.AVAILABLE
        self.booking_id = None

    def reserve_ticket(self, booking_id: str) -> bool:
        """Reserve this ticket"""
        if self.status != TicketStatus.AVAILABLE:
            return False

        self.status = TicketStatus.RESERVED
        self.booking_id = booking_id
        return True

    def confirm_sale(self) -> bool:
        """Mark this ticket as sold"""
        if self.status != TicketStatus.RESERVED:
            return False

        self.status = TicketStatus.SOLD
        return True

    def cancel_reservation(self) -> bool:
        """Cancel the reservation for this ticket"""
        if self.status not in [TicketStatus.RESERVED, TicketStatus.SOLD]:
            return False

        self.status = TicketStatus.AVAILABLE
        self.booking_id = None
        return True

    def get_ticket_details(self) -> Dict[str, Any]:
        """Return a dictionary of ticket details"""
        return {
            "ticket_id": self.ticket_id,
            "match_id": self.match_id,
            "section": self.section,
            "row": self.row,
            "seat": self.seat,
            "ticket_type": self.ticket_type.value,
            "price": self.price,
            "status": self.status.value,
            "booking_id": self.booking_id
        }

    def __str__(self) -> str:
        return f"Ticket {self.ticket_id}: {self.section} {self.row}-{self.seat} ({self.ticket_type.value})"
