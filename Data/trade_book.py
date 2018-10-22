class Trade_book:
    """
    keep a record of all the transactions and the net worth
    """
    def __init__(self, time_step, price, position, cash, action):
        """
        initialize an instance of trade book
        :param time_step: time step for the information
        :param price: float, price of each share of a stock
        :param position: int, position of the stock
        :param cash: float, cash
        :param action: int, change in position
        """
        self.book = {}
        self.book[time_step] = [price, position, cash]

    def net_worth(self):
        """
        calculate the networth
        :return: dictionary of networth
        """
        time_steps = list(self.book)
        net_worth = {}
        for time in time_steps:
            price, position, cash = self.book[time]
            net_worth[time] = price * position + cash
        return net_worth

    def get_recent_information(self):
        """
        get the most recent information
        :return: time_step, price, position, cash
        """
        time_steps = list(self.book)
        time_steps.sort()
        recent_time_step = time_steps[-1]
        price, position, cash, action = self.book[recent_time_step]
        return recent_time_step, price, position, cash, action

    def add(self, time_step, action, price, trade_cost):
        """
        record the trade to the trade book, adjust cash according to trading cost
        :param time_step: index for time step
        :param action: share traded
        :param price: price for each share
        :param trade_cost: trade cost defined by the stock
        """
        _, last_price, last_postion, last_cash, _ = self.get_recent_information()
        self.book[time_step] = [price, last_postion+action, last_cash - trade_cost(action), action]
