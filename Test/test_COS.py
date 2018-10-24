#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:13:00 2018

@author: Kingther
"""
import sys
import numpy as np
sys.path.append('../Model/')
import COS
import model_utils as mu

from sklearn.tree import DecisionTreeRegressor

sk_regressor = DecisionTreeRegressor(max_depth=3)
sla = COS.SLA(sk_regressor)
action_space = mu.ActionSpace([-200,-100,0,100,200])
trading_cost = mu.trading_cost

epsilon_greedy = COS.EpsilonGreedy(action_space=action_space, utility_function=mu.utility_function,
                                   trading_cost=trading_cost, gamma=0.5, epsilon=0.9)


price_process_generator=COS.PriceProcessGenerator(theta = np.log(2) / 5, mu = 0, time = 1000, sigma = .15, p0 = 50)
simulator = COS.SimpleSimulator(liquidity_constant=0.1, price_process_generator=price_process_generator)
cos = COS.COS(sla, epsilon_greedy, simulator)

cos.train(n_iter=10, batch_size=250000)
fig = cos.plot_qval_func()
fig.show()