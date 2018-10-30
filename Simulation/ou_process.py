import numpy as np
import matplotlib.pyplot as plt


class Ornstein_Uhlenbeck:
    """
    define the OU process
    """

    def __init__(self, theta = np.log(2) / 5, mu = 0, time = 1000, sigma = .15, p0 = 50):
        """
        simulate OU process according to:
        X_n+1 = X_n + theta(mu - X_n)dt + sigma sqrt(dt) N~(0,1)
        :param theta: float parameter
        :param mu: float parameter
        :param time: total span of time
        :param sigma: float parameter
        """
        self.mu = mu
        self.sigma = sigma
        self.theta = theta
        self.p0 = p0
        n_step = int(time)
        self.n_step = n_step
        x_array = np.zeros(n_step)
        self.sqrt_dt = 1
        for i in range(1, n_step):
            x_array[i] = x_array[i-1] + \
                         theta * (mu - x_array[i-1]) * 1 + \
                         sigma * self.sqrt_dt * np.random.normal(0,1)
        self.x_array = x_array
        self.time = time
        self.price_array = np.exp(self.x_array) * p0
        # use dictionary to contain all information such that
        # we can find time stamp with corresponding price
        self.x_dict = {}
        self.price_dict = {}
        self.x_array = list(self.x_array)
        self.price_array = list(self.price_array)
        for i in range(len(self.x_array)):
            self.x_dict[i] = self.x_array[i]
            temp = round(self.price_array[i], 1)
            if temp <= 100:
                self.price_dict[i] = round(self.price_array[i],1)
            else:
                self.price_dict[i] = round(100.0,1)
        self.last_time_step = len(self.x_array) - 1

    def clear(self):
        """
        remove all other price, only keep the last one
        """
        last_time = self.get_last_time_step()
        last_price = self.price_dict[last_time]
        last_x = self.x_dict[last_time]
        self.price_dict.clear()
        self.x_dict.clear()
        self.price_dict[last_time] = last_price
        self.x_dict[last_time] = last_x

    def get_price(self, n_steps):
        """
        get the process as an array
        :param n_steps: int, number of days before
        :return: list of recent n steps of price data, list of the last n steps index
        """
        recent_price = []
        price_index_array = list(self.price_dict)
        price_index_array.sort()
        recent_price_index = price_index_array[- n_steps:]
        for i in recent_price_index:
            recent_price.append(self.price_dict[i])
        return recent_price, recent_price_index

    def move_forward(self):
        """
        move the price process one day forward
        """
        time_steps = list(self.x_dict)
        last_x_data = self.x_dict[time_steps[-1]]
        new_x_data = last_x_data + self.theta * (self.mu - last_x_data) * 1 + \
                      self.sigma * self.sqrt_dt * np.random.normal(0, 1)
        new_price_data = round(np.exp(new_x_data) * self.p0,1)
        if new_price_data <= 100:
            new_price_data = new_price_data
        else:
            new_price_data = 100
        self.x_dict[time_steps[-1]+1] = new_x_data
        self.price_dict[time_steps[-1]+1] = new_price_data
        # update the last step
        self.last_time_step += 1

    def plot_x(self):
        """
        plot the underlying log process
        """
        plt.plot(np.linspace(0, self.time, self.n_step), list(self.x_dict.values()))

    def plot_price(self):
        """
        plot the process
        """
        plt.plot(np.linspace(0, self.time, self.n_step), list(self.price_dict.values()))

    def get_last_time_step(self):
        """
        get the last time step
        :return: int, most recent time step
        """
        return self.last_time_step
