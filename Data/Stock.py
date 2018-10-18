class Stock:
    """
    define a stock which has its own price process, liquidity process
    it can show its history at any point of time
    it also has its unique trade cost
    """

    def __init__(self, price_process, liquidity_process, trade_cost):
        """
        initialize an instance of Stock
        :param price_process: an array of price process
        :param liquidity_process: an array of liquidity process
        :param trade_cost: a function of trading cost
        """
        self.price_process = price_process
        self.liquidity_process = liquidity_process
        self.trade_cost = trade_cost



