ReadMe
======
:Phase:
   Phase 2
:Authors:
   Patrick Hoey,
   Ryan McCann,
   Divyaksh Wadhwa,
   Parikshit Jadav

Environment
===========
- Ubuntu 20.04 LTS
- Python 3.8.10

Requirements
============
- pytest (if you want to run full test suite)
- sphinx (if you want to regenerate the documentation on your own machine)
- groundwork-sphinx-theme (If you want to regenerate pretty documentation instead of being a basic light theme normie)

if you want to install all of these at once run

(note: this has only been tested on my machine, inform me of errors)

.. code-block:: bash

   cd phase_1
   pip3 install -r requirements.txt

Usage
=====
*Basic Test*

.. code-block:: bash

   cd phase_2
   # Run server in background
   python3 scripts/udp_echo_server.py
   # Separate terminal
   python3 scripts/udp_client.py

*Full Test Suite*

.. code-block:: bash

   cd phase_1
   # Run Server in background
   python3 scripts/udp_echo_server.py &
   # Separate terminal, requires pytest
   pytest

:ref:`Home`

