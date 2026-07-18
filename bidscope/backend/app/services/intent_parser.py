import re
from datetime import datetime, timedelta
from app.domain.enums import NoticeStage
from app.domain.schemas import QueryIntent

REGIONS = [
    "北京","上海","天津","重庆","河北","山西","内蒙古","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","广西","海南","四川","贵州","云南","西藏","陕西","甘肃","青海","宁夏","新疆","全国"
]
TOPIC_SYNONYMS = {
    "服务器": ["服务器", "计算设备", "机架式服务器", "AI服务器", "GPU服务器"],
    "算力": ["算力", "智算", "算力集群", "高性能计算", "计算中心"],
    "AI基础设施": ["AI基础设施", "人工智能基础设施", "智能算力", "大模型平台"],
    "存储": ["存储", "磁盘阵列", "分布式存储", "备份"],
    "网络": ["网络设备", "交换机", "路由器", "数据中心网络"],
    "充电站": ["充电站", "充电桩", "储能电站", "新能源"],
}

def _parse_date_range(query: str):
    now = datetime.now().replace(microsecond=0)
    m = re.search(r"最近\s*(\d+)\s*个?月", query)
    if m:
        return now - timedelta(days=30*int(m.group(1))), now
    m = re.search(r"近\s*(\d+)\s*天", query)
    if m:
        return now - timedelta(days=int(m.group(1))), now
    if "最近一个月" in query or "近一个月" in query:
        return now - timedelta(days=30), now
    if "本周" in query:
        return now - timedelta(days=7), now
    if "今天" in query:
        return now.replace(hour=0, minute=0, second=0), now
    return now - timedelta(days=30), now

def _parse_schedule(query: str):
    if "每天" in query:
        m = re.search(r"每天\s*(\d{1,2})(?:[:：点时])?(\d{0,2})", query)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2) or 0)
            return f"{minute} {hour} * * *", f"每天 {hour:02d}:{minute:02d}"
        return "0 9 * * *", "每天 09:00"
    if "每周" in query:
        return "0 9 * * 1", "每周一 09:00"
    return None, None

def parse_intent(query: str) -> QueryIntent:
    regions = [r for r in REGIONS if r in query]
    if not regions:
        regions = ["全国"]
    topic_hits: list[str] = []
    synonyms: list[str] = []
    for topic, words in TOPIC_SYNONYMS.items():
        if topic in query or any(w in query for w in words):
            topic_hits.append(topic)
            synonyms.extend(words)
    if not topic_hits:
        topic_hits = ["服务器与算力"]
        synonyms = TOPIC_SYNONYMS["服务器"] + TOPIC_SYNONYMS["算力"]
    start_at, end_at = _parse_date_range(query)
    cron, schedule_text = _parse_schedule(query)
    stages = []
    if any(x in query for x in ["招标", "采购", "询价", "竞谈", "竞磋"]):
        stages.append(NoticeStage.PROCUREMENT)
    if any(x in query for x in ["中标", "成交", "结果"]):
        stages.append(NoticeStage.AWARD)
    if any(x in query for x in ["更正", "澄清", "延期"]):
        stages.append(NoticeStage.CHANGE)
    if not stages:
        stages = [NoticeStage.PROCUREMENT, NoticeStage.AWARD, NoticeStage.CHANGE]
    questions = []
    clarification = False
    if regions == ["全国"] and "全国" not in query:
        questions.append("未识别到明确地区，已默认全国；正式订阅前建议确认目标区域。")
    confidence = 0.96 if not questions else 0.82
    return QueryIntent(
        raw_query=query,
        topic="、".join(topic_hits),
        synonyms=sorted(set(synonyms)),
        regions=regions,
        start_at=start_at,
        end_at=end_at,
        stages=stages,
        schedule_cron=cron,
        schedule_text=schedule_text,
        confidence=confidence,
        clarification_needed=clarification,
        clarification_questions=questions,
    )
