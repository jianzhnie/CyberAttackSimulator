# CyberAttackSimulator

## About CyberAttackSimulator

CyberAttackSimulator 是一个强化学习 (RL) 模拟环境，用于在模拟网络上训练和评估自主网络防御模型。它在构建时考虑到了模块化，以便用户可以根据自己的需求在其基础上进行构建。它支持各种强大的配置文件来构建网络、服务、主机类型、防御代理等。

动机：

- 可扩展性——允许修改和添加各种防御行动和进攻策略，而无需对代码库进行结构性更改。
- 可扩展性——以最小的性能成本支持大型网络的训练

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

### 1. `随机节点数量网络` 环境创建，模型训练, 这里，你可以尝试不同的网络结构和修改网络节点数量。

```python
python examples/cyberattacksim/run_random_nodes_env.py
```

### 2. `随机连接网络` 环境创建，模型训练

```python
cyber/CyberAttackSimulator/examples/cyberattacksim/run_random_connected_graph_env.py
```

### 3. 运行一个 18 节点网络自动攻防（DQN， A2C， PPO）

```python
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name dqn --env_id default_18_node_network
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name a2c --env_id default_18_node_network
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name ppo --env_id default_18_node_network
```
