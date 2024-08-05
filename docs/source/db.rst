CyberAttackSim DB
================

CyberAttackSim comes packages with a lightweight document database (See: `TinyDB <https://tinydb.readthedocs.io/en/latest/>`_).


The CyberAttackDB class
************************

A base class, :class:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB`, exists that
provides extended TinyDB functions :func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.__init__`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.insert`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.update`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.upsert`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.all`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.get`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.search`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.count`,
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.remove`, and
:func:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.close`, methods. All methods provided have either direct
calls to their their :class:`~tinydb.database.TinyDB` counterpart, or some custom CyberAttackSim login before the call. Methods have been defined as
abstract methods to force sub-classes of :class:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB` to
implement them. If functionality does not change, the implementations of the abstract methods can simple
call ``super()`` to trigger the default logic.

When :func:`CyberAttackDB.__init__ <cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB.__init__>` is called,
the ``name`` passed to it is used to generate a filepath using :attr:`cyberattacksim.DB_DIR`. For example, calling
``CyberAttackDB("demo")`` would generate a :class:`~tinydb.database.TinyDB` db `.json` file at:

- **Linux** - `~/.local/share/cyberattacksim/db/demo.json`
- **Windows** - `~/AppData/cyberattacksim/cyberattacksim/db/demo.json`
- **MacOs** - `~/Library/Application Support/cyberattacksim/db/demo.json`

The CyberAttackQuery class
***************************

The :class:`~cyberattacksim.db.query.CyberAttackQuery` extends :class:`tinydb.queries.Query` by implementing
:func:`~cyberattacksim.db.query.CyberAttackQuery.len_eq`, :func:`~cyberattacksim.db.query.CyberAttackQuery.len_gt`,
:func:`~cyberattacksim.db.query.CyberAttackQuery.len_ge`, :func:`~cyberattacksim.db.query.CyberAttackQuery.len_lt`,
and :func:`~cyberattacksim.db.query.CyberAttackQuery.len_le` functions to test the length of a field.

The EntryNodeCompatibilityQuery class
***************************

The :class:`~cyberattacksim.db.compatibility_query.EntryNodeCompatibilityQuery` extends :class:`tinydb.queries.Query` by implementing
:func:`~cyberattacksim.db.compatibility_query.EntryNodeCompatibilityQuery.works_with`. This function allows for the game mode to
be checked against a provided :class:`~cyberattacksim.networks.network.Network` or an integer number of entry nodes. Game modes where the number of entry nodes is unrestricted
or the provided value falls within the restricted range will be returned.

The HighValueNodeCompatibilityQuery class
***************************

The :class:`~cyberattacksim.db.compatibility_query.HighValueNodeCompatibilityQuery` extends :class:`tinydb.queries.Query` by implementing
:func:`~cyberattacksim.db.compatibility_query.HighValueNodeCompatibilityQuery.works_with`. This function allows for the game mode to
be checked against a provided :class:`~cyberattacksim.networks.network.Network` or an integer number of high value nodes. Game modes where the number of high value nodes is unrestricted
or the provided value falls within the restricted range will be returned.

The NetworkNodeCompatibilityQuery class
***************************

The :class:`~cyberattacksim.db.compatibility_query.NetworkNodeCompatibilityQuery` extends :class:`tinydb.queries.Query` by implementing
:func:`~cyberattacksim.db.compatibility_query.NetworkNodeCompatibilityQuery.works_with`. This function allows for the game mode to
be checked against a provided :class:`~cyberattacksim.networks.network.Network` or an integer number of total network nodes. Game modes where the number of total network nodes is unrestricted
or the provided value falls within the restricted range will be returned.

The NetworkCompatibilityQuery class
***************************

The :class:`~cyberattacksim.db.compatibility_query.NetworkCompatibilityQuery` extends :class:`tinydb.queries.Query` by implementing
:func:`~cyberattacksim.db.compatibility_query.NetworkCompatibilityQuery.compatible_with`. This function allows for the game mode to
be checked against a provided network. This query will check all restricted network attributes are compatible with the properties of the
provided :class:`~cyberattacksim.networks.network.Network`.

.. _network-networks-network_db-schema-classes:

The NetworkDB and NetworkSchema classes
***************************************

The :class:`~cyberattacksim.networks.network_db.NetworkDB` class, used for inserting, querying, updating, and deleting
instances of :class:`~cyberattacksim.networks.network.Network`, relies upon
:class:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB` at
:attr:`NetworkDB._db<cyberattacksim.networks.network_db.NetworkDB._db>`. It wraps the
:class:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB` functions,
:func:`~cyberattacksim.networks.network.NetworkDB.insert`,
:func:`~cyberattacksim.networks.network.NetworkDB.update`,
:func:`~cyberattacksim.networks.network.NetworkDB.upsert`,
:func:`~cyberattacksim.networks.network.NetworkDB.all`,
:func:`~cyberattacksim.networks.network.NetworkDB.get`,
:func:`~cyberattacksim.networks.network.NetworkDB.search`,
:func:`~cyberattacksim.networks.network.NetworkDB.count`,
:func:`~cyberattacksim.networks.network.NetworkDB.remove`, with the return types overridden to return
:class:`~cyberattacksim.networks.network.Network`.
The :class:`~cyberattacksim.db.network.NetworkDB` class writes to a `network.json` file at:

- **Linux** - `~/.local/share/cyberattacksim/db/network.json`
- **Windows** - `~/AppData/cyberattacksim/cyberattacksim/db/network.json`
- **MacOs** - `~/Library/Application Support/cyberattacksim/db/network.json`


First, we must instantiate the :class:`~cyberattacksim.db.network.NetworkDB` with:

.. code:: python

    from cyberattacksim.networks.network_db import NetworkDB
    db = NetworkDB()

Next, we have the option to query the db with either the standard :class:`tinydb.queries.Query` class, the extended
:class:`~cyberattacksim.db.query.CyberAttackQuery` class, or by using the network config specific
:class:`~cyberattacksim.networks.network.NetworkSchema` class. Here we will use :class:`~cyberattacksim.networks.network_db.NetworkSchema`.
The :class:`~cyberattacksim.networks.network_db.NetworkSchema` class has an attribute mapped to each attribute of
:class:`~cyberattacksim.networks.network.Network` as an instance of :class:`~cyberattacksim.db.query.CyberAttackQuery`.
This gives direct access to the specific field within the :class:`~tinydb.database.TinyDB` db file.

The following code blocks demonstrate how to use combinations of the :class:`~cyberattacksim.networks.network_db.NetworkSchema`
class to build a :class:`~tinydb.queries.Query` chain to query the :class:`~cyberattacksim.networks.network_db.NetworkDB`.

**Search for all network configs that have "1" as an entry node:**

.. code:: python

    results = db.search(NetworkSchema.ENTRY_NODES.all(["1"]))

**Search for all network configs that have "1" as both an entry node and a high value node:**

.. code:: python

    results = db.search(
        NetworkSchema.ENTRY_NODES.all(["1"]))
        and (NetworkSchema.HIGH_VALUE_NODES.all(["1"])
    )

**Search for all network configs that have at least 3 high value nodes**

.. code:: python

    results = db.search(NetworkSchema.ENTRY_NODES.len_ge(3))

The :class:`~cyberattacksim.db.network.NetworkDB` comes pre-packaged with default network functions:

- :func:`~cyberattacksim.networks.network_db.default_18_node_network`
- :func:`~cyberattacksim.networks.network_db.dcbo_base_network`

There networks are stored in a 'backup' `cyberattacksim/networks/_package_data/network.json` db file.
If the default networks become corrupted, they can be reset using the
:func:`~cyberattacksim.networks.network_db.NetworkDB.reset_default_networks_in_db` function.

As a last resort, the entire db can be rebuilt using the :func:`~cyberattacksim.networks.network_db.NetworkDB.rebuild_db`
function.

.. warning::

        This function completely rebuilds the database. Any custom networks
        saved in the db will be lost.

The GameModeDB and GameModeSchema classes
***************************************

The :class:`~cyberattacksim.game_modes.game_mode_db.GameModeDB` class, used for inserting, querying, updating, and deleting
instances of :class:`~cyberattacksim.game_modes.game_mode.GameMode`, relies upon
:class:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB` at
:attr:`GameModeDB._db<cyberattacksim.networks.network_db.GameModeDB._db>`. It wraps the
:class:`~cyberattacksim.db.cyberattacksim_db_abc.CyberAttackDB` functions,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.insert`,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.update`,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.upsert`,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.all`,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.get`,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.search`,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.count`,
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.remove`, with the return types overridden to return
:class:`~cyberattacksim.game_modes.game_mode.GameMode`.
The :class:`~cyberattacksim.game_modes.game_mode_db.GameModeDB` class writes to a `game_modes.json` file at:

- **Linux** - `~/.local/share/cyberattacksim/db/game_modes.json`
- **Windows** - `~/AppData/cyberattacksim/cyberattacksim/db/game_modes.json`
- **MacOs** - `~/Library/Application Support/cyberattacksim/db/game_modes.json`


First, we must instantiate the :class:`~cyberattacksim.game_modes.game_mode.GameModeDB` with:

.. code:: python

    from cyberattacksim.game_modes.game_mode_db import GameModeDB
    db = GameModeDB()

Next, we have the option to query the db with either the standard :class:`tinydb.queries.Query` class, the extended
:class:`~cyberattacksim.db.query.CyberAttackQuery` class, or by using the game mode specific
:class:`~cyberattacksim.game_modes.game_mode_db.GameModeSchema` class. Here we will use :class:`~cyberattacksim.game_modes.game_mode.GameModeSchema`.
This class has an attribute mapped to each attribute of the attributes of
:class:`~cyberattacksim.game_modes.game_mode.GameMode` (including all nested descendants) as an instance of :class:`~cyberattacksim.db.query.CyberAttackQuery`.
This gives direct access to the specific field within the :class:`~tinydb.database.TinyDB` db file.

The :class:`~cyberattacksim.game_modes.game_mode_db.GameModeSchema` also exposes features that allow for

The following code blocks demonstrate how to use combinations of the :class:`~cyberattacksim.game_modes.game_mode_db.GameModeSchema`
class to build a :class:`~tinydb.queries.Query` chain to query the :class:`~cyberattacksim.game_modes.game_mode_db.GameModeDB`.

**Search for all game modes where the red agent ignores defences:**

.. code:: python

    results = db.search(GameModeSchema.CONFIGURATION.RED.AGENT_ATTACK.IGNORES_DEFENCES.all([True]))

**Search for all game modes where the red agent ignores defences and where the red agents attack alwys succeeds:**

.. code:: python

    results = db.search(
        GameModeSchema.CONFIGURATION.RED.AGENT_ATTACK.IGNORES_DEFENCES.all([True])
        and (GameModeSchema.CONFIGURATION.RED.AGENT_ATTACK.ALWAYS_SUCCEEDS.all([True])
    )

**Search for all game modes where the blue agent uses at least 3 deceptive nodes:**

.. code:: python

    results = db.search(GameModeSchema.BLUE.ACTION_SET.DECEPTIVE_NODES.MAX_NUMBER.ge(3))

The :class:`~cyberattacksim.game_modes.game_mode_db.GameModeDB` comes pre-packaged with default game mode functions:

- :func:`~cyberattacksim.game_modes.game_mode_db.default_game_mode`
- :func:`~cyberattacksim.game_modes.game_mode_db.dcbo_game_mode`

The game modes are stored in a 'backup' `cyberattacksim/game_modes/_package_data/game_modes.json` db file.
If the default networks become corrupted, they can be reset using the
:func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.reset_default_game_modes_in_db` function.

As a last resort, the entire db can be rebuilt using the :func:`~cyberattacksim.game_modes.game_mode_db.GameModeDB.rebuild_db`
function.

.. warning::

        This function completely rebuilds the database. Any custom game modes
        saved in the db will be lost.
