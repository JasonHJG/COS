class Trade_book:
    """
    keep a record of all the transactions and the net worth
    """
    def __init__(self, price, position, cash):
        """
        initialize an instance of trade book
        :param price: float, price of each share of a stock
        :param position: int, position of the stock
        :param cash: float, cash
        """
        self.book = {}
        self.book[0] = [price, position, cash]

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

    def update(self, action, price, trade_cost):
        """
        update the trade book when an action is taken
        :param action: int, change in the position
        :param price: float, current stock price
        :param trade_cost: function,
        :return:
        """