from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RLArguments:
    """Common settings for Reinforcement Learning algorithms."""

    # Common settings
    project: str = field(
        default='rltoolkit',
        metadata={'help': "Name of the project. Defaults to 'rltoolkit'"},
    )
    algo_name: str = field(
        default='dqn',
        metadata={'help': "Name of the algorithm. Defaults to 'dqn'"},
    )
    use_cuda: bool = field(
        default=True,
        metadata={'help': 'Whether to use CUDA. Defaults to True'},
    )
    torch_deterministic: bool = field(
        default=False,
        metadata={
            'help':
            'Whether to use deterministic operations in CUDA. Defaults to True'
        },
    )
    seed: int = field(
        default=42,
        metadata={
            'help': 'Seed for environment randomization. Defaults to 42'
        },
    )
    # Environment settings
    env_id: str = field(
        default='CartPole-v0',
        metadata={'help': "The environment name. Defaults to 'CartPole-v0'"},
    )
    num_envs: int = field(
        default=10,
        metadata={
            'help':
            'Number of parallel environments to run for collecting experiences. Defaults to 10'
        },
    )
    capture_video: Optional[bool] = field(
        default=None,
        metadata={
            'help':
            'Flag indicating whether to capture videos of the environment during training.'
        },
    )
    # ReplayBuffer settings
    buffer_size: int = field(
        default=10000,
        metadata={
            'help': 'Maximum size of the replay buffer. Defaults to 10000'
        },
    )
    batch_size: int = field(
        default=32,
        metadata={
            'help':
            'Size of the mini-batches sampled from the replay buffer during training. Defaults to 32'
        },
    )
    # Training parameters
    n_steps: int = field(
        default=1,
        metadata={
            'help':
            'Number of steps to take before updating the target network. Defaults to 1'
        },
    )
    max_timesteps: int = field(
        default=12000,
        metadata={
            'help': 'Maximum number of training steps. Defaults to 12000'
        },
    )
    gamma: float = field(
        default=0.99,
        metadata={
            'help': 'Discount factor for future rewards. Defaults to 0.99'
        },
    )
    eval_episodes: int = field(
        default=10,
        metadata={'help': 'Number of episodes to evaluate. Defaults to 10'},
    )
    # Logging and saving
    work_dir: str = field(
        default='work_dirs',
        metadata={
            'help':
            "Directory for storing work-related files. Defaults to 'work_dirs'"
        },
    )
    save_model: Optional[bool] = field(
        default=False,
        metadata={
            'help': 'Flag indicating whether to save the trained model.'
        },
    )
    train_log_interval: int = field(
        default=5,
        metadata={'help': 'Logging interval during training. Defaults to 10'},
    )
    test_log_interval: int = field(
        default=10,
        metadata={
            'help': 'Logging interval during evaluation. Defaults to 20'
        },
    )
    save_interval: int = field(
        default=1000,
        metadata={'help': 'Frequency of saving the model. Defaults to 1000'},
    )
    logger: str = field(
        default='wandb',
        metadata={
            'help': "Logger to use for recording logs. Defaults to 'wandb'"
        },
    )


@dataclass
class DQNArguments(RLArguments):
    """DQN-specific settings."""

    hidden_dim: int = field(
        default=128,
        metadata={
            'help':
            'The hidden dimension size of the neural network. Defaults to 128'
        },
    )
    double_dqn: bool = field(
        default=False,
        metadata={
            'help':
            'Flag indicating whether to use Double DQN. Defaults to False'
        },
    )
    dueling_dqn: bool = field(
        default=False,
        metadata={
            'help':
            'Flag indicating whether to use Dueling DQN. Defaults to False'
        },
    )
    learning_rate: float = field(
        default=1e-3,
        metadata={
            'help': 'Learning rate used by the optimizer. Defaults to 1e-4'
        },
    )
    min_learning_rate: float = field(
        default=1e-5,
        metadata={
            'help':
            'Minimum learning rate used by the optimizer. Defaults to 1e-5'
        },
    )
    lr_scheduler_method: str = field(
        default='linear',
        metadata={
            'help':
            "Method used for learning rate scheduling. Defaults to 'linear'"
        },
    )
    eps_greedy_start: float = field(
        default=1.0,
        metadata={
            'help':
            'Initial value of epsilon for epsilon-greedy exploration. Defaults to 1.0'
        },
    )
    eps_greedy_end: float = field(
        default=0.1,
        metadata={
            'help':
            'Final value of epsilon for epsilon-greedy exploration. Defaults to 0.1'
        },
    )
    eps_greedy_scheduler: str = field(
        default='linear',
        metadata={
            'help':
            "Type of scheduler used for epsilon-greedy exploration. Defaults to 'linear'"
        },
    )
    max_grad_norm: float = field(
        default=None,
        metadata={'help': 'Maximum gradient norm. Defaults to 1.0'},
    )
    use_smooth_l1_loss: bool = field(
        default=False,
        metadata={
            'help':
            'Flag indicating whether to use the smooth L1 loss. Defaults to False'
        },
    )
    warmup_learn_steps: int = field(
        default=1000,
        metadata={
            'help':
            'Number of steps before starting to update the model. Defaults to 1000'
        },
    )
    target_update_frequency: int = field(
        default=100,
        metadata={
            'help': 'Frequency of updating the target network. Defaults to 100'
        },
    )
    soft_update_tau: float = field(
        default=1.0,
        metadata={
            'help':
            'Interpolation parameter for soft target updates. Defaults to 1.0'
        },
    )
    train_frequency: int = field(
        default=10,
        metadata={'help': 'Frequency of training updates. Defaults to 1'},
    )
    gradient_steps: int = field(
        default=2,
        metadata={
            'help':
            'Number of times to update the learner network. Defaults to 1'
        },
    )


@dataclass
class A2CArguments(RLArguments):
    hidden_dim: int = field(
        default=128,
        metadata={
            'help':
            'The hidden dimension size of the neural network. Defaults to 128'
        },
    )
    entropy_weight: float = field(
        default=0.01,
        metadata={
            'help':
            'Entropy weight for the policy gradient method. Defaults to 0.01'
        },
    )

    actor_lr: float = field(
        default=1e-4,
        metadata={
            'help': 'Learning rate for the actor network. Defaults to 1e-4'
        },
    )
    critic_lr: float = field(
        default=1e-4,
        metadata={
            'help': 'Learning rate for the critic network. Defaults to 1e-4'
        },
    )


@dataclass
class PPOArguments(RLArguments):
    """PPO-specific settings."""

    hidden_dim: int = field(
        default=64,
        metadata={
            'help':
            'The hidden dimension size of the neural network. Defaults to 128'
        },
    )
    learning_rate: float = field(
        default=1e-2,
        metadata={'help': 'Learning rate for the optimizer. Defaults to 1e-4'},
    )
    actor_lr: float = field(
        default=1e-4,
        metadata={
            'help': 'Learning rate for the actor network. Defaults to 1e-4'
        },
    )
    critic_lr: float = field(
        default=1e-4,
        metadata={
            'help': 'Learning rate for the critic network. Defaults to 1e-4'
        },
    )
    epsilon: float = field(
        default=1e-5,
        metadata={'help': 'Epsilon for the PPO algorithm. Defaults to 1e-5'},
    )
    gae_lambda: float = field(
        default=0.95,
        metadata={
            'help':
            'Lambda for Generalized Advantage Estimation (GAE). Defaults to 0.95'
        },
    )
    norm_advantages: bool = field(
        default=True,
        metadata={
            'help':
            'Flag indicating whether to normalize the advantages. Defaults to True'
        },
    )
    value_loss_coef: float = field(
        default=0.5,
        metadata={
            'help':
            'Coefficient for the value loss in the PPO algorithm. Defaults to 0.5'
        },
    )
    entropy_coef: float = field(
        default=0.01,
        metadata={
            'help':
            'Coefficient for the entropy term in the PPO algorithm. Defaults to 0.01'
        },
    )
    clip_vloss: bool = field(
        default=True,
        metadata={
            'help':
            'Flag indicating whether to clip the value loss. Defaults to False'
        },
    )
    clip_param: float = field(
        default=0.2,
        metadata={
            'help': 'Clip parameter for the PPO algorithm. Defaults to 0.2'
        },
    )
    max_grad_norm: float = field(
        default=1.0,
        metadata={'help': 'Maximum gradient norm. Defaults to 1.0'},
    )
    rollout_steps: int = field(
        default=128,
        metadata={
            'help':
            'Number of steps to take before updating the target network. Defaults to 10'
        },
    )
    update_epochs: int = field(
        default=1,
        metadata={
            'help': 'Number of epochs to run for training. Defaults to 10'
        },
    )