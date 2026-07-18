import hashlib
import re
from datetime import timedelta
from app.domain.schemas import Notice


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", "", text or "")
    text = re.sub(r"[，。；：、,.!！?？（）()\[\]【】]", "", text)
    return text.lower()


def apply_content_hash(notice: Notice) -> Notice:
    base = normalize_text(notice.title + notice.core_content)
    notice.content_hash = hashlib.sha256(base.encode("utf-8")).hexdigest()
    return notice


def deduplicate(notices: list[Notice]) -> tuple[list[Notice], int]:
    for n in notices:
        apply_content_hash(n)
    kept: list[Notice] = []
    duplicate_count = 0
    by_url: dict[str, str] = {}
    by_hash: dict[str, str] = {}
    by_project: dict[str, str] = {}
    for n in sorted(notices, key=lambda x: (x.published_at, x.source_tier.value), reverse=True):
        url_key = n.source_url.rstrip("/")
        project_key = None
        if n.project_no:
            project_key = f"project_no::{n.project_no}::{n.notice_stage}"
        else:
            date_bucket = n.published_at.strftime("%Y-%m")
            project_key = f"soft::{normalize_text(n.title)[:30]}::{n.buyer or ''}::{n.region}::{date_bucket}::{n.notice_stage}"
        if url_key in by_url:
            n.duplicate_of = by_url[url_key]
        elif f"{n.content_hash}::{n.notice_stage}" in by_hash:
            n.duplicate_of = by_hash[f"{n.content_hash}::{n.notice_stage}"]
        elif project_key in by_project:
            n.duplicate_of = by_project[project_key]
        if n.duplicate_of:
            duplicate_count += 1
            continue
        by_url[url_key] = n.id
        by_hash[f"{n.content_hash}::{n.notice_stage}"] = n.id
        by_project[project_key] = n.id
        n.related_project_id = n.project_no or project_key
        kept.append(n)
    return kept, duplicate_count
