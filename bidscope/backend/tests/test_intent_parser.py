from app.services.intent_parser import parse_intent


def test_parse_shanghai_daily_query():
    intent = parse_intent('最近3个月上海服务器与算力招标，请每天9:00汇总发送给我')
    assert '上海' in intent.regions
    assert '服务器' in intent.topic
    assert intent.schedule_cron == '0 9 * * *'
    assert intent.confidence >= 0.9
