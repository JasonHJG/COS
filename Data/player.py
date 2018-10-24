import numpy as np
from .trade_book import Trade_book


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
        :param trade_book: a book to keep track of the player's position and cash
        :param action: list of possible movement of position
        """
        self.stock = stock
        self.utility_function = utility_function
        self.strategy = strategy
        self.action = action
        time_step, price, _ = self.stock.get_history(1)
        self.trade_book = Trade_book(time_step[0], price[0], 0, 0, 0)
        self.utility = {}

    def calculate_utility(self):
        """
        calculate the utility at time T, which is determined by the change in wealth from T-1 to T
        :return: float, utility
        """
        net_worth = self.trade_book.calculate_net_worth()
        time_steps = list(net_worth)
        self.utility[time_steps[0]] = 0  # initialization
        net_worth_value = list(net_worth.values())
        for i in range(1, len(time_steps)):
            self.utility[i] = self.utility_function(net_worth_value[i] - net_worth_value[i - 1])

    def observe(self, n_steps=1):
        """
        the player observe n_step backward to help make the decision
        :param n_steps: [1] int number of steps to look back in the history of stock
        :return: index list, price list, liquidity list
        """
        return self.stock.get_history(n_steps)

    def record(self, time_step, action, price, trade_cost):
        """
        record the trade to the trade book
        :param time_step: index for time step
        :param action: share traded
        :param price: price for each share
        :param trade_cost: trade cost defined by the stock
        """
        self.trade_book.add(time_step, action, price, trade_cost)

    def progress(self):
        """
        the stock the player is observing moves one step forward
        """
        self.stock.move_forward()

    def epsilon_greedy(self, epsilon=0.05):
        """
        trade according to epsilon greedy algorithm:
        with probability epsilon to trade randomly,
        with probability 1-epsilon not to trade (action = 0)
        :param epsilon: probability to trade randomly
        """
        index, price, liquidity = self.observe(1)
        index = index[0]
        price = price[0]
        liquidity = liquidity[0] # for this time being, liquidity is not used
        ran = np.random.random()
        if ran < epsilon: # trade randomly
            rand_index = np.random.randint(len(self.action))
            action = self.action[rand_index]
        else:
            action = self.strategy.decide(price) # look at the current state and take action to maximize the gain
        self.record(index, action, price, self.stock.trade_cost)

    def update_strategy(self, look_back, length_of_state=1):
        """
        update Q function in strategy based on past observations
        :param look_back: int, number of steps to look back
        :param length_of_state: [1], number of steps to take as one state
        """
        index, price_list, liquidity_list = self.observe(look_back)
        # todo implement strategy class
        self.strategy.train(index, price_list, liquidity_list, self.position, self.utility_function,
                            length_of_state, self.action)

