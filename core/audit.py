import hashlib, json
from datetime import datetime, timezone

class AuditTrail:
    """Tamper-evident hash-chained audit log for the prototype."""
    def __init__(self):
        self.entries = []
        self.previous_hash = "GENESIS"

    def add(self, event, actor, payload=None):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "actor": actor,
            "payload": payload or {},
            "previous_hash": self.previous_hash,
        }
        raw = json.dumps(entry, sort_keys=True, separators=(",", ":")).encode()
        entry["hash"] = hashlib.sha256(raw).hexdigest()
        self.previous_hash = entry["hash"]
        self.entries.append(entry)
        return entry

    def verify(self):
        previous = "GENESIS"
        for e in self.entries:
            check = dict(e)
            saved = check.pop("hash")
            if check["previous_hash"] != previous:
                return False
            raw = json.dumps(check, sort_keys=True, separators=(",", ":")).encode()
            if hashlib.sha256(raw).hexdigest() != saved:
                return False
            previous = saved
        return True
