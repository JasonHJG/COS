import numpy as np
import matplotlib.pyplot as plt


class Ornstein_Uhlenbeck:
    """
    define the OU process
    """

    def __init__(self, theta = np.log(2) / 5, mu = 0, time_step = 0.01, time = 100, sigma = .15, p0 = 150):
        """
        simulate OU process according to:
        X_n+1 = X_n + theta(mu - X_n)dt + sigma sqrt(dt) N~(0,1)
        :param theta: float parameter
        :param mu: float parameter
        :param time_step: minimium time interval
        :param time: total span of time
        :param sigma: float parameter
        """
        self.mu = mu
        self.sigma = sigma
        self.theta = theta
        self.time_step = time_step
        self.p0 = p0
        n_step = int(time/ time_step)
        self.n_step = n_step
        x_array = np.zeros(n_step)
        self.sqrt_dt = np.sqrt(time_step)
        for i in range(1, n_step):
            x_array[i] = x_array[i-1] + \
                         theta * (mu - x_array[i-1]) * time_step + \
                         sigma * self.sqrt_dt * np.random.normal(0,1)
        self.x_array = x_array
        self.time = time
        self.price_array = np.exp(self.x_array) * p0
        # use list for fast appending
        self.x_array = list(self.x_array)
        self.price_array = list(self.price_array)

    def get_price(self, n_days):
        """
        get the process as an array
        :param n_days: int, number of days before
        :return:
        """
        return self.price_array[-n_days:]

    def move_forward(self):
        """
        move the price process one day forward
        """
        last_x_data = self.x_array[-1]
        new_x_data = last_x_data + self.theta * (self.mu - last_x_data) * self.time_step + \
                         self.sigma * self.sqrt_dt * np.random.normal(0,1)
        new_price_data = np.exp(new_x_data) * self.p0
        self.x_array.append(new_x_data)
        self.price_array.append(new_price_data)

    def plot_x(self):
        """
        plot the underlying log process
        """
        plt.plot(np.linspace(0, self.time, self.n_step), self.x_array)

    def plot_price(self):
        """
        plot the process
        """
        plt.plot(np.linspace(0, self.time, self.n_step), self.price_array)
