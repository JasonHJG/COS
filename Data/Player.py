import Stock as

class Player:
    """
    define the player, who is able to buy and sell a stock he is holding
    the player has his own strategy, utility function
    """

    def __init__(self, stock, share, utility_function, strategy):
        """
        initialize an instance of player in the stock market
        :param stock: stock the player is holding
        :param share: number of share the player is holding
        :param utility_function: the utility function of the player
        :param strategy: the RL strategy of the player
        """
        self.stock = stock
        self.share = share
        self.utility_function = utility_function
        self.strategy = strategy
        # still need to consider the net worth

    def long(self, amount):
        """
        long the stock by the amount
        :param amount: int
        """

    def short(self, amount):
        """
        short the stock by the amount
        :param amount: int
        """
