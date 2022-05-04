from datetime import datetime, time

from app.settings import settings


def is_time_between(check_time: time = None):

    open_market_at = settings.open_market_at.split(":")
    close_market_at = settings.close_market_at.split(":")
    begin_time = time(hour=int(open_market_at[0]), minute=int(open_market_at[1]))
    end_time = time(hour=int(close_market_at[0]), minute=int(close_market_at[1]))

    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time
