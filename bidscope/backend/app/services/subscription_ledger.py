import json
import hashlib
from pathlib import Path
from app.core.config import settings
from app.domain.schemas import Notice, QueryIntent

LEDGER_PATH = settings.storage_dir / "delivery_ledger.json"

def _load() -> dict:
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {}

def _save(data: dict):
    LEDGER_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def subscription_key(intent: QueryIntent) -> str:
    raw = f"{intent.raw_query}|{intent.regions}|{intent.topic}|{intent.schedule_cron or 'once'}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def filter_new_and_mark(intent: QueryIntent, notices: list[Notice]) -> tuple[list[Notice], int]:
    data = _load()
    sub = subscription_key(intent)
    sent = set(data.get(sub, []))
    new_notices = []
    skipped = 0
    for n in notices:
        key = f"{n.id}:{n.content_hash}"
        if key in sent:
            skipped += 1
            continue
        new_notices.append(n)
        sent.add(key)
    data[sub] = sorted(sent)
    _save(data)
    return new_notices, skipped
