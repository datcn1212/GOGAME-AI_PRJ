from agent.rl_agent import *
from agent.rl_env import *
from numpy.random import normal

if __name__ == '__main__':
    # Train and save ApproxQAgent
    # approx_q_agent = ApproxQAgent('BLACK', RlEnv())
    # approx_q_agent.train(1000, 0.001, 0.9, 0.1)
    # approx_q_agent.save()
    print(normal(1, 0.1))