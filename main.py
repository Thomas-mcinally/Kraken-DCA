import math
import requests

def place_limit_order(ticker:str, eur_budget:float):

    bid_price:str = get_bid_price(ticker)
    volume:str = get_trade_volume(eur_budget, bid_price)

    requests.post(
        url="https://api.kraken.com/0/private/AddOrder",
        json={
                "ordertype": "limit",
                "type": "buy",
                "volume": volume,
                "price": bid_price,
                "pair": ticker
        },
        headers={
            "API-Key": "fake123",
            "API-Sign": "fake123"
        }
    )
def round_down(n:float, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier
    
def get_bid_price(ticker:str) -> str:
    market_data:dict = requests.get(url=f"https://api.kraken.com/0/public/Ticker?pair={ticker}").json()
    top_market_bid = float(market_data["result"][ticker]["b"][0])
    my_bid_price = str(round_down(top_market_bid, decimals=6))
    
    return my_bid_price

def get_trade_volume(budget:float, bid_price:str) -> str:
    return str(budget/float(bid_price))


