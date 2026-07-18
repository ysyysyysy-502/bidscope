from datetime import datetime
from app.domain.enums import SourceTier, AccessStatus, NoticeStage
from app.domain.schemas import Notice
from app.services.dedup import deduplicate


def make_notice(id_, url, stage=NoticeStage.PROCUREMENT):
    return Notice(
        id=id_, title='上海服务器采购公告', published_at=datetime(2026, 7, 1), region='上海',
        buyer='测试采购人', project_no='P-001', notice_stage=stage, source_url=url,
        source_name='test', source_tier=SourceTier.T0_CANONICAL, access_status=AccessStatus.PUBLIC_FREE,
        core_content='采购服务器和算力设备。'
    )


def test_same_project_same_stage_dedup():
    a = make_notice('a', 'https://example.com/a')
    b = make_notice('b', 'https://example.com/b')
    kept, duplicate_count = deduplicate([a, b])
    assert len(kept) == 1
    assert duplicate_count == 1


def test_same_project_different_stage_kept():
    a = make_notice('a', 'https://example.com/a', NoticeStage.PROCUREMENT)
    b = make_notice('b', 'https://example.com/b', NoticeStage.CHANGE)
    kept, duplicate_count = deduplicate([a, b])
    assert len(kept) == 2
    assert duplicate_count == 0
