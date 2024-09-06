# GAIL_and_AIRL

## method paper
[1]GAIL:  Ho, Jonathan, and Stefano Ermon. "Generative adversarial imitation learning." Advances in neural information processing systems. 2016.

[2]AIRL:  Fu, Justin, Katie Luo, and Sergey Levine. "Learning robust rewards with adversarial inverse reinforcement learning." arXiv preprint arXiv:1710.11248 (2017).


## steps
0.change path:
In save_expert_traj.py line 10, and train_imitation_discrete.py line 14, change abs path of PACKAGE_PATH.

1. train expert ppo
```
python train_expert_discrete.py
```

2. collect expert trajectory
```
python save_expert_traj.py
```

3. train imitation RL
```
python train_imitation_discrete.py --algo gail
```
or
```
python train_imitation_discrete.py --algo airl
```
