import json
from pathlib import Path
from datetime import datetime
from app.domain.enums import SourceTier, AccessStatus, NoticeStage
from app.domain.schemas import Notice, Attachment, Evidence, SourceHealth, QueryIntent
from app.core.config import settings

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "notices_api_t2.json"

class ApiBidMockConnector:
    source_id = "api_bid_mock"
    source_name = "招投标 API Mock（可替换为真实 API Key）"

    async def healthcheck(self) -> SourceHealth:
        note = "当前使用 fixture。配置 BID_API_KEY 后可在此类中替换为真实 API 调用。"
        if settings.bid_api_key:
            note = "已检测到 BID_API_KEY，但 Demo 仍默认走 fixture，避免未经核验的外部调用。"
        return SourceHealth(
            source_id=self.source_id,
            source_name=self.source_name,
            tier=SourceTier.T2_DISCOVERY,
            access_status=AccessStatus.ACCOUNT_REQUIRED,
            healthy=True,
            mode="fixture_api_contract",
            note=note,
        )

    async def search(self, intent: QueryIntent) -> list[Notice]:
        raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        notices: list[Notice] = []
        for item in raw:
            notices.append(Notice(
                id=item["id"],
                title=item["title"],
                published_at=datetime.fromisoformat(item["published_at"]),
                region=item["region"],
                buyer=item.get("buyer"),
                agency=item.get("agency"),
                project_no=item.get("project_no"),
                notice_stage=NoticeStage(item.get("notice_stage", "UNKNOWN")),
                procurement_method=item.get("procurement_method"),
                budget=item.get("budget"),
                deadline=datetime.fromisoformat(item["deadline"]) if item.get("deadline") else None,
                source_url=item["source_url"],
                source_name=self.source_name,
                source_tier=SourceTier.T2_DISCOVERY,
                access_status=AccessStatus.ACCOUNT_REQUIRED,
                core_content=item["core_content"],
                attachments=[Attachment(**x) for x in item.get("attachments", [])],
                evidence=[Evidence(source_url=item["source_url"], quote=item["evidence_quote"], captured_at=datetime.now())],
            ))
        return notices
