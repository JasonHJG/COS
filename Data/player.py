class Player:
    """
    define the player, who is able to buy and sell a stock he is holding
    the player has his own strategy, utility function
    the player needs to record each step the state and action
    """

    def __init__(self, stock, utility_function, strategy, action=[-200, -100, 0, 100, 200]):
        """
        initialize an instance of player in the stock market
        :param stock: stock the player is holding
        :param utility_function: the utility function of the player
        :param strategy: the RL strategy of the player
        :param action: list of possible movement of position
        """
        self.stock = stock
        self.utility_function = utility_function
        self.strategy = strategy
        self.action = action
        # dictionary to record what actions are taken and what are the pnls
        self.position = {}
        self.pnl = {}
        self.action_list = {}

    def trade_epsilon(self, epsilon=0.05):
        """
        trade according to epsilon greedy algorithm:
        with probability epsilon to trade randomly,
        with probability 1-epsilon not to trade
        :param epsilon: probability to trade randomly
        """
        


    def make_strategy(self, look_back, length_of_state=1):
        """
        make a strategy based on past observations
        :param look_back: int, number of steps to look back
        :param length_of_state: [1], number of steps to take as one state
        """
        index, price_list, liquidity_list = self.observe(look_back)
        # todo implement strategy class
        self.strategy.train(index, price_list, liquidity_list, self.position, self.utility_function,
                            length_of_state, self.action)

    def make_decision(self, length_of_state=1):
        """
        choose an action from action list
        :param length_of_state: [1], number of steps to take as one state
        :return: int, one action from action_list
        """
        price_list, liquidity_list = self.observe(length_of_state)
        return self.strategy.decide()

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
