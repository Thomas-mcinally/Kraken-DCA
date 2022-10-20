import requests

def place_limit_order(ticker:str, eur_budget:float):

    bid_price = get_bid_price(ticker)

    requests.post(
        url="https://api.kraken.com/0/private/AddOrder",
        json={
                "ordertype": "limit",
                "type": "buy",
                "volume": "0.002",
                "price": str(bid_price),
                "pair": ticker
        }
    )

def get_bid_price(ticker:str) -> float:
    market_data:dict[str, dict[str, dict[str, list[str]]]] = requests.get(url=f"https://api.kraken.com/0/public/Ticker?pair={ticker}").json()
    top_market_bid = float(market_data["result"][ticker]["b"][0])
    my_bid_price = round(top_market_bid, 6)
    return my_bid_price

