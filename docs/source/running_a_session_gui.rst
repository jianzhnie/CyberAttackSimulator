=================
Running a session
=================

Gettting started
################

To get started, Navigate to the run session (play icon) page from the sidebar or main menu

.. image:: ../_static/create_template_run.gif
  :width: 800
  :alt: run session

Running a CyberAttackRun session
#################################

The run session page is comprised of 6 sections that represent most configurable elements of the :class: `~cyberattacksim.cyberattacksim_run.CyberAttackRun`.
To launch a run instance navigate to the *Run session* button on the bottom right of the window

Network selection
*****************
The first section displays all networks which can be selected to be used within the run session

Game mode selection
*******************
The next section displays valid game modes compatible with the chosen network which can be selected to be used within the run session

Configurable inputs
*******************
The next section is comprised of 2 tabs which represent configurable elements for agent training and evaluation sessions

Metric display
**************
The next section is a live display of the metrics output by each loop of the currently running session

Log display
***********
The next section is a live display of the logs produced by :class: `~cyberattacksim.cyberattacksim_run.CyberAttackRun`
related to the Individual stages of the run session

Preview output
**********
The next section displays the Animated GIF or WEBM video output produced after an example evaluation run.
If both GIF and WEBM outputs are to be generated, the preview will show the video, otherwise it will show the Animated GIF if only the GIF is to be generated.
