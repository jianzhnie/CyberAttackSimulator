.. _getting-started:

Getting Started
===============


Pre-Requisites
**************
To get CyberAttackSim installed, you will need to have the following
installed:

**Bash**

* ``python >= 3.8.*, <= 3.10.*``
* ``python3-pip``
* ``virtualenv``

**Powershell**

* ``python >= 3.8.*, <= 3.10.*``

CyberAttackSim is designed to be OS-agnostic, and thus should work on most variations/distros of Linux, Windows, and MacOS.

Environment Setup
*****************

CyberAttackSim operates from the users home directory where it has two locations, one hidden for backend stuff, and one user-facing
for user files. To initialise this environment, run:



.. tabs::

    .. code-tab:: bash
        :caption: Bash

        mkdir ~/yawning_titan
        cd ~/yawning_titan
        python3 -m venv .venv
        source .venv/bin/activate
        pip install <path to downloaded yawningtitan .whl file>
        CyberAttackSim setup

    .. code-tab:: powershell
        :caption: Powershell

        mkdir ~\yawning_titan
        cd ~\yawning_titan
        python3 -m venv .venv
        attrib +h .venv /s /d # Hides the .venv directory
        .\.venv\Scripts\activate
        pip install <path to downloaded yawningtitan .whl file>
        CyberAttackSim setup



Starting CyberAttackSim
**********************

The best way to begin working with CyberAttackSim is to the GUI.

.. code:: bash

    CyberAttackSim gui

See CyberAttackSim GUI :ref:`yt-gui` for a guide on how to use the GUI.

Alternatively, you can work with CyberAttackSim from Jupyter Labs.

.. code:: bash

    CyberAttackSim notebooks

Running CyberAttackSim
*********************

From a notebook in Jupyter Lab, import :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` and instantiate it.
This will run the :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` using all default parameters. With
``auto=True``, this will perform the ``.setup()``, ``.train()``, and ``.evaluate()``.

.. code:: python

    from yawning_titan.yawning_titan_run import YawningTitanRun

    yt_run = YawningTitanRun()

The :class:`~yawning_titan.yawning_titan_run.YawningTitanRun` class is fully configurable. Check out the
:class:`~yawning_titan.yawning_titan_run.YawningTitanRun` docs for further customisation.



Development Install
*******************

For those wishing to install CyberAttackSim and use it or extend it from within an IDE, perform the following development installation:

1. Navigate to the CyberAttackSim folder and create a new python :term:`Virtual Environment` (**venv**)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   python3 -m venv venv


2. Activate the :term:`venv<Virtual Environment>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tabs::

    .. code-tab:: bash
        :caption: Bash

        source venv/bin/activate

    .. code-tab:: powershell
        :caption: Powershell

        .\venv\Scripts\activate


3. Install CyberAttackSim into the :term:`venv<Virtual Environment>` along with all of its dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   python3 -m pip install -e .[dev]
