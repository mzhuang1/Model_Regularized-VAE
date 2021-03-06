import gym
import math
from misc.utils import toNatureDQNFormat
from misc.history import history

class environment(object):

    def __init__(self, params):
        self.game = params['game']
        self.image_format = params['image_format']
        self.history_length = params['history_length']
        self.env = gym.make(self.game)
        self.nActions = self.env.action_space.n
        obs = self.env.reset()
        self.total_reward = 0
        self.state_history = history({'history_length': self.history_length,\
                                      'image_format': self.image_format,\
                                      'start_frame': toNatureDQNFormat(obs)})
        self.reward = 0
        self.done = 0
        self.info = 0
    
    def take_step(self, action):
        if self.done == 0:
            obs, reward, self.done, \
                    self.info = self.env.step(action)
            self.state_history.update(toNatureDQNFormat(obs))
            # reward clipping
            self.reward = max(min(1, reward), -1)
            self.total_reward += reward
                    
    def take_random_step(self):
        action = 0
        if self.done == 0:
            action = self.env.action_space.sample()
            obs, reward, done, info = self.env.step(action)
            self.state_history.update(toNatureDQNFormat(obs))
            # reward clipping
            self.reward = max(min(1, reward), -1)
            self.total_reward += reward
        return action

    def reset_env(self):
        obs = self.env.reset()
        self.done = 0
        self.total_reward = 0
        self.reward = 0
        self.info = 0
        self.state_history.reset(toNatureDQNFormat(obs))

    def display_env(self):
        self.env.render()
