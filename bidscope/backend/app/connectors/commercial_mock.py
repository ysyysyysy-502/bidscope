import json
from pathlib import Path
from datetime import datetime
from app.domain.enums import SourceTier, AccessStatus, NoticeStage
from app.domain.schemas import Notice, Attachment, Evidence, SourceHealth, QueryIntent

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "notices_commercial_t2.json"

class CommercialMockConnector:
    source_id = "commercial_mock"
    source_name = "商业聚合源 Mock（剑鱼 / 千里马 / 采招网口径）"

    async def healthcheck(self) -> SourceHealth:
        return SourceHealth(
            source_id=self.source_id,
            source_name=self.source_name,
            tier=SourceTier.T2_DISCOVERY,
            access_status=AccessStatus.AUTHORIZED_ACCOUNT,
            healthy=True,
            mode="fixture_authorized_visible_fields",
            note="只返回账号合法可见字段；联系人、画像、关系分析等遮罩字段标记 access_restricted，不尝试恢复。",
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
                access_status=AccessStatus.AUTHORIZED_ACCOUNT,
                core_content=item["core_content"],
                attachments=[Attachment(**x) for x in item.get("attachments", [])],
                evidence=[Evidence(source_url=item["source_url"], quote=item["evidence_quote"], captured_at=datetime.now())],
                restricted_fields=item.get("restricted_fields", []),
            ))
        return notices
