import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional

class TicketStatus(Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    SOLD = "Sold"
    CANCELLED = "Cancelled"