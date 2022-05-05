from datetime import datetime

from app.common.utils import is_time_between


def test_time_between_function():
    datetime1 = datetime(2020, 1, 31, 13, 14, 31)
    datetime2 = datetime(2021, 1, 31, 17, 14, 31)
    timestamp1 = datetime.timestamp(datetime(2023, 1, 31, 6, 14, 31))
    timestamp2 = datetime.timestamp(datetime(2018, 1, 31, 9, 14, 31))

    assert is_time_between(datetime1.time()) is True
    assert is_time_between(datetime2.time()) is False
    assert is_time_between(datetime.fromtimestamp(timestamp1).time()) is True
    assert is_time_between(datetime.fromtimestamp(timestamp2).time()) is True
