class Player:
    """
    define the player, who is able to buy and sell a stock he is holding
    the player has his own strategy, utility function
    """

    def __init__(self, stock, share, utility_function, strategy, action=[-200, -100, 0, 100, 200]):
        """
        initialize an instance of player in the stock market
        :param stock: stock the player is holding
        :param share: number of share the player is holding
        :param utility_function: the utility function of the player
        :param strategy: the RL strategy of the player
        :param action: list of possible movement of position
        """
        self.stock = stock
        self.share = share
        self.utility_function = utility_function
        self.strategy = strategy
        self.pnl = []
        self.action_list = []


    def trade_one_step(self):
        """
        the player trade according to his strategy and the stock he is observing
        training and testing are done simultaneously in an online fashion
        """
        price_list, liquidity_list = self.observe()
        # todo implement strategy class
        action = self.strategy.decide(price_list, liquidity_list, self.share, self.utility_function)
        self.action_list.append(action)
        self.share += action

    def observe(self, n_steps):
        """
        the player observe n_step backward to help make the decision
        :param n_steps: int number of steps to look back in the history of stock
        :return: price list, liquidity list
        """
        return self.stock.get_history(n_steps)

    def calculate_pnl(self):
        """
        calculate the pnl from the previous time step
        :return: float, pnl from the previous day
        """

    def trade(self):
        """
        trade continuously
        """