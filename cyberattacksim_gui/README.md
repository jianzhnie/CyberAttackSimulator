# How is the CyberAttackSim GUI built

The CyberAttackSim GUI is designed as an optional extension to the underlying CyberAttackSim library. The Yawning Titan GUI primarily uses Django to convert aspects of CyberAttackSim into html objects that can be interacted with in a local browser instance by the user thereby allowing the underlying Python to be executed without need for a command line interface or knowledge of the python language.

The CyberAttackSim GUI also integrates with a customised version Cytoscape JS which has been extended to work directly with CyberAttackSim. This allows for users to directly interface with network topologies and edit the position and attributes of network nodes that actively updates a database of stored networks.

## Run the django server:

If you’re a developer making changes to CyberAttackSim, you can run the GUI from the cloned repo to test your changes:

- navigate to repository root
- run `python ./manage.py runserver`

## Run the django server in a minified chrome window:

- navigate to repository root
- run `python ./manage.py`
