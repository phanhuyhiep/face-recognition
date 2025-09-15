from datetime import datetime
from zoneinfo import ZoneInfo
from configs.core_config import CoreSettings

TIME_ZONE = CoreSettings.TIME_ZONE

def current_time_vn_by_timestamp() -> int:
    """Lấy thời gian hiện tại theo giờ VN (UTC+7) dạng timestamp."""
    return int(datetime.now(TIME_ZONE).timestamp())
