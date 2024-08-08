from dataclasses import dataclass, field


@dataclass
class RLArguments:
    """Common settings for Reinforcement Learning algorithms."""

    # Common settings
    project: str = field(
        default='cyberattacksim',
        metadata={'help': "Name of the project. Defaults to 'rltoolkit'"},
    )
    algo_name: str = field(
        default='dqn',
        metadata={'help': "Name of the algorithm. Defaults to 'dqn'"},
    )
    seed: int = field(
        default=42,
        metadata={
            'help': 'Seed for environment randomization. Defaults to 42'
        },
    )
    # Environment settings
    env_id: str = field(
        default='default_18_node_network',
        metadata={
            'help':
            "The environment name. Defaults to 'default_18_node_network'"
        },
    )
    num_envs: int = field(
        default=10,
        metadata={
            'help':
            'Number of parallel environments to run for collecting experiences. Defaults to 10'
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
        default='work_dir',
        metadata={
            'help':
            "Directory for storing work-related files. Defaults to 'work_dirs'"
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


@dataclass
class DQNArguments(RLArguments):
    """DQN-specific settings."""

    learning_rate: float = field(
        default=1e-3,
        metadata={
            'help': 'Learning rate used by the optimizer. Defaults to 1e-4'
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
    max_grad_norm: float = field(
        default=10.0,
        metadata={'help': 'Maximum gradient norm. Defaults to 10.0'},
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
        default=4,
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
    learning_rate: float = field(
        default=1e-3,
        metadata={
            'help': 'Learning rate used by the optimizer. Defaults to 1e-4'
        },
    )
    rollout_steps: int = field(
        default=5,
        metadata={
            'help':
            'The number of steps to run for each environment per update'
        },
    )
    gae_lambda: float = field(
        default=0.95,
        metadata={
            'help':
            'Lambda for Generalized Advantage Estimation (GAE). Defaults to 0.95'
        },
    )
    ent_coef: float = field(
        default=0,
        metadata={
            'help':
            'Entropy weight for the policy gradient method. Defaults to 0.01'
        },
    )
    vf_coef: float = field(
        default=0.5,
        metadata={
            'help':
            'Coefficient for the value loss in the a2c algorithm. Defaults to 0.5'
        },
    )
    max_grad_norm: float = field(
        default=0.5,
        metadata={'help': 'Maximum gradient norm. Defaults to 1.0'},
    )
    normalize_advantage: bool = field(
        default=True,
        metadata={
            'help':
            'Flag indicating whether to normalize the advantages. Defaults to True'
        },
    )


@dataclass
class PPOArguments(RLArguments):
    """PPO-specific settings."""

    learning_rate: float = field(
        default=1e-2,
        metadata={'help': 'Learning rate for the optimizer. Defaults to 1e-4'},
    )
    rollout_steps: int = field(
        default=2048,
        metadata={
            'help':
            'The number of steps to run for each environment per update'
        },
    )
    n_epochs: int = field(
        default=10,
        metadata={'help: Number of epoch when optimizing the surrogate loss'},
    )
    gae_lambda: float = field(
        default=0.95,
        metadata={
            'help':
            'Lambda for Generalized Advantage Estimation (GAE). Defaults to 0.95'
        },
    )
    normalize_advantage: bool = field(
        default=True,
        metadata={
            'help':
            'Flag indicating whether to normalize the advantages. Defaults to True'
        },
    )
    ent_coef: float = field(
        default=0.01,
        metadata={
            'help':
            'Coefficient for the entropy term in the PPO algorithm. Defaults to 0.01'
        },
    )
    vf_coef: float = field(
        default=0.5,
        metadata={
            'help':
            'Coefficient for the value loss in the a2c algorithm. Defaults to 0.5'
        },
    )
    clip_range: float = field(
        default=0.2,
        metadata={
            'help': 'Clip parameter for the PPO algorithm. Defaults to 0.2'
        },
    )
    max_grad_norm: float = field(
        default=0.5,
        metadata={'help': 'Maximum gradient norm. Defaults to 1.0'},
    )

    update_epochs: int = field(
        default=1,
        metadata={
            'help': 'Number of epochs to run for training. Defaults to 10'
        },
    )
