# SAC-Discrete-Pytorch

This is a **clean and robust Pytorch implementation of Soft-Actor-Critic** on **discrete** action space

## Dependencies

```python
gymnasium==0.29.1
numpy==1.26.1
pytorch==2.2.0

python==3.10.14
```

## How to use Discrete SAC

### Train from scratch

```bash
python run_SACD_18_nodes_env.py
```

where the default enviroment is 'YAWNING-TITAN' with 18 nodes,i.e.default_18_node_network.

### Play with trained model

```bash
python main.py --EnvIdex default_18_node_network --Loadmodel True --ModelIdex 50
```

- Visualization:

```bash
tensorboard --logdir runs
```

### Hyperparameter Setting

For more details of Hyperparameter Setting, please check 'main.py'

### References

Christodoulou P. Soft actor-critic for discrete action settings\[J\]. arXiv preprint arXiv:1910.07207, 2019.

Haarnoja T, Zhou A, Abbeel P, et al. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor\[C\]//International conference on machine learning. PMLR, 2018: 1861-1870.

Haarnoja T, Zhou A, Hartikainen K, et al. Soft actor-critic algorithms and applications\[J\]. arXiv preprint arXiv:1812.05905, 2018.

- [Yawning Titan](https://github.com/dstl/YAWNING-TITAN)

- [SAC-Discrete-Pytorch](https://github.com/XinJingHao/SAC-Discrete-Pytorch)
