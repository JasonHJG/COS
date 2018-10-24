from sklearn.base import clone
from sklearn.tree import DecisionTreeRegressor
import numpy as np


class SLA:
    """
    Supervised Learner Averaging
    """

    def __init__(self, sk_regressor=DecisionTreeRegressor()):
        """
        initialize an instance of COS learner
        """
        self.regressor = sk_regressor
        self.supervised_learners = []

    def qval(self, state, action):
        """
        compute q values for state,action
        """
        if not self.supervised_learners:
            return 0.
        else:
            x = mu.compute_x(state, action)
            return np.mean([sl.predict(x) for sl in self.supervised_learners])

    def predict(self, X):
        """
        predict yhat using X
        """
        if not self.supervised_learners:
            return np.zeros(len(X))
        else:
            return np.array([sl.predict(X) for sl in self.supervised_learners]).mean(axis=0)

    def fit(self, X, y):
        """
        fit the next batch of training data with a new supervised_learner
        """
        sl = clone(self.regressor)
        self.supervised_learners.append(sl.fit(X, y))