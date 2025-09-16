# WARNING: On Linux, you may need to run this first for TKinter to be included in your OS install of Python:
# sudo apt update
# sudo apt install python3-tk
# On Windows and MacOS, TKinter should be included by default.
# (And note, if you want to actually download/install all available updates, use `sudo apt upgrade -y` or `sudo apt full-upgrade -y` to include removing old versions and install new dependencies)

# --- --- ---
# Import Options in Python...
# Each .py file is a module. We can import them a couple of different ways.
# Each folder can act like a package now as well, no longer requiring __init__.py since Python 3.3.

# OPTION 1:     Import the entire file (module), but requires prefacing every API call with the fully qualified path each time:
# import gui.firstbasics
# window = gui.firstbasics.ExampleGUI()
# window.run()

# OPTION 2:     Import the API Member INSIDE the file (module):
from gui.firstbasics import ExampleGUI
window = ExampleGUI()
window.run()

# OPTION 3:     Alias for the entire file (module):
# import gui.firstbasics as fb
# window = fb.ExampleGUI()
# window.run()

# OPTION 4:     Alias for JUST the API Member INSIDE the file (module):
# from gui.firstbasics import ExampleGUI as EG
# window = EG()
# window.run()
