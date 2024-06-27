import time

from simulator.env.graph_explore import GraphExplore

if __name__ == '__main__':
    env = GraphExplore(graph_name='random_internet',
                       num_nodes=1000,
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
