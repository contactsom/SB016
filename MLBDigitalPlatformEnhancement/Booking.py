import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

from MLBDigitalPlatformEnhancement.BookingStatus import BookingStatus
from MLBDigitalPlatformEnhancement.Ticket import Ticket


class Booking:
    def __init__(self, booking_id: str, customer_name: str, customer_email: str,
                customer_phone: str, match_id: str, booking_time: datetime.datetime):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone
        self.match_id = match_id
        self.booking_time = booking_time
        self.status = BookingStatus.PENDING
        self.ticket_ids: List[str] = []
        self.total_amount = 0.0
        self.payment_reference = ""

    def add_ticket(self, ticket: Ticket) -> bool:
        """Add a ticket to this booking"""
        if not ticket.reserve_ticket(self.booking_id):
            return False

        self.ticket_ids.append(ticket.ticket_id)
        self.total_amount += ticket.price
        return True

    def remove_ticket(self, ticket: Ticket) -> bool:
        """Remove a ticket from this booking"""
        if ticket.ticket_id not in self.ticket_ids:
            return False

        if not ticket.cancel_reservation():
            return False

        self.ticket_ids.remove(ticket.ticket_id)
        self.total_amount -= ticket.price
        return True

    def confirm_booking(self, payment_reference: str) -> bool:
        """Confirm this booking"""
        if self.status != BookingStatus.PENDING:
            return False

        self.status = BookingStatus.CONFIRMED
        self.payment_reference = payment_reference
        return True

    def cancel_booking(self) -> bool:
        """Cancel this booking"""
        if self.status == BookingStatus.CANCELLED:
            return False

        self.status = BookingStatus.CANCELLED
        return True

    def get_booking_details(self) -> Dict[str, Any]:
        """Return a dictionary of booking details"""
        return {
            "booking_id": self.booking_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_phone": self.customer_phone,
            "match_id": self.match_id,
            "booking_time": self.booking_time.isoformat(),
            "status": self.status.value,
            "ticket_count": len(self.ticket_ids),
            "total_amount": self.total_amount,
            "payment_reference": self.payment_reference
        }

    def __str__(self) -> str:
        return f"Booking {self.booking_id}: {self.customer_name}, {len(self.ticket_ids)} tickets, ${self.total_amount:.2f}"
