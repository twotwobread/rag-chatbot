from datetime import datetime
from zoneinfo import ZoneInfo

UTC_TIMEZONE = ZoneInfo("UTC")
KST_TIMEZONE = ZoneInfo("Asia/Seoul")


def now_utc() -> datetime:
    return datetime.now(UTC_TIMEZONE)
