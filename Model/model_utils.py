#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 12:09:20 2018

@author: Kingther
"""
import numpy as np

class State():
    """
    A simple state data struction including price and liquidity
    """
    def __init__(self,price,liquidity):
        """
        initialize the state
        :param time: float, total time span
        """
        self.values = np.array([price,liquidity])
    
    def get_price(self):
        return self.values[0]

    def get_liquidity(self):
        return self.values[1]
        
        
class ActionSpace():
    def __init__(self, values):
        self.values = values
        
    def get(self, idx):
        return self.values[idx]
        
    def available_space(self, curr_position, max_position, min_position):
        avlb_space=[v for v in self.values if (curr_position+v<=max_position and curr_position+v>=min_position)]
        #print([(curr_position,v)  for v in self.values if (curr_position+v<=max_position and curr_position+v>=min_position)])
        return avlb_space
        
    def uniform_sample_available(self, curr_position, max_position, min_position):
        return  np.random.choice(self.available_space(curr_position, max_position, min_position))
        
    def uniform_sample(self,count=None):
        if count is None:
            return np.random.choice(self.values)
        else:
            return np.random.choice(self.values,count)
        
def compute_x(state, action):
    X = np.r_[state,action].reshape((1,-1))
    return X
    
def compute_X(states, actions):
    X = np.c_[states,actions]
    return X
   

def utility_function(dV, k=0.1):
    """
    calculate the utility function according to utility = dV - .5k * dV^2
    :param dV: change in the price of each share
    :param k: float between 0 and 1, risk aversion parameter
    :return: utility
    """
    return dV - 0.5 * k * dV * dV


def trading_cost(share, liquidity, ts=0.1):
    """
    calculate trading cost based on cost(share) = mul * ts *(abs(share)+0.01 * share^2)
    :param share: int, number of share
    :param liquidity: float, liquidity
    :param ts: float, ticker size
    :return: trading cost
    """
    return 1./liquidity * ts * (np.abs(share) + 0.01 * share * share)
