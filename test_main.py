from main import place_limit_order

def test_input_arguments_exist():
    place_limit_order(ticker="ETH-USD", amount_to_purchase=0.002, leverage=0.0)