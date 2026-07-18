from app.domain.schemas import Notice, QueryIntent

STAGE_WEIGHT = 0.15
REGION_WEIGHT = 0.25
TERM_WEIGHT = 0.45
TIER_WEIGHT = 0.15

def score_notice(notice: Notice, intent: QueryIntent) -> Notice:
    haystack = f"{notice.title} {notice.core_content} {notice.buyer or ''} {notice.project_no or ''}"
    matched = []
    for term in [intent.topic] + intent.synonyms:
        if term and term in haystack:
            matched.append(term)
    region_ok = "全国" in intent.regions or notice.region in intent.regions
    stage_ok = notice.notice_stage in intent.stages if intent.stages else True
    term_score = min(1.0, len(set(matched)) / 3) if matched else 0
    tier_score = 1.0 if notice.source_tier.value.startswith("T0") else 0.65
    score = 0
    score += REGION_WEIGHT if region_ok else 0
    score += STAGE_WEIGHT if stage_ok else 0
    score += TERM_WEIGHT * term_score
    score += TIER_WEIGHT * tier_score
    notice.matched_terms = sorted(set(matched))
    notice.relevance_score = round(score, 3)
    if matched:
        quote = notice.evidence[0].quote if notice.evidence else notice.core_content[:80]
        notice.relevance_reason = f"命中 {', '.join(sorted(set(matched)))}；证据片段：{quote[:120]}"
    else:
        notice.relevance_reason = "未命中核心主题词，仅作为待核验线索保留。"
    return notice

def filter_and_score(notices: list[Notice], intent: QueryIntent, threshold: float = 0.45) -> list[Notice]:
    scored = [score_notice(n, intent) for n in notices]
    # 保守策略：T0 低分也保留为待核验；T2/T3 低分过滤
    return [n for n in scored if n.relevance_score >= threshold or n.source_tier.value.startswith("T0")]
