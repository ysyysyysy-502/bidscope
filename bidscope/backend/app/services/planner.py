from app.connectors.registry import get_connectors
from app.domain.schemas import QueryIntent, SourcePlan

async def build_source_plan(intent: QueryIntent, include_sources: list[str] | None = None) -> list[SourcePlan]:
    plans = []
    for connector in get_connectors(include_sources):
        health = await connector.healthcheck()
        plans.append(SourcePlan(
            source_id=health.source_id,
            source_name=health.source_name,
            tier=health.tier,
            access_status=health.access_status,
            mode=health.mode,
            note=health.note,
        ))
    return plans
