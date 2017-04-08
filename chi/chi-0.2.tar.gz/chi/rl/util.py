import numpy as np
from gym import Wrapper, Env
from gym.spaces import Box


def print_env(env: Env):
  spec = getattr(env, 'spec', False)
  if spec:
    from gym.envs.registration import EnvSpec
    print(f'Env spec: {vars(spec)}')

  acsp = env.action_space
  obsp = env.observation_space

  if isinstance(acsp, Box):
    print(f'Continuous action space = [{acsp.high}, {acsp.low}]')

  if isinstance(obsp, Box):
    print(f'Continuous observation space = [{obsp.high}, {obsp.low}]')


class DiscretizeActions(Wrapper):
  def __init__(self):
    pass


class PenalizeAction(Wrapper):
  def __init__(self, env, alpha=.01, slack=.5):
    super().__init__(env)
    self.alpha = alpha
    self.slack = slack

  def _step(self, action):
    s, r, t, i = super()._step(action)
    assert isinstance(self.env, Env)
    assert isinstance(self.env.action_space, Box)
    l = self.env.action_space.low
    h = self.env.action_space.high
    m = h - l
    dif = (action - np.clip(action, l - self.slack * m, h + self.slack * m))
    r -= self.alpha * np.mean(np.square(dif / m))
    return s, r, t, i