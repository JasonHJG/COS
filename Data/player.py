import numpy as np
from .trade_book import Trade_book


class Player:
    """
    define the player, who is able to buy and sell a stock he is holding
    the player has his own strategy, utility function
    the player needs to record each step the state and action
    """

    def __init__(self, stock, utility_function, strategy, gamma = 0.8, action=[-200, -100, 0, 100, 200],
                 threshold=(0,1000)):
        """
        initialize an instance of player in the stock market
        :param stock: stock the player is holding
        :param utility_function: the utility function of the player
        :param strategy: the RL strategy of the player
        :param gamma: [0.8], float, speed of diminishing utility
        :param action: list of possible movement of position
        """
        self.stock = stock
        self.utility_function = utility_function
        self.strategy = strategy
        self.action = action
        self.gamma = gamma
        time_step, price, _ = self.stock.get_history(1)
        self.trade_book = Trade_book(time_step[0], price[0], 0, 0, 0)
        self.utility = {}
        self.threshold = threshold

    def calculate_utility(self):
        """
        calculate the utility at time T, which is determined by the change in wealth from T-1 to T
        :return: float, utility
        """
        net_worth = self.trade_book.calculate_net_worth()
        time_steps = list(net_worth)
        net_worth_value = list(net_worth.values())
        for i in range(len(time_steps)-1):
            self.utility[i] = self.utility_function(net_worth_value[i+1] - net_worth_value[i])
        return self.utility

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

    def trade_greedy_one_step(self, epsilon=.05):
        """
        trade one step forward
        :return:
        """
        step, price, liquid = self.observe(1)
        # get the players position
        _, _, position, _, _ = self.trade_book.get_recent_information()
        # add position
        state = np.array([price, position])
        action = self.strategy.epsilon_greedy(state, self.action, epsilon)
        if action + position > self.threshold[1] or action + position < self.threshold[0]:
            action = 0
        self.record(step[0], action, price[0], lambda x: self.stock.trade_cost(x, 10, 0.01))
        self.progress()

    def update_strategy(self, look_back=50000, length_of_state=1):
        """
        update Q function in strategy based on past observations
        :param look_back: int, number of steps to look back
        :param length_of_state: [1], number of steps to take as one state
        """
        utility_dict = self.calculate_utility()
        trade_book = self.trade_book.book
        self.strategy.upgrade(utility_dict, trade_book, self.gamma)
