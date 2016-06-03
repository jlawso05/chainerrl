from cached_property import cached_property
import chainer
from chainer import functions as F
from chainer import cuda
import numpy as np


class QOutput(object):
    """Struct that holds Q-function output and subproducts."""
    pass


class DiscreteQOutput(object):
    """Qfunction output for discrete action space."""

    def __init__(self, q_values):
        assert isinstance(q_values, chainer.Variable)
        self.xp = cuda.get_array_module(q_values.data)
        self.q_values = q_values
        self.n_actions = q_values.data.shape[1]

    @cached_property
    def greedy_actions(self):
        return chainer.Variable(
            self.q_values.data.argmax(axis=1).astype(np.int32))

    @cached_property
    def max(self):
        return F.select_item(self.q_values, self.greedy_actions)

    def sample_epsilon_greedy_actions(self, epsilon):
        assert self.q_values.data.shape[0] == 1, \
            "This method doesn't support batch computation"
        if np.random.random() < epsilon:
            return chainer.Variable(
                self.xp.asarray([np.random.randint(0, self.n_actions)],
                                dtype=np.int32))
        else:
            return self.greedy_actions

    def evaluate_actions(self, actions):
        assert isinstance(actions, chainer.Variable)
        return F.select_item(self.q_values, actions)

    def __repr__(self):
        return 'DiscreteQOutput greedy_actions:{} q_values:{}'.format(
            self.greedy_actions.data, self.q_values.data)


class ContinuousQOutput(object):
    """Qfunction output for continuous action space."""

    # TODO(fujita) implement

    @cached_property
    def greedy_actions(self):
        raise NotImplementedError

    @cached_property
    def max(self):
        raise NotImplementedError
