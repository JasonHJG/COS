import sys
sys.path.append('../Simulation/')
from ou_process import Ornstein_Uhlenbeck
import numpy as np

class PriceProcessGenerator():
    """
    A generator that generates OU process for price process
    """
    def __init__(self, theta = np.log(2) / 5, mu = 0, time = 1000, sigma = .15, p0 = 150):
        """
        a generator that generates OU process according to:
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
        self.time = time
        
    def generate_price_process(self, time=None):
        """
        generate OU process for price process
        """
        if time is None:
            time = self.time
        
        return Ornstein_Uhlenbeck(theta = self.theta, mu = self.mu, time = time, sigma = self.sigma, p0 = self.p0)
        
        

class SimpleSimulator():
    """
    A simple simulator that simulate constant for liquidity and ou process for price
    """
    def __init__(self,liquidity_constant=0.9, price_process_generator=PriceProcessGenerator()):
        """
        initialize a simple simulator
        :param liquidity_constant: float parameter
        :param price_process: process parameter
        """
        self.liquidity_constant = liquidity_constant
        self.price_process_generator = price_process_generator
        
    def get_states(self,time=None):
        """
        get the process as an array
        :param n_steps: int, number of days before
        :return: list of recent n steps of price data, list of the last n steps index
        """
        
        price_process = self.price_process_generator.generate_price_process(time)
        recent_price, recent_price_index = price_process.get_price(self.price_process_generator.time)
        recent_state = np.array([np.array([p,self.liquidity_constant]) for p in recent_price])
        return recent_state

