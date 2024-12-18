from __future__ import annotations

import json
import os
import os.path
import pathlib
import shutil
import sys
from copy import deepcopy
from datetime import datetime
from logging import Logger, getLogger
from pathlib import Path
from typing import Final, List, Optional, Union
from uuid import uuid4
import pdb
import gymnasium as gym
import torch
from stable_baselines3 import A2C, DQN, PPO, HerReplayBuffer
from stable_baselines3.a2c import MlpPolicy as A2CMlp
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.dqn import MlpPolicy as DQNMlp
from stable_baselines3.ppo import MlpPolicy as PPOMlp
import logging

sys.path.append(os.getcwd())
from cyberattacksim import AGENTS_DIR
from cyberattacksim.utils.utils import get_system_info
from cyberwheel.cyberwheel_envs.cyberwheel_dynamic import DynamicCyberwheel
from cyberwheel.network.network_base import Network
from cyberwheel.red_agents import ARTAgent
from cyberwheel.red_agents.strategies import DFSImpact, ServerDowntime


# 配置 logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
_LOGGER = logging.getLogger(__name__)


def create_cyberwheel_env(
    network_config: str = "15-host-network.yaml",
    decoy_config: str = "decoy_hosts.yaml",
    host_config: str = "host_definitions.yaml",
    detector_config: str = "example_detector_handler.yaml",
    min_decoys: int = 0,
    max_decoys: int = 1,
    reward_scaling: float = 10.0,
    reward_function: str = "default",
    red_agent: str = "art_agent",
    blue_config: str = "dynamic_blue_agent.yaml",
    num_steps: int = 100,
    red_strategy: str = "server_downtime",
    logger: str = _LOGGER,
) -> DynamicCyberwheel:
    """Creates a DynamicCyberwheel environment."""

    # Load network from yaml here
    network_config = Path("cyberwheel/resources/configs/network").joinpath(
        network_config
    )
    logger.info(f"Building network: {network_config} ...")
    network = Network.create_network_from_yaml(
        network_config=network_config, logger=logger
    )

    logger.info("Mapping attack validity to hosts...")
    service_mapping = {}
    if red_agent == "art_agent":
        service_mapping = ARTAgent.get_service_map(network)

    if red_strategy == "dfs_impact":
        red_strategy = DFSImpact
    else:
        red_strategy = ServerDowntime

    env: gym.Env = DynamicCyberwheel(
        network_config=network_config,
        decoy_host_file=decoy_config,
        host_def_file=host_config,
        detector_config=detector_config,
        min_decoys=min_decoys,
        max_decoys=max_decoys,
        blue_reward_scaling=reward_scaling,
        reward_function=reward_function,
        red_agent=red_agent,
        blue_config=blue_config,
        num_steps=num_steps,
        network=deepcopy(network),
        service_mapping=service_mapping,
        red_strategy=red_strategy,
    )

    return env


def create_massive_node_env(
    network_size: int = 10,
    logger: str = _LOGGER,
):
    """Creates a DynamicCyberwheel environment with a massive network."""
    if network_size == 10:
        network_config = "10-host-network.yaml"
    elif network_size == 50:
        network_config = "50-host-network.yaml"
    elif network_size == 200:
        network_config = "200-host-network.yaml"

    elif network_size == 1000:
        network_config = "1000-host-network.yaml"
    elif network_size == 5000:
        network_config = "5000-host-network.yaml"
    elif network_size == 10000:
        network_config = "10000-host-network.yaml"

    elif network_size == 100000:
        network_config = "100000-host-network.yaml"
    elif network_size == 150000:
        network_config = "150000-host-network.yaml"
    else:
        raise ValueError("Invalid network size")

    env = create_cyberwheel_env(network_config=network_config, logger=logger)

    return env


class CyberWheelAttackRun:
    """The ``CyberAttackRun`` class is the run class for training YT agents
    from a given set of parameters.

    The ``CyberAttackRun`` class can be used 'straight out of the box', as all params have default values.

    .. code:: python

        cas_runner = CyberAttackRun()

    The ``CyberAttackn`` class can also be used manually by setting auto=False.

    .. code:: python

        cas_runner = CyberAttackRun(auto=False)
        cas_runner.setup()
        cas_runner.train()
        cas_runner.evaluate()

    Trained agents can be saved by calling ``.save()``. If no path is provided, a path is generated using the
    AGENTS_DIR, today's date, and the uuid of the instance of ``CyberAttackRun``.

    .. code:: python

        cas_runner = CyberAttackRun()
        cas_runner.save()

    .. todo::

        - Build a reporting functionality that captures all logs and eval and generates a PDF report.
        - Add multiple training runs functionality for the same agent.
        - Add the ability to load a saved agent and continue training it.
    """

    def __init__(
        self,
        massive_node_size: int = None,
        algorithm: str = "ppo",
        print_metrics: bool = False,
        show_metrics_every: int = 1,
        eval_freq: int = 10000,
        total_timesteps: int = 200000,
        training_runs: int = 1,
        n_eval_episodes: int = 1,
        deterministic: bool = False,
        warn: bool = True,
        verbose: int = 1,
        logger: Optional[Logger] = None,
        output_dir: Optional[str] = None,
        auto: bool = True,
        device: Union[torch.device, str] = "cuda",
        **kwargs,
    ):
        """The CyberAttackRun constructor.

        # TODO: Add proper Sphinx mapping for classes/methods.

        :param network: An instance of ``Network``.
        :param game_mode: An instance of ``GameMode``.
        :param red_agent_class: The agent/action set class used for the red agent.
        :param blue_agent_class: The agent/action set class used for the blue agent.
        :param print_metrics: Print the metrics if True. Default value = True.
        :param show_metrics_every: Prints the metrics every ``show_metrics_every`` time steps. Default value = 10.
        :param collect_additional_per_ts_data: Collects additional per-timestep data if True.Default value = False.
        :param eval_freq: Evaluate the agent every ``eval_freq`` call of the callback. Default value = 10,000.
        :param total_timesteps: The number of samples (env steps) to train on. Default value = 200000.
        :param training_runs: The number of times the agent is trained.
        :param n_eval_episodes: The number of episodes to evaluate the agent. Default value = 1.
        :param deterministic: Whether the evaluation should use stochastic or deterministic actions. Default value =
            False.
        :param warn: Output additional warnings mainly related to the interaction with stable_baselines if True.
            Default value = True.
        :param render: Renders the environment during evaluation if True. Default value = False.
        :param verbose: Verbosity level: 0 for no output, 1 for info messages (such as device or wrappers used),
            2 for debug messages. Default value = 1.
        :param logger: An optional custom logger to override the use of the default module logger.
        :param output_dir: An optional output path for eval output and saved agent zip file. If none is provided,
            a path is generated using the ``cyberattacksim.AGENTS_DIR``, today's date, and the uuid of the instance
            of ``CyberAttackun``.
        :param auto: If True, ``setup()``, ``train()``, and ``evaluate()`` are called automatically.
        """
        # Give the run an uuid
        self.uuid: Final[str] = str(uuid4())

        # Initialise required instance variables as None

        self.agent: Optional[PPO] = None
        self.eval_callback: Optional[EvalCallback] = None

        self.massive_node_size = massive_node_size
        self.algorithm = algorithm
        self.print_metrics = print_metrics
        self.show_metrics_every = show_metrics_every
        self.eval_freq = eval_freq
        self.total_timesteps = total_timesteps
        self.training_runs = training_runs
        self.n_eval_episodes = n_eval_episodes
        self.deterministic = deterministic
        self.warn = warn
        self.verbose = verbose
        self.auto = auto
        self.device = device

        self.logger = _LOGGER if logger is None else logger
        self.sys_info = get_system_info(logger=self.logger)
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Run initialised")
        self.logger.info(f"CyberAttackSim Run with {self.massive_node_size} nodes")

        self.output_dir = output_dir

        # Automatically setup, train, and evaluate the agent if auto is True.
        if self.auto:
            self.setup()
            self.train()
            self.evaluate()
            self.save()

    def _args_dict(self):
        return {
            "uuid": self.uuid,
            "print_metrics": self.print_metrics,
            "show_metrics_every": self.show_metrics_every,
            "eval_freq": self.eval_freq,
            "total_timesteps": self.total_timesteps,
            "training_runs": self.training_runs,
            "n_eval_episodes": self.n_eval_episodes,
            "deterministic": self.deterministic,
            "warn": self.warn,
            "verbose": self.verbose,
            "auto": self.auto,
        }

    def _get_new_ppo(self) -> PPO:
        """Get a new instance of ``stable_baselines.ppo.ppo.PPO``."""
        self.logger.info(f"New instance of {self.algorithm} agent.")
        if self.algorithm == "dqn":
            agent = DQN(
                DQNMlp,
                self.env,
                verbose=self.verbose,
                device=self.device,
            )

        if self.algorithm == "her":
            agent = DQN(
                A2CMlp,
                self.env,
                verbose=self.verbose,
                replay_buffer_class=HerReplayBuffer,
                device=self.device,
            )
        if self.algorithm == "a2c":
            agent = A2C(
                A2CMlp,
                self.env,
                verbose=self.verbose,
                device=self.device,
            )
        if self.algorithm == "ppo":
            agent = PPO(
                PPOMlp,
                self.env,
                verbose=self.verbose,
                device=self.device,
            )
        else:
            agent = PPO(
                PPOMlp,
                self.env,
                verbose=self.verbose,
                device=self.device,
            )
        return agent

    def setup(self, new: bool = True, agent_zip_path: Optional[str] = None):
        """Performs a setup of the ``NetworkInterface``, ``GenericNetworkEnv``,
        ``PPO`` algorithm.

        The setup needs to be performed before training can occur.

        :param new: If True, a new instance of PPO is generated. If False, a agent_zip_path must be passed tooo.
        :param agent_zip_path: Optional path to a saved ppo.zip file. Required if new = False.

        :raise AttributeError: When new=False and agent_zip_path hasn't been provided.
        """
        if not new and not agent_zip_path:
            msg = f"Performing setup when new=False requires agent_zip_path as the path of a saved {agent_zip_path} file."
            try:
                raise AttributeError(msg)
            except AttributeError as e:
                _LOGGER.critical(e)
                raise e

        if self.output_dir:
            if isinstance(self.output_dir, str):
                self.output_dir = pathlib.Path(self.output_dir)
        else:
            self.output_dir = pathlib.Path(
                os.path.join(
                    AGENTS_DIR, "trained", str(datetime.now().date()), f"{self.uuid}"
                )
            )
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.env = create_massive_node_env(
            network_size=int(self.massive_node_size), logger=self.logger
        )

        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Env created")

        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Performing env check")
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Env checking complete")

        self.env.reset()
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Env reset")
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Instantiating agent")
        self.agent = self._get_new_ppo()
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Agent instantiated")

        self.eval_callback = EvalCallback(
            Monitor(self.env, str(self.output_dir)),
            n_eval_episodes=self.n_eval_episodes,
            eval_freq=self.eval_freq,
            deterministic=self.deterministic,
            verbose=self.verbose,
        )
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Eval callback set")

    def train(self) -> Union[PPO, None]:
        """Trains the agent.

        :return: The trained instance of ``stable_baselines3.ppo.ppo.PPO``.
        """
        if self.env and self.agent and self.eval_callback:
            self.logger.info(
                f"CyberAttackSim Run  {self.uuid}: Performing agent training"
            )
            for i in range(self.training_runs):
                self.agent.learn(
                    total_timesteps=self.total_timesteps,
                    callback=self.eval_callback,
                )
                self.logger.info(
                    f"CyberAttackSim Run  {self.uuid}: Training run {i + 1} complete"
                )

                self.env.reset()
                self.logger.info(
                    f"CyberAttackSim Run  {self.uuid}: GenericNetworkEnv reset"
                )

            self.logger.info(
                f"CyberAttackSim Run  {self.uuid}: Agent training complete"
            )
            return self.agent
        else:
            self.logger.error(
                f"Cannot train the agent for CyberAttackSim Run  {self.uuid} as the run has not been setup. "
                f"Call .setup() on the instance of {self.__class__.__name__} to setup the run."
            )

    def evaluate(self) -> Union[tuple[float, float], tuple[List[float], List[int]]]:
        """Evaluates the trained agent.

        :return: Mean reward per episode, std of reward per episode.
        """
        if self.agent:
            return evaluate_policy(
                self.agent, self.env, n_eval_episodes=self.n_eval_episodes
            )
        else:
            self.logger.error(
                f"Cannot evaluate CyberAttackSim Run  {self.uuid} as the agent has not been trained. "
                f"Call .train() on the instance of {self.__class__.__name__} to train the agent."
            )

    def save(self) -> Union[str, None]:
        """Saves the trained agent using the stable_baselines3 save as zip
        functionality.

        The instance of PPO is saved to ppo.zip.

        The CyberAttackRun args are saved to args.json.

        The CyberAttackun.uuid is saved to UUID.


        :return: The path the agent has been saved to.
        """
        if self.agent:
            # Save the agent
            agent_path = os.path.join(self.output_dir, self.algorithm + ".zip")
            self.agent.save(path=agent_path)

            # Dump the args down to yaml file
            args_path = os.path.join(self.output_dir, "args.json")
            with open(args_path, "w") as file:
                json.dump(self._args_dict(), file, indent=4)

            # Write the UUID file
            uuid_path = os.path.join(self.output_dir, "UUID")
            with open(uuid_path, "w") as file:
                file.write(self.uuid)

            self.logger.info(
                f"CyberAttackSim Run  {self.uuid}: Saved trained agent (Stable Baselines3 PPO) to: {agent_path}"
            )
            return str(agent_path)
        else:
            self.logger.error(
                f"Cannot save the trained agent from CyberAttackSim Run  {self.uuid} as the agent has not been "
                f"trained. Call .train() on the instance of {self.__class__.__name__} to train the agent."
            )

    def _build_inventory_file(self):
        # Walk the output_dir to build an inventory file
        inventory_path = os.path.join(self.output_dir, "INVENTORY")
        if os.path.isfile(inventory_path):
            os.remove(inventory_path)
        self.logger.info(
            f"CyberAttackSim Run  {self.uuid}: Building INVENTORY file {inventory_path}."
        )

        with open(inventory_path, "w") as inventory:
            inventory.write("file, ST_SIZE")
            inventory.write("\n")
            for root, dirs, files in os.walk(self.output_dir):
                for file in files:
                    if file != "INVENTORY":
                        file_path = os.path.join(root, file)
                        dir_path = file_path.replace(str(self.output_dir), "")[1:]
                        file_stat = os.stat(file_path)
                        inventory.write(f"{dir_path}, {file_stat.st_size}")
                        inventory.write("\n")
                        self.logger.info(
                            f"CyberAttackSim Run  {self.uuid}: File added to inventory: {dir_path}."
                        )
        self.logger.info(
            f"CyberAttackSim Run  {self.uuid}: Finished building INVENTORY file."
        )

    def export(self) -> str:
        """Export the CyberAttack zip.

        The contents of output_dir is archived to the agents_dir exported dir.

        Included is an INVENTORY file that contains all files and their sizes. This is used for file verification when
        an exported CyberAttackn is imported.

        :return: The exported filepath as a str.
        """
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Performing export.")
        self.save()

        self._build_inventory_file()

        # Make a zip archive of the output dir
        exported_root = pathlib.Path(os.path.join(AGENTS_DIR, "exported"))
        exported_root.mkdir(parents=True, exist_ok=True)
        export_path = os.path.join(exported_root, f"EXPORTED_cas_runner_{self.uuid}")
        self.logger.info(
            f"CyberAttackSim Run  {self.uuid}: Making a zip archive of {self.output_dir} and writing to {export_path}.zip."
        )
        shutil.make_archive(export_path, "zip", self.output_dir)
        self.logger.info(f"CyberAttackSim Run  {self.uuid}: Export completed.")
        return f"{export_path}.zip"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"uuid='{self.uuid}', "
            f"algorithm ={self.algorithm}, "
            f"print_metrics={self.print_metrics}, "
            f"show_metrics_every={self.show_metrics_every}, "
            f"eval_freq={self.eval_freq}, "
            f"total_timesteps={self.total_timesteps}, "
            f"training_runs={self.training_runs}, "
            f"n_eval_episodes={self.n_eval_episodes}, "
            f"deterministic={self.deterministic}, "
            f"warn={self.warn}, "
            f"verbose={self.verbose}"
            ")"
        )
