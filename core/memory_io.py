### ---- ### Memory Management Module ### ---- ###
##
#
# handles the entire memory framework
# (retrieval, storage, and management)
#



import json
from core.core import load_config
from core._logger import logger, MEMORY_LEVEL, SYSTEM_LEVEL
import os
from datetime import datetime
from typing import List, Dict, Any







def save_memory(user_id, entry):
    path = f"data/memory/{user_id}.json"
    with open(path, "a") as f:
        json.dump(entry, f)
        f.write("\n")

def load_recent_context(user_id, limit=5):
    path = f"data/memory/{user_id}.json"
    if not os.path.exists(path): return []
    with open(path) as f:
        return list(map(json.loads, f.readlines()))[-limit:]

