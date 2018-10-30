import numpy as np
from .trade_book import Trade_book


class Player:
    """
    define the player, who is able to buy and sell a stock he is holding
    the player has his own strategy, utility function
    the player needs to record each step the state and action
    """

    def __init__(self, stock, utility_function, strategy, gamma = 0.8, action=[-200, -100, 0, 100, 200],
                 threshold=(-1000,1000)):
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
        time_step, price, _ = self.stock.get_last_history()
        self.trade_book = Trade_book()
        self.trade_book.add_state(time_step, price, 0) #assume no initial position
        self.utility = {}
        self.threshold = threshold

    def observe(self, n_steps=1):
        """
        the player observe n_step backward to help make the decision
        :param n_steps: [1] int number of steps to look back in the history of stock
        :return: index list, price list, liquidity list
        """
        return self.stock.get_history(n_steps)

    def progress(self):
        """
        the stock the player is observing moves one step forward
        """
        self.stock.move_forward()

    def trade_greedy_one_step(self, epsilon=.05):
        """
        trade one step forward
        """
        # get the player's state at t
        time_step, price, position = self.trade_book.get_recent_state()
        state = np.array([price, position])
        # need to find the possible actions first
        possible_actions = []
        for action in self.action:
            if self.threshold[0] <= action + position <= self.threshold[1]:
                possible_actions.append(action)
        action = self.strategy.epsilon_greedy(state, possible_actions, epsilon)
        self.trade_book.add_action(time_step, action)
        self.progress()
        # update price and position at t+1
        next_time_step, next_price, _ = self.stock.get_last_history()
        next_position = position + action
        self.trade_book.add_state(next_time_step, next_price, next_position)
        # add player's utility at t
        dv = next_position * (next_price - price) - self.stock.trade_cost(action)
        utility = self.utility_function(dv)
        self.trade_book.add_utility(time_step, utility)

    def update_strategy(self, look_back=50000, length_of_state=1):
        """
        update Q function in strategy based on past observations
        :param look_back: int, number of steps to look back
        :param length_of_state: [1], number of steps to take as one state
        """
        trade_book = self.trade_book.book
        self.strategy.upgrade(trade_book, self.gamma)
        self._clean_trade_book()

    def _clean_trade_book(self):
        """
        clean trade book so that it only contains the most recent state
        """
        time_step, price, position = self.trade_book.get_recent_state()
        self.trade_book.clear()
        self.trade_book.add_state(time_step, price, position)
