# MLB Digital Platform Backend System
import threading
import datetime
import uuid
import time
from enum import Enum
import json
from typing import List, Dict, Any, Optional


class Position(Enum):
    PITCHER = "Pitcher"
    CATCHER = "Catcher"
    FIRST_BASE = "First Base"
    SECOND_BASE = "Second Base"
    THIRD_BASE = "Third Base"
    SHORTSTOP = "Shortstop"
    LEFT_FIELD = "Left Field"
    CENTER_FIELD = "Center Field"
    RIGHT_FIELD = "Right Field"
    DESIGNATED_HITTER = "Designated Hitter"

