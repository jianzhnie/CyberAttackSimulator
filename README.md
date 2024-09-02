# CyberAttackSimulator

## Table of Content

- [CyberAttackSimulator](#cyberattacksimulator)
  - [Table of Content](#table-of-content)
  - [About CyberAttackSimulator](#about-cyberattacksimulator)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [CyberAttackSimulator GUI](#cyberattacksimulator-gui)
    - [CyberAttackSimulator GUI 是如何构建的](#cyberattacksimulator-gui-是如何构建的)
    - [启动 GUI](#启动-gui)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  - [Citation](#citation)

## About CyberAttackSimulator

CyberAttackSimulator 是一组抽象的、高度灵活的基于图形的强化学习 (RL) 网络安全模拟环境, 用于在模拟网络上训练和评估自主网络防御模型, 提供了标准的基于 OpenAI Gym 强化学习环境接口。它在构建时考虑到了模块化，以便用户可以根据自己的需求在其基础上进行构建。它支持各种强大的配置文件来构建网络、服务、主机类型、防御代理等。

**动机**

- 可在高度可定制的配置中防御任意网络拓扑结构。
- 可扩展性——允许修改和添加各种防御行动和进攻策略，而无需对代码库进行结构性更改。
- 可扩展性——以最小的性能成本支持大型网络的训练

**设计原则**

CyberAttackSimulator 的设计遵循了以下关键原则：

- 简单胜过复杂
- 最低硬件要求
- 操作系统无关
- 支持多种算法
- 增强智能体/策略评估
- 支持灵活的环境和游戏规则配置

## Getting Started

为了安装 CyberAttackSimulator，您需要安装以下软件：

- python3.10
- python3-pip
- nvirtualenv

CyberAttackSimulator 的设计与操作系统无关，因此应该适用于 Linux、Windows 和 MacOS 的大多数版本/发行版。该项目在 Python 3.10 上运行并已通过测试。

1. 创建并激活虚拟环境

```shell
conda create -n cybersim python=3.10 && conda activate cybersim
```

2. 克隆源代码

使用 HTTPS 克隆 CyberAttackSimulator 仓库

```shell
git clone https://github.com/jianzhnie/CyberAttackSimulator.git
```

3. 安装所有依赖项：

```shell
cd CyberAttackSimulator
pip install -r requirements.txt
```

## Usage

要运行任何 CyberAttackSimulator 脚本，请进入 `cybersim` 虚拟环境. 所有运行的例子都在 `examples` 文件夹下。

1. `随机节点数量网络` 环境创建，模型训练, 这里，你可以尝试不同的网络结构和修改网络节点数量。

```python
python examples/cyberattacksim/run_random_nodes_env.py
```

2. `随机连接网络` 环境创建，模型训练

```python
python cyber/CyberAttackSimulator/examples/cyberattacksim/run_random_connected_graph_env.py
```

3. 运行一个 18 节点网络自动攻防（DQN， A2C， PPO）

```python
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name dqn --env_id default_18_node_network
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name a2c --env_id default_18_node_network
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name ppo --env_id default_18_node_network
```

## CyberAttackSimulator GUI

### CyberAttackSimulator GUI 是如何构建的

CyberAttackSimulator GUI 是作为底层 CyberAttackSimulator 库的可选扩展而设计的。CyberAttackSimulator GUI 主要使用Django将 CyberAttackSimulator 的各个方面转换为 html 对象，用户可以在本地浏览器实例中与这些对象进行交互，从而允许执行底层 Python，而无需命令行界面或 Python 语言知识。

CyberAttackSimulator GUI 还集成了定制版Cytoscape JS ，该版本已扩展为可直接与 CyberAttackSimulator 配合使用。这允许用户直接与网络拓扑交互并编辑网络节点的位置和属性，从而主动更新存储网络的数据库。

### 启动 GUI

如果您是一位对 CyberAttackSimulator 进行更改的开发人员，则可以从克隆的 repo 运行 GUI 来测试您的更改：

```python
python3 -m manage.py runserver
```

## License

`CyberAttackSimulator` is released under the Apache 2.0 license.

## Acknowledgements

We appreciate the work by many open-source contributors, especially:

- [Yawning Titan](https://github.com/dstl/YAWNING-TITAN)
- [CyberBattleSim](https://github.com/microsoft/CyberBattleSim)
- [CybORG](https://github.com/cage-challenge/CybORG)
- [NetworkAttackSimulator](https://github.com/Jjschwartz/NetworkAttackSimulator)

## Citation

Please cite the repo if you use the data or code in this repo.

```bibtex
@misc{CyberAttackSimulator,
  author = {jianzhnie},
  title = {Auto Cybersecurity Simulator: A reinforcement learning simulation environment focused on autonomous cyber defence.},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/jianzhnie/CyberAttackSimulator}},
}
```
