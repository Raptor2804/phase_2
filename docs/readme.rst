ReadMe
======
:Phase:
   Phase 1
:Authors:
   Patrick Hoey

Environment
===========
- Ubuntu 20.04 LTS
- Python 3.8

Requirements
============
- pytest (if you desire to run full test suite)
- sphinx (if you desire to generate the documentation on your own machine)
- groundwork-sphinx-theme (If you want pretty documentation instead of being a basic light theme normie)

if you want to install all of these at once run

(note: this has only been tested on my machine, inform me of errors)

.. code-block:: bash

   cd phase_1
   pip3 install -r requirements.txt;

Usage
=====
*Basic Test*

.. code-block:: bash

   cd phase_1
   # Run server in background
   python3 scripts/udp_server.py
   # Separate terminal
   python3 scripts/udp_client.py

*Full Test Suite*

.. code-block:: bash

   cd phase_1
   # Run Server in background
   python3 scripts/udp_server.py &
   # Separate terminal, requires pytest
   pytest

