from Simulation import Ornstein_Uhlenbeck
from Simulation import Dummy_liquidity_process


class Stock:
    """
    define a stock which has its own price process, liquidity process
    it can show its history at any point of time
    it also has its unique trade cost
    """

    def __init__(self, price_process, liquidity_process, trade_cost):
        """
        initialize an instance of Stock
        :param price_process: an instance of price process
        :param liquidity_process: an instance of liquidity process
        :param trade_cost: a function of trading cost
        """
        self.price_process = price_process
        self.liquidity_process = liquidity_process
        self.trade_cost = trade_cost

    def move_forward(self):
        """
        move one unit step forward
        """
        self.price_process.move_forward()
        self.liquidity_process.move_forward()

    def get_history(self, n_steps):
        """
        get the history of price_process and liquidity_process for the previous n steps
        :param n_steps: int
        :return: list of recent n steps of price and liquidity data
        """
        return self.price_process.get_price(n_steps), self.liquidity_process.get_process(n_steps)
