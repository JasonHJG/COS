import numpy as np


class Strategy:
    """
    exploit and explore strategy
    """
    def __init__(self, learner):
        """
        initialize an instance of strategy class
        it is able to take observations of state-action pairs and use the learner inside it to train and predict
        :param learner: some supervised learner
        """
        self.learner = learner

    def epsilon_greedy(self, observed_states, actions, epsilon=0.05):
        """
        trade according to epsilon greedy algorithm:
        with probability epsilon to trade randomly,
        with probability 1-epsilon not to trade (action = 0)
        :param actions: int list of actions allowed to take
        :param epsilon: float probability to trade randomly
        :return: int action to make
        """
        # with probability epsilon, trading randomly
        ran = np.random.random()
        if ran < epsilon:  # trade randomly
            rand_index = np.random.randint(len(actions))
            action = actions[rand_index]
        # with probability 1-epsilon, trading greedily
        else:
            action = self.learner.predict(observed_states, actions)
        return action

    def upgrade(self, utility_dict, trade_book, gamma):
        """
        upgrade the learner with observations of one-step Sarsa target
        notice trade book at time t matches the utility at time t in our setting,
        :param utility_dict: dictionary of time_step(t): utility(t)
        :param trade_book: dictionary of time_step(t):[price(t), position(t), cash(t), action(t)]
        :param gamma: float between (0,1) discounting factor for that person
        """
        utility_dates = list(utility_dict)
        utility_dates.sort()
        X = []
        y = []
        for date in utility_dates:
            price = trade_book[date][0]
            position = trade_book[date][1]
            action = trade_book[date][3]
            state = np.array([price, position])
            X.append(np.r_[state, action]) # add position
            y.append(utility_dict[date]+ gamma * self.learner.qval(state, action))
        self.learner.fit(X, y)
