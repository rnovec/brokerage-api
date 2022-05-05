from datetime import datetime

BUY_ORDER_TEST_PAYLOAD = {
    "timestamp": datetime.timestamp(datetime(2020, 1, 31, 13, 14, 31)),
    "operation": "BUY",
    "issuer_name": "AAPL",
    "total_shares": 2,
    "shared_price": 50,
}

SELL_ORDER_TEST_PAYLOAD = {
    "timestamp": datetime.timestamp(datetime(2021, 1, 31, 13, 14, 31)),
    "operation": "SELL",
    "issuer_name": "AAPL",
    "total_shares": 2,
    "shared_price": 50,
}

CLOSED_MARKET_ORDER_TEST_PAYLOAD = {
    "timestamp": datetime.timestamp(datetime(2022, 1, 31, 17, 14, 31)),
    "operation": "SELL",
    "issuer_name": "AAPL",
    "total_shares": 2,
    "shared_price": 50,
}
