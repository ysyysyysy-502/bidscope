import json
from pathlib import Path
from datetime import datetime
from app.domain.enums import SourceTier, AccessStatus, NoticeStage
from app.domain.schemas import Notice, Attachment, Evidence, SourceHealth, QueryIntent

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "notices_government_t0.json"

class GovernmentMockConnector:
    source_id = "government_mock"
    source_name = "政府公开源 Mock（中国政府采购网 / 全国公共资源交易平台口径）"

    async def healthcheck(self) -> SourceHealth:
        return SourceHealth(
            source_id=self.source_id,
            source_name=self.source_name,
            tier=SourceTier.T0_CANONICAL,
            access_status=AccessStatus.PUBLIC_FREE,
            healthy=True,
            mode="fixture_http_static",
            note="使用脱敏样例模拟 T0 官方公告。替换真实源时优先使用公开列表/详情页或官方开放接口。",
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
                source_tier=SourceTier.T0_CANONICAL,
                access_status=AccessStatus.PUBLIC_FREE,
                core_content=item["core_content"],
                attachments=[Attachment(**x) for x in item.get("attachments", [])],
                evidence=[Evidence(source_url=item["source_url"], quote=item["evidence_quote"], captured_at=datetime.now())],
            ))
        return notices
