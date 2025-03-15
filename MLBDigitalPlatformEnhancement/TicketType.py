import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

class TicketType(Enum):
    GENERAL = "General Admission"
    RESERVED = "Reserved Seating"
    PREMIUM = "Premium Seating"
    VIP = "VIP"
    BOX = "Box Seats"
    SUITE = "Luxury Suite"
