import os
import sys
import time

sys.path.append(os.getcwd())

from cyberattacksim.envs.specific.graph_explore import GraphExplore

if __name__ == '__main__':
    env = GraphExplore(graph_name='path_graph',
                       num_nodes=10000000,
                       game_max=1000)
    _ = env.reset()
    done = False
    steps = 0
    start_time = time.time()
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        print('reward:', reward)
        steps += 1
    end_time = time.time()
    print(
        f'Episode finished after {steps} steps. Time taken: {end_time - start_time} seconds'
    )
