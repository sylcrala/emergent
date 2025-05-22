### ---- ### Memory Management Module ### ---- ###
##
#
# handles the entire memory framework
# (retrieval, storage, and management)
#


import uuid
import json
from ext.config_loader import main_config
from ext._logger import logger, MEMORY_LEVEL, SYSTEM_LEVEL
import os
from datetime import datetime
from typing import List, Dict, Any
from utils.tokenizer_tool import TokenizerBank


config = main_config["memory"]

class memIO:
    def __init__(self, user_id, memory_path, model_id, reflection_interval=10):
        self.tokenizer = TokenizerBank().get(model_id)

        self.reflection_interval = reflection_interval
        self.interaction_count = 0

        self.memory_bank = []


    def add_memory(self, user_id, raw_input, response,  model_id, voice="neutral", context="default", expires=None):
        path = f"data/memory_bank/{user_id}.json"



        try:
         tokenizer = TokenizerBank().get(model_id)
        except Exception as e:
            print("failed loading tokenizer for memory save")
            logger.log(SYSTEM_LEVEL, MEMORY_LEVEL, f"[Tokenizer] failed to load for {model_id}: {e}")
            return

        try:
            tokens = tokenizer.encode(raw_input, add_special_tokens=False)
            sanitized_input = tokenizer.decode(tokenizer.encode(tokens))
        except Exception as e:
            logger.log(SYSTEM_LEVEL, MEMORY_LEVEL, f"[MemoryIO] tokenizer error while decoding/encoding for {model_id}: {e}")
            sanitized_input = raw_input
            tokens = []



        entry = {
            "id": self.generate_id(),
            "user_id": user_id,
            "raw_input": raw_input,
            "generated_output": response,
            "sanitized": sanitized_input,
            "tokens": tokens,
            "token_count": len(tokens),
            "tokenizer_id": model_id,
            "context": context,
            "voice": voice,
            "timestamp": self.timestamp(),
            "expires": expires
        }

        with open(path, "a") as f:
            json.dump(entry, f)
            f.write("\n")

   #-# loading memory
    def load_memory(self, user_id):
        path = f"data/memory_bank/{user_id}.json"
        try:
            with open(path) as f:
                return list(map(json.loads, f.readlines()))
            if not isinstance(self.memory_bank, list):
                raise ValueError("memory_bank format incorrect")
        except (json.JSONDecodeError, ValueError) as e:
            self.memory_bank = []
            logger.log(MEMORY_LEVEL, f"[MemoryIO] Failed to load memory; initialized empty memory bank.")


    def load_recent_context(self, user_id, limit=5):
        path = f"data/memory_bank/{user_id}.json"
        if not os.path.exists(path): return []
        with open(path) as f:
           return list(map(json.loads, f.readlines()))[-limit:]



    #-# generating random id for memory storage
    def generate_id(self):
        return str(uuid.uuid4())


    #-# timestamping
    def timestamp(self):
        return datetime.utcnow().isoformat()
    

    #expiry check
    def _is_expired(self, memory):
        if "expires" in memory and memory["expires"]:
            try:
                expiry = datetime.fromisoformat(memory["expires"])
                return datetime.utcnow() > expiry
            except ValueError:
                return False
        return False
    

    #-# updating memory bank
    def update_memory(self, memory_id, **kwargs):
        for memory in self.memory_bank:
            if memory["id"] == memory_id:
                memory.update(kwargs)
                self._save_memory()
                return memory
        return None
    

    #-# trimming old memories
    def delete_memory(self, memory_id):
        original_len = len(self.memory_bank)
        self.memory_bank = [m for m in self.memory_bank if m["id"] != memory_id]
        if len(self.memory_bank) < original_len:
            self._save_memory()
            return True
        return False
    
    def save_memory(self, user_id):
        path = f"data/memory_bank/{user_id}.json"
        with open(path, "w") as f:
            json.dump(self.memory_bank, f, indent=2)


