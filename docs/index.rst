Welcome to the CyberAttackSim docs!
==================================

.. toctree::
   :maxdepth: 8
   :caption: Contents:
   :hidden:

   source/getting_started
   source/create_a_network
   source/db
   source/tutorials
   source/agent_training
   source/experiments
   GameMode UML <source/game_mode_config_explained>
   CyberAttackSim CLI <source/yt_cli>
   source/yt_gui
   CyberAttackSim API <source/_autosummary/yawning_titan>
   CyberAttackSim Tests <source/_autosummary/tests>
   Contribute to CyberAttackSim <source/contributing>
   source/glossary
   source/license
   source/dependencies

.. toctree::
   :caption: Project Links:
   :hidden:

   Code <https://github.com/jianzhnie/CyberAttackSimulatorulator>
   Issues <https://github.com/jianzhnie/CyberAttackSimulator/issues>
   Pull Requests <https://github.com/jianzhnie/CyberAttackSimulator/pulls>
   Discussions <https://github.com/jianzhnie/CyberAttackSimulator/discussions>


What is CyberAttackSim?
----------------------

CyberAttackSim is a collection of abstract, graph based cyber-security simulation environments that supports the training
of intelligent agents for autonomous cyber operations based on OpenAI Gym. CyberAttackSim focuses on providing a fast
simulation to support the development of defensive autonomous agents who face off against probabilistic red agents.

CyberAttackSim contains a small number of specific, self contained OpenAI Gym environments for autonomous cyber defence
research, which are great for learning and debugging, as well as a flexible, highly configurable generic environment
which can be used to represent a range of scenarios of increasing complexity and scale. The generic environment only
needs a network topology and a settings file in order to create an OpenAI Gym compliant environment which also enables
open research and enhanced reproducibility.


How can CyberAttackSim be used?
------------------------------

CyberAttackSim can be used either through the CLI app or vie the GUI. The idea of this is to make CyberAttackSim as
accessible as possible to all users out of the box whilst not compromising the ability for users to make in-depth
modifications to the source code.


Design Principles
-----------------

CyberAttackSim has been designed with the following key principles in mind:
 - Simplicity over complexity
 - Minimal Hardware Requirements
 - Operating System agnostic
 - Support for a wide range of algorithms
 - Enhanced agent/policy evaluation support
 - Flexible environment and game rule configuration


What is CyberAttackSim built with
--------------------------------
CyberAttackSim is built on the shoulders of giants and heavily relies on the following libraries:

 * `OpenAI's Gym <https://gym.openai.com/>`_ is used as the basis for all of the environments
 * `Networkx <https://github.com/networkx/networkx>`_ is used as the underlying data structure used for all environments
 * `Stable Baselines 3 <https://github.com/DLR-RM/stable-baselines3>`_ is used as a source of RL algorithms
 * `Rllib (part of Ray) <https://github.com/ray-project/ray>`_ is used as another source of RL algorithms
 * `Typer <https://github.com/tiangolo/typer>`_ is used to provide a command-line interface
 * `Django <https://github.com/django/django/>`_ is used to provide the management and elements of the GUI
 * `Cytoscape JS <https://github.com/cytoscape/cytoscape.js/>`_ is used to provide a lightweight and intuitive network editor


CyberAttackSim Quick start
-------------------------

.. code:: bash

    pip install <CyberAttackSim.whl file>
    CyberAttackSim setup
    CyberAttackSim gui


Where next?
------------

The best place to start is diving into the :ref:`getting-started`, or just straight into the :ref:`cas-gui`.
