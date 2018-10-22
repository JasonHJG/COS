#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:13:00 2018

@author: Kingther
"""
import sys
sys.path.append('../Model/')
import COS
import model_utils as mu

from sklearn.tree import DecisionTreeRegressor

sk_regressor = DecisionTreeRegressor()#max_depth=3)
sla = COS.SLA(sk_regressor)
action_space = mu.ActionSpace([-100,-200,0,100,200])
epsilon_greedy = COS.EpsilonGreedy(action_space=action_space, utility_function=mu.utility_function,
                                   trading_cost=mu.trading_cost, gamma=0.9, epsilon=1e-2)
simulator = COS.SimpleSimulator()
cos = COS.COS(sla, epsilon_greedy, simulator)

cos.train(n_iter=20, batch_size=500000)
cos.plot_qval_func()