from django import forms as django_forms
from django.forms import widgets


class MassiveNetworkForm(django_forms.Form):
    """Django form to represent options required by the :class:

    `~cyberattacksim.cyberattacksim_run.CyberAttackRun`.
    """

    massive_node_size = django_forms.ChoiceField(
        choices=[
            (10, '10-nodes'),
            (50, '50-nodes'),
            (200, '200-nodes'),
            (1000, '1000-nodes'),
            (5000, '5000-nodes'),
            (10000, '10000-nodes'),
            (100000, '100000-nodes'),
            (150000, '150000-nodes'),
        ],
        required=True,
        label='Massive node size',
        initial=1000,  # 默认选中值
        help_text=
        'The node size used for build the massive node env, Defalut set to 1000',
    )
    algorithm = django_forms.ChoiceField(
        choices=[
            ('dqn', 'DQN'),
            ('rainbow', 'Rainbow'),
            ('her', 'HER'),
            ('a2c', 'A2C'),
            ('ppo', 'PPO'),
            ('sac', 'SAC'),
            ('td3', 'TD3'),
            ('gail', 'GAIL'),
            ('airl', 'AIRL'),
            ('mc', 'MC'),
            ('cfr', 'CFR'),
        ],
        required=True,
        label='Algorithm',
        initial='ppo',  # 默认选中值
        help_text=
        'The algorithm use for training the agent, Defalut set to PPO',
    )
    deterministic = django_forms.BooleanField(
        widget=widgets.CheckboxInput(attrs={
            'role': 'switch',
            'class': 'inline form-check-input'
        }),
        required=False,
        label='Deterministic',
        initial=False,
        help_text=
        'Whether the evaluation should use stochastic or deterministic actions',
    )
    save = django_forms.BooleanField(
        widget=widgets.CheckboxInput(attrs={
            'role': 'switch',
            'class': 'inline form-check-input'
        }),
        required=False,
        label='Save trained agent',
        help_text=
        'Saves the trained agent using the stable_baselines3 save as zip functionality.',
    )
    export = django_forms.BooleanField(
        widget=widgets.CheckboxInput(attrs={
            'role': 'switch',
            'class': 'inline form-check-input'
        }),
        required=False,
        label='Export run',
        help_text='Export the CyberAttackRun as a zip.',
    )
    total_timesteps = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={'class': 'inline form-control'}),
        required=False,
        help_text='The number of samples (env steps) to train on',
        label='Total timesteps',
        initial=2000,
    )
    training_runs = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={'class': 'inline form-control'}),
        required=False,
        help_text='The number of times the agent is trained',
        label='Training episodes',
        initial=1,
    )
    n_eval_episodes = django_forms.IntegerField(
        widget=widgets.NumberInput(attrs={'class': 'inline form-control'}),
        required=False,
        help_text='The number of episodes to evaluate the agent',
        label='Evaluation episodes',
        initial=1,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @property
    def training_fields(self):
        """The fields of the form related to agent training."""
        return [
            f for f in self if f.id_for_label.replace('id_', '') in [
                'massive_node_size',
                'algorithm',
                'deterministic',
                'save',
                'export',
                'total_timesteps',
                'training_runs',
                'n_eval_episodes',
            ]
        ]
