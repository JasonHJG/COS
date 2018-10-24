from sklearn.base import clone
from sklearn.tree import DecisionTreeRegressor
import model_utils as mu
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from Simulator import *

class SLA():
    """
    Supervised Learner Averaging
    """

    def __init__(self, sk_regressor=DecisionTreeRegressor()):
        """
        initialize an instance of COS learner
        """
        self.regressor = sk_regressor
        self.supervised_learners = []
        
        
    def qval(self, state,action):
        """
        compute q values for state,action
        """
        if not self.supervised_learners :
            return 0.
        else:
            x = mu.compute_x(state, action)
            return np.mean([sl.predict(x) for sl in self.supervised_learners])
            
    def predict(self, X):
        """
        predict yhat using X
        """
        if not self.supervised_learners :
            return np.zeros(len(X))
        else:
            return np.array([sl.predict(X) for sl in self.supervised_learners]).mean(axis=0)
        
    def fit(self, X, y):
        """
        fit the next batch of training data with a new supervised_learner
        """
        sl = clone(self.regressor)
        self.supervised_learners.append(sl.fit(X,y))


class SLOA():
    """
    Supervised Learner Online Averaging
    """

    def __init__(self, sk_regressor=DecisionTreeRegressor(), n_regressor=25):
        """
        initialize an instance of COS learner
        """
        self.regressor = sk_regressor
        self.supervised_learners = deque()
        self.n_regressor = n_regressor
        
        
    def qval(self, state,action):
        """
        compute q values for state,action
        """
        if not self.supervised_learners :
            return 0.
        else:
            x = mu.compute_x(state, action)
            return np.mean([sl.predict(x) for sl in self.supervised_learners])
            
    def predict(self, X):
        """
        predict yhat using X
        """
        if not self.supervised_learners :
            return np.zeros(len(X))
        else:
            return np.array([sl.predict(X) for sl in self.supervised_learners]).mean(axis=0)
        
    def fit(self, X, y):
        """
        fit the next batch of training data with a new supervised_learner
        """
        sl = clone(self.regressor)
        self.supervised_learners.append(sl.fit(X,y))  
        if len(self.supervised_learners)>self.n_regressor:
            self.supervised_learners.popleft()
            
        
        
        
class EpsilonGreedy():
    """
    Epsilon Greedy Algorithm
    """
    def __init__(self,action_space, utility_function, trading_cost, gamma=0.99, epsilon=1e-2):
        """
        Initialize a Epsilon Greedy Algorithm
        :param action_space: ActionSpace
        :param utility_function: func
        :param trading_cost: func
        :param gamma: float, discount factor, value in [0,1]
        :param epsilon: float, probability to explore, value in [0,1]
        """
        self.action_space = action_space
        self.qval_function = lambda state,action: 0
        self.utility_function = utility_function
        self.trading_cost = trading_cost
        self.epsilon = epsilon
        self.gamma = gamma
        
    
        
    def update_qval_function(self,sla):
        """
        update the qval_function with a SLA
        :param sla: SLA
        """
        self.qval_function = sla.qval
        
        
    def explore_exploit(self,simulated_state_process, max_position=10000, min_position=0):
        """
        decide whether to explore or exploit
        :param simulated_state_process: np.array
        """
        # explore: 1, exploit: 0
        count = len(simulated_state_process)
        exps = np.random.binomial(n=1, p=self.epsilon, size=count)
        actions = np.zeros(count)
        positions = np.zeros(count)
        rewards = np.zeros(count)
        states = simulated_state_process
        for i in range(count-1):
            compute_dv = lambda act: positions[i]*(states[i+1,0]-states[i,0]) - self.trading_cost(share=act, liquidity=states[i,1])
            compute_reward = lambda act: self.utility_function(dV=compute_dv(act)) + self.gamma * self.qval_function(state=states[i],action=act)
            
            available_action_space = self.action_space.available_space(curr_position=positions[i],
                                                                       max_position=max_position,
                                                                       min_position=min_position)
            
            if exps[i] == 0:
                rewards_acts = [compute_reward(act) for act in available_action_space]
                
                idx_greedy_policy = rewards_acts.index(max(rewards_acts))
                actions[i] = available_action_space[idx_greedy_policy]
                
            else:
                actions[i] = self.action_space.uniform_sample_available(curr_position=positions[i],
                                                                        max_position=max_position,
                                                                        min_position=min_position)
                
            # update rewards and position
            
            positions[i+1] = positions[i] + actions[i]
            rewards[i] = compute_reward(actions[i])
        #plt.plot(positions)
                
        X = mu.compute_X(states=states, actions=actions)
        y = rewards
        return X, y
        
class COS():
    """
    abbreviation for Continuous Online Supervised reinforcement learning
    """
    def __init__(self,sla, epsilon_greedy, simulator):
        """
        Initialize a COS learner
        :param sla: SLA
        :param epsilon_greedy: EpsilonGreedy
        :param simulator: Simulator
        """
        self.sla = sla
        self.epsilon_greedy = epsilon_greedy
        self.simulator = simulator
        
    def train(self,n_iter = 100,batch_size = 1000):
        for i in range(n_iter):
            simulated_state_process = self.simulator.get_states(time=batch_size)
            X,y = self.epsilon_greedy.explore_exploit(simulated_state_process)
            self.sla.fit(X,y)
            self.epsilon_greedy.update_qval_function(self.sla)
            
    def generate_strategy(self):
        def trading_strategy(state_process, action_space):
            count = len(state_process)
            actions = np.zeros(count)
            positions = np.zeros(count)
            
            for i in range(count-1):
                compute_dv = lambda act: positions[i]*(state_process[i+1,0]-state_process[i,0]) - self.epsilon_greedy.trading_cost(share=act, liquidity=state_process[i,1])
                compute_reward = lambda act: self.epsilon_greedy.utility_function(dV=compute_dv(act)) + self.gamma * self.sla.qval(state=state_process[i],action=act)
                rewards_acts = [compute_reward(act) for act in self.action_space.values]
                idx_greedy_policy = rewards_acts.index(max(rewards_acts))
                actions[i] = action_space.get(idx_greedy_policy)
                    
                # update position
                positions[i+1] = positions[i] + actions[i]
            return positions
        return trading_strategy
        
    def plot_qval_func(self):
        colors = ["b","g","r","c","m","y","k"]
        fig, ax = plt.subplots(figsize=(12,6))
        ps = np.arange(0,150,1)
        ax.set_xlim(ps[0],ps[-1])
        n = len(ps)
        action_space = self.epsilon_greedy.action_space
        for i,act in enumerate(action_space.values):
            X = np.c_[ps,np.ones(n)*0.5,np.ones(n)*act]
            q_hat = self.sla.predict(X)
            ax.scatter(ps,q_hat,label=str(act),c=colors[i%len(colors)],marker='o',linewidths=0)
        ax.legend()
        return fig
