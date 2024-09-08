**我的修改：**

1.`cyberattacksim\envs\generic\core\blue_action_set.py`  line188

```python
# Get the nodes that are connected via the input edge
# nodes = self.network_interface.edge_map[edge] # source version
nodes = self.network_interface.edge_map[int(edge)] # changed by ltl
```

2.`cyberattacksim\envs\generic\core\blue interface.py`  line134

```python
# blue_action, blue_node = self.global_action_dict[action]()   # source version
blue_action, blue_node = self.global_action_dict[int(action)]()  # changed by ltl
```

3. `examples/configs/rl_args.py`  
4. `examples/cyberattacksim/run_default_18_nodes_env.py`

**算法运行（SAC， TD3， DQfD， CFR）**

```python
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name sac --env_id default_18_node_network
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name td3 --env_id default_18_node_network
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name dqfd --env_id default_18_node_network
python examples/cyberattacksim/run_default_18_nodes_env.py --algo_name cfr --env_id default_18_node_network
```

