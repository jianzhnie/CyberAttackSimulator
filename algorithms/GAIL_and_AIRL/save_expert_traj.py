import argparse
import os
from pathlib import Path

import torch
import torch_npu
from gail_airl_ppo.algo.discrete import PPOExpert
from gail_airl_ppo.algo.discrete.utils import collect_demo
from gail_airl_ppo.env import make_env
from torch_npu.contrib import transfer_to_npu

PACKAGE_PATH = Path(__file__).parents[0]  # Abs path of package


def run(args):
    env = make_env(args.env_id)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    device = torch.device("cuda" if (
        torch.cuda.is_available() and args.cuda) else "cpu")
    torch.cuda.empty_cache()
    net_width = 64
    algo = PPOExpert(
        state_dim=state_dim,
        action_dim=action_dim,
        net_width=net_width,
        device=device,
        actor_path=args.actor_weight,
        critic_path=args.critic_weight,
    )

    buffer = collect_demo(env=env,
                          algo=algo,
                          buffer_size=args.buffer_size,
                          device=device,
                          std=args.std,
                          p_rand=args.p_rand,
                          seed=args.seed,
                          max_episode_steps=1000)

    buffer.save(
        os.path.join(
            'buffers', args.env_id,
            f'size{args.buffer_size}_std{args.std}_prand{args.p_rand}.pth'))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument(
        '--actor_weight',
        type=str,
        default=
        f'{PACKAGE_PATH}/gail_airl_ppo/model/default_18_node_network/actor/ppo_actor_100000.pth'
    )
    p.add_argument(
        '--critic_weight',
        type=str,
        default=
        f'{PACKAGE_PATH}/gail_airl_ppo/model/default_18_node_network/critic/ppo_critic_100000.pth'
    )

    p.add_argument('--env_id', type=str, default="default_18_node_network")
    p.add_argument('--buffer_size', type=int, default=10**4)
    p.add_argument('--std', type=float, default=0.0)
    p.add_argument('--p_rand', type=float, default=0.0)
    p.add_argument('--cuda', type=bool, default=False)
    p.add_argument('--seed', type=int, default=0)
    args = p.parse_args()
    run(args)
