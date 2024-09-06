from .network.actor_critic import Actor, Critic
from .network.disc import AIRLDiscrim
from .network.disc import GAILDiscrim
from .ppo_discrete import PPO, PPOExpert
from .airl import AIRL
from .gail import GAIL
from .rollout_buffer import SerializedBuffer, RolloutBuffer
from .utils import disable_gradient, collect_demo

ALGOS = {
    'gail': GAIL,
    'airl': AIRL
}
