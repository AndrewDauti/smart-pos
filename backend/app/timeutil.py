from datetime import datetime
from zoneinfo import ZoneInfo

LUSAKA = ZoneInfo("Africa/Lusaka")


def now_lusaka() -> datetime:
    return datetime.now(LUSAKA).replace(tzinfo=None)
