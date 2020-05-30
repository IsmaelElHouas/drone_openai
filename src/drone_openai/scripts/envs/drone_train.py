#! /usr/bin/env python

import gym
import numpy as np
import rospy

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)
import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(0)
import logging
tf.get_logger().setLevel(logging.ERROR)

import parrotdrone_goto
from stable_baselines.deepq import DQN, MlpPolicy


def callback(lcl, _glb):
    """
    The callback function for logging and saving

    :param lcl: (dict) the local variables
    :param _glb: (dict) the global variables
    :return: (bool) is solved
    """
    # stop training if reward exceeds 199
    if len(lcl['episode_rewards'][-101:-1]) == 0:
        mean_100ep_reward = -np.inf
    else:
        mean_100ep_reward = round(float(np.mean(lcl['episode_rewards'][-101:-1])), 1)
    is_solved = lcl['self'].num_timesteps > 100 and mean_100ep_reward >= 0.9
    return not is_solved


def main():
    rospy.init_node('train_node', anonymous=True)
    env = gym.make("ParrotDroneGoto-v0")
    model = DQN(
        env=env,
        policy=MlpPolicy,
        learning_rate=1e-3,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
    )
    model.learn(total_timesteps=1000, callback=callback)

    # print("Saving model to cartpole_model.zip")
    # model.save("cartpole_model.zip")


if __name__ == '__main__':
    main()