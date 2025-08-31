from datetime import datetime, timedelta, timezone

def formatTime(dt_utc=None):
    """
    Chuyển datetime UTC thành timestamp GMT+7
    
    Args:
        dt_utc (datetime, optional): datetime ở UTC. Mặc định là datetime.utcnow()
        
    Returns:
        int: timestamp (giây) theo GMT+7
    """
    if dt_utc is None:
        dt_utc = datetime.utcnow()
    tz_gmt7 = timezone(timedelta(hours=7))
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_gmt7 = dt_utc.astimezone(tz_gmt7)
    return int(dt_gmt7.timestamp())