from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RLArguments:
    """Common settings for Reinforcement Learning algorithms."""

    # Common settings
    project: str = field(
        default='cyberattacksim',
        metadata={'help': 'Name of the project. Defaults to cyberattacksim'},
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
    rollout_length: int = field(
        default=200, metadata={'help': 'The rollout length (time dimension)'})
    eval_episodes: int = field(
        default=5,
        metadata={'help': 'Number of episodes to evaluate. Defaults to 10'},
    )
    n_steps: bool = field(
        default=False,
        metadata={
            'help':
            'Use multi-step experience replay buffer, defaults to False'
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
    save_model: Optional[bool] = field(
        default=False,
        metadata={
            'help': 'Flag indicating whether to save the trained model.'
        },
    )
    train_log_interval: int = field(
        default=10,
        metadata={'help': 'Logging interval during training. Defaults to 10'},
    )
    test_log_interval: int = field(
        default=100,
        metadata={
            'help': 'Logging interval during evaluation. Defaults to 20'
        },
    )
    logger: str = field(
        default='tensorboard',
        metadata={
            'help': "Logger to use for recording logs. Defaults to 'wandb'"
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
class DistDQNArguments(RLArguments):
    """DQN-specific settings."""

    per: bool = field(
        default=False,
        metadata={
            'help':
            'Flag indicating whether to use Prioritized Experience Replay. Defaults to False'
        },
    )
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
    noisy_dqn: bool = field(
        default=False,
        metadata={
            'help':
            'Flag indicating whether to use Noisy DQN. Defaults to False'
        },
    )
    categorical_dqn: bool = field(
        default=False,
        metadata={
            'help':
            'Flag indicating whether to use Categorical DQN. Defaults to False'
        },
    )
    v_min: float = field(
        default=0.0,
        metadata={
            'help': 'Minimum value for the value function. Defaults to 0.0'
        },
    )
    v_max: float = field(
        default=200.0,
        metadata={
            'help': 'Maximum value for the value function. Defaults to 200.0'
        },
    )
    num_atoms: float = field(
        default=51,
        metadata={
            'help': 'Number of atoms for the value function. Defaults to 51'
        },
    )
    noisy_std: float = field(
        default=0.5,
        metadata={
            'help':
            'Standard deviation for the initial weights of the value function. Defaults to 0.1'
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
    learn_steps: int = field(
        default=1,
        metadata={
            'help':
            'Number of times to update the learner network. Defaults to 1'
        },
    )


@dataclass
class A2CArguments(RLArguments):
    """Actor-Critic specific settings."""

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
        metadata={
            'help': 'Number of epoch when optimizing the surrogate loss'
        },
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


@dataclass
class MCArguments(RLArguments):
    learning_rate: float = field(
        default=1e-3,
        metadata={
            'help': 'Learning rate used by the optimizer. Defaults to 1e-4'
        },
    )
    exploration_rate: float = field(
        default=0.4,
        metadata={'help': 'exploration_rate'},
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
class BRArguments(RLArguments):
    learning_rate: float = field(
        default=1e-3,
        metadata={
            'help': 'Learning rate used by the optimizer. Defaults to 1e-4'
        },
    )
    exploration_rate: float = field(
        default=0.4,
        metadata={'help': 'exploration_rate'},
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
class SACArguments(RLArguments):
    """SAC-specific settings."""

    learning_rate: float = field(
        default=1e-4,
        metadata={
            'help': 'Learning rate used by the optimizer. Defaults to 1e-4'
        },
    )

    initialization: float = field(default=1.0, )

    reward_scale: float = field(default=1.0, )

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
        metadata={
            'help': 'Number of epoch when optimizing the surrogate loss'
        },
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


@dataclass
class TD3Arguments(RLArguments):
    """TD3-specific settings."""

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
        metadata={
            'help': 'Number of epoch when optimizing the surrogate loss'
        },
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


@dataclass
class DQfDArguments(RLArguments):
    """DQfD-specific settings."""

    learning_rate: float = field(
        default=1e-3,
        metadata={
            'help': 'Learning rate used by the optimizer. Defaults to 1e-4'
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
        default=10000,
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
        default=5,
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
class CFRArguments(RLArguments):
    """CFR-specific settings."""

    learning_rate: float = field(
        default=5e-2,
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
        metadata={
            'help': 'Number of epoch when optimizing the surrogate loss'
        },
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
            'Coefficient for the entropy term in the CFR algorithm. Defaults to 0.01'
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
            'help': 'Clip parameter for the CFR algorithm. Defaults to 0.2'
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
