from .airl import AIRL
from .gail import GAIL
from .network.actor_critic import Actor, Critic
from .network.disc import AIRLDiscrim, GAILDiscrim
from .ppo_discrete import PPO, PPOExpert
from .rollout_buffer import RolloutBuffer, SerializedBuffer
from .utils import collect_demo, disable_gradient

ALGOS = {'gail': GAIL, 'airl': AIRL}
