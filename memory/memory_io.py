import json
import shutil
import uuid
import os
from datetime import datetime
from logs._logger import logger, MEMORY_LEVEL, WARN_LEVEL, SYSTEM_LEVEL
from config_loader import load_config

config = load_config()
memory_path_cfg = config["memory"]
tags_path_cfg = config["memory"]

max_file_size = 10 * 1024 * 1024

#--# main memory function #--#
class MemoryIO:
    def __init__(self, memory_path, tags_path, use_cache=True):
        self.use_cache = use_cache
        self.memory_path = memory_path_cfg["bank_path"]
        self.tags_path = tags_path_cfg["tags_path"]
        self.memory_bank = []
        self.tags = {}
        self._ensure_files(self.memory_path, "Memory Bank")
        self._ensure_files(self.tags_path, "Tags Bank")
        if self.tags_path and self.use_cache:
            self.memory_bank = self._load_json_file(self.memory_path, fallback=[])
            self.tags = self._load_json_file(self.tags_path, fallback={})

        #-# default tags and types
        self.default_types = ["core_memory", "reflection", "interaction", "system", "meta"]
        self.default_tags = {
            "core_memory": {"description": "Essential knowledge and memories", "reserved": True},
            "boot": {"description": "System startup/reboot events", "reserved": True},
            "self_reflection": {"description": "Self-assessments or insights", "reserved": False},
            "user_input": {"description": "Direct user messages", "reserved": False}
        }

        #-# load and debug default tags
        if isinstance (self.default_tags, dict):
            for tag, meta in self.default_tags.items():
                if isinstance(meta, dict):
                    self.add_tag(
                        tag,
                        description=meta.get("description", ""),
                        reserved=meta.get("reserved", False)
                        )
                else:
                    logger.log(MEMORY_LEVEL, f"[WARNING] An error occurred while importing '{tag}' from default tags. - meta is not a dict: {meta}")


    #-# ensuring existence of memory bank and tags bank
    def _ensure_files(self, path, label):
        #checking file at path
        if not os.path.exists(path):
            logger.log(WARN_LEVEL, f"[MemoryIO - {label} INIT] {path} does not exist.")
            return

        size = os.path.getsize(path)
        if size == 0:
            logger.log(WARN_LEVEL, f"[MemoryIO - {label} INIT] {path} is empty.")
            return

        if size > max_file_size:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            rotated_path = f"{path}.{timestamp}.bak"
            shutil.move(path, rotated_path)
            logger.log(SYSTEM_LEVEL, f"[MemoryIO - {label}] file rotated: {rotated_path}")

            with open(path, 'w') as f:
                if path.endswith(".json"):
                    json.dump({}if "tag" in label.lower() else [], f)

    #-# loading json
    def _load_json_file(self, path, fallback):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.log(WARN_LEVEL, f"[MemoryIO] Could not load {path}: {e}")
            return fallback




    #-# loading memory
    def _load_memory(self):
        try:
            with open(self.memory_path, 'r') as f:
                self.memory_bank = json.load(f)
            if not isinstance(self.memory_bank, list):
                raise ValueError("memory_bank format incorrect")
        except (json.JSONDecodeError, ValueError) as e:
            self.memory_bank = []
            logger.log(MEMORY_LEVEL, f"[MemoryIO] Failed to load memory; initialized empty memory bank.")

    #-# loading tags
    def _load_tags(self):
        try:
            with open(self.tags_path, 'r') as f:
                self.tags = json.load(f)
            if not isinstance(self.tags, dict):
                raise ValueError("tags file missing dictionary")
        except (json.JSONDecodeError, ValueError) as e:
            self.tags = {}
            logger.log(MEMORY_LEVEL, f"[MemoryIO] Failed to load tags; initialized empty tag bank.")

    #-# saving memory
    def _save_memory(self):
        try:
            if os.path.exists(self.memory_path) and os.path.getsize(self.memory_path) >= max_file_size:
                timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
                rotated_path = f"{path}.{timestamp}.bak"
                shutil.move(self.memory_path, rotated_path)
                logger.log(MEMORY_LEVEL, f"[MemoryIO] Memory bank rotated: {rotated_path}")

            with open(self.memory_path, 'w') as f:
                json.dump(self.memory_bank, f, indent=2)
        except Exception as e:
            logger.log(MEMORY_LEVEL, f"[MemoryIO] failed to save memory: {e}")

    #-# saving tags
    def _save_tags(self):
        try:
            if os.path.exists(self.tags_path) and os.path.getsize(self.tags_path) >= max_file_size:
                timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
                rotated_path = f"{path}.{timestamp}.bak"
                shutil.move(self.tags_path, rotated_path)
                logger.log(MEMORY_LEVEL, f"[MemoryIO] Memory bank rotated: {rotated_path}")

            with open(self.tags_path, 'w') as f:
                json.dump(self.tags, f, indent=2)

        except Exception as e:
            logger.log(MEMORY_LEVEL, f"[MemoryIO] failed to save memory: {e}")

    #-# generating random id for memory storage
    def _generate_id(self):
        return str(uuid.uuid4())

    #-# timestamping
    def _timestamp(self):
        return datetime.utcnow().isoformat()

    #-# adding new tags
    def add_tag(self, tag, description = "", reserved = False):
        now = datetime.utcnow().isoformat()
        if tag not in self.tags:
            self.tags[tag] = {
                "description": description,
                "created_at": now,
                "use_count": 0,
                "last_used": now,
                "reserved": reserved
            }
        # else optionally update description
        self._save_tags()

    #-# recording tag usage
    def record_tag_usage(self, tag):
        entry = self.tags.setdefault(tag, {
            "description": "",
            "created_at": datetime.utcnow().isoformat(),
            "use_count": 0,
            "last_used": None
        })
        entry["use_count"] += 1
        entry["last_used"] = datetime.utcnow().isoformat()
        self._save_tags()

    #-# checking whether memory is past expiration date or not
    def _is_expired(self, memory):
        if "expires" in memory and memory["expires"]:
            try:
                expiry = datetime.fromisoformat(memory["expires"])
                return datetime.utcnow() > expiry
            except ValueError:
                return False
        return False

    #-# adding memory to overall iris_memory
    def add_memory(self, content, memory_type="type", tags=None, source="source", expires=None):
        memory = {
            "id": self._generate_id(),
            "type": memory_type,
            "tags": tags or [],
            "content": content,
            "source": source,
            "timestamp": self._timestamp(),
            "expires": expires
        }
        for t in tags or []:
            self.record_tag_usage(t)
        self.memory_bank.append(memory)
        self._save_memory()
        return memory

    def get_memories(self, tags=None, memory_type=None, limit=10, include_expired=False):
        memories = self.memory_bank
        if tags:
            memories = [m for m in memories if any(tag in m.get("tags", []) for tag in tags)]
        if memory_type:
            memories = [m for m in memories if m.get("type") == memory_type]
        return memories[:limit]

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




# Example usage
if __name__ == "__main__":
    memory_io = MemoryIO()

    # Add a memory
    memory_io.add_memory(
        content="Iris was rebooted with limited memory.",
        memory_type="core_memory",
        tags=["boot", "system"],
        source="boot_sequence"
    )

    # Retrieve memories
    memories = memory_io.get_memories(limit=6)
    logger.log(MEMORY_LEVEL, f"[MemoryIO] Recent boot memories: {memories}")
