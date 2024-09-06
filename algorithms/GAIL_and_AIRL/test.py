import torch
import torch_npu
import argparse
from pathlib import Path
from gail_airl_ppo.env import make_env
from gail_airl_ppo.algo.discrete import ALGOS
from gail_airl_ppo.algo.discrete import ALGOS, SerializedBuffer
from gail_airl_ppo.trainer_discrete import Trainer
from gail_airl_ppo.env import make_env
from torch_npu.contrib import transfer_to_npu

PACKAGE_PATH = Path(__file__).parents[0]  # Abs path of package


def run(args):
    env = make_env(args.env_id)
    eval_env = make_env(args.env_id)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    device = torch.device("cuda" if (torch.cuda.is_available() and args.cuda) else "cpu")
    torch.cuda.empty_cache()
    print(1111111111111111111111111111111111111111111111111)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--buffer', type=str,
                   default=f'{PACKAGE_PATH}/buffers/default_18_node_network/size10000_std0.0_prand0.0.pth')
    p.add_argument('--save_path', type=str, default=f'{PACKAGE_PATH}/irl_models/rl_models')
    p.add_argument('--rollout_length', type=int, default=1000)
    p.add_argument('--num_steps', type=int, default=10 ** 7)
    p.add_argument('--eval_interval', type=int, default=10000)
    p.add_argument('--save_interval', type=int, default=1e5)
    p.add_argument('--epoch_disc', type=int, default=20)
    p.add_argument('--epoch_ppo', type=int, default=200)
    p.add_argument('--env_id', type=str, default="default_18_node_network")
    p.add_argument('--algo', type=str, default='gail')
    p.add_argument('--cuda', type=bool, default=True)
    p.add_argument('--render', type=bool, default=False)
    p.add_argument('--write', type=bool, default=True)
    p.add_argument('--seed', type=int, default=0)
    args = p.parse_args()
    run(args)
