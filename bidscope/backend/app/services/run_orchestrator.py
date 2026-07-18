import uuid
from app.connectors.registry import get_connectors
from app.domain.enums import RunStatus
from app.domain.schemas import RunResult, RunRequest
from app.services.intent_parser import parse_intent
from app.services.planner import build_source_plan
from app.services.relevance import filter_and_score
from app.services.dedup import deduplicate
from app.services.subscription_ledger import filter_new_and_mark
from app.services.report import generate_word

RUNS: dict[str, RunResult] = {}

async def run_query(req: RunRequest) -> RunResult:
    run_id = str(uuid.uuid4())[:8]
    intent = parse_intent(req.query)
    plans = await build_source_plan(intent, req.include_sources)
    all_notices = []
    messages = []
    for connector in get_connectors(req.include_sources):
        try:
            items = await connector.search(intent)
            all_notices.extend(items)
            messages.append(f"{connector.source_id} 返回 {len(items)} 条候选。")
        except Exception as exc:
            messages.append(f"{connector.source_id} 失败：{exc}")
    relevant = filter_and_score(all_notices, intent)
    deduped, duplicate_count = deduplicate(relevant)
    new_notices, skipped_incremental = filter_new_and_mark(intent, deduped)
    report_path = generate_word(intent, plans, new_notices, duplicate_count, skipped_incremental)
    restricted_count = sum(1 for n in new_notices if n.restricted_fields)
    result = RunResult(
        run_id=run_id,
        status=RunStatus.COMPLETED,
        intent=intent,
        source_plan=plans,
        notices=new_notices,
        duplicate_count=duplicate_count,
        restricted_count=restricted_count,
        report_filename=report_path.name,
        report_download_url=f"/api/v1/reports/{run_id}/download",
        messages=messages + [f"增量账本跳过历史已推送 {skipped_incremental} 条。"],
    )
    RUNS[run_id] = result
    return result

def get_run(run_id: str) -> RunResult | None:
    return RUNS.get(run_id)
