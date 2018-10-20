import numpy as np


class Dummy_liquidity_process:
    """
    case for a dummy liquidity process, the process is normalized and for simplicity assume to be 0.5
    """

    def __init__(self, time):
        """
        initialize the constant liquidity process
        :param time: float, total time span
        """
        self.liquidity_dict = {}
        n_step = int(time)
        liquidity_process = np.ones(n_step) * 0.5
        for i in range(len(liquidity_process)):
            self.liquidity_dict[i] = liquidity_process[i]

    def move_forward(self):
        """
        move forward for one step
        """
        last_time_step = list(self.liquidity_dict)[-1]
        self.liquidity_dict[last_time_step+1] = 0.5

    def get_process(self, n_steps):
        """
        get the liquidity process for the previous n steps
        :param n_steps: int
        :return: list of recent n steps of liquidity data, list of recent n steps index
        """
        recent_process = []
        process_index_array = list(self.liquidity_dict)
        process_index_array.sort()
        recent_process_index = process_index_array[- n_steps:]
        for i in recent_process_index:
            recent_process.append(self.liquidity_dict_dict[i])
        return recent_process, recent_process_index
