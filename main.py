import requests

def place_limit_order(ticker:str, amount_to_purchase:float, leverage:float, limit_price:float):
    requests.post("https://api.kraken.com/0/private/AddOrder")
