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
        n_step = int(time/ time_step)
        self.n_step = n_step
        x_array = np.zeros(n_step)
        sqrt_dt = np.sqrt(time_step)
        for i in range(1, n_step):
            x_array[i] = x_array[i-1] + \
                         theta * (mu - x_array[i-1]) * time_step + \
                         sigma * sqrt_dt * np.random.normal(0,1)
        self.x_array = x_array
        self.time = time
        self.price_array = np.exp(self.x_array) * p0

    def plot_x(self):
        plt.plot(np.linspace(0, self.time, self.n_step), self.x_array)

    def plot_price(self):
        plt.plot(np.linspace(0, self.time, self.n_step), self.price_array)

    def get_price(self):
        return self.price_array








