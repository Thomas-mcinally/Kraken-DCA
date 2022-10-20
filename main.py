import requests

def place_limit_order(ticker:str, eur_budget:float):

    bid_price = get_bid_price(ticker)

    requests.post(
        url="https://api.kraken.com/0/private/AddOrder",
        json={
                "ordertype": "limit",
                "type": "buy",
                "volume": "0.002",
                "price": "19200.1",
                "pair": ticker
        }
    )

def get_bid_price(ticker:str) -> float:
    market_data = requests.get(url=f"https://api.kraken.com/0/public/Ticker?pair={ticker}")
    return float(0)

