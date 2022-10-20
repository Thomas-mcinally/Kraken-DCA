import requests

def place_limit_order(ticker:str, eur_budget:float):

    requests.get(url=f"https://api.kraken.com/0/public/Ticker?pair={ticker}")

    requests.post(
        url="https://api.kraken.com/0/private/AddOrder",
        json={
                "ordertype": "limit",
                "type": "buy",
                "volume": 0.002,
                "pair": ticker
        }
    )
