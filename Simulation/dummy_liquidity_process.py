class Dummy_liquidity_process:
    """
    case for a dummy liquidity process, the process is normalized and for simplicity assume to be 0.5
    """

    def __init__(self, time_step, time):
        """
        initialize the constant liquidity process
        :param time_step: float, unit time
        :param time: float, total time span
        """
        n_step = int(time / time_step)
        self.liquidity_process = np.ones(n_step) * 0.5

    def move_forward(self):
        """
        move forward for one step
        """
        self.liquidity_process.append(0.5)

    def get_process(self, n_steps):
        """
        get the liquidity process for the previous n steps
        :param n_steps: int
        :return: list of recent n steps of liquidity data
        """
        return self.liquidity_process[-n_steps:]
