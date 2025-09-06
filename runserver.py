#!/usr/bin/env python -B
# Instructions for running and debugging this python file in VSCode
#
# In VSCode, press Cmd-Shift-P (on Mac) or Ctrl-Shift-P (on Windows).
#   In the command selection text box, type "Python Create"
#   From the options dropdown select "Python Create Environment"
#   From the next options dropdown select "venv"
#
# The program assumes that you have python 3.10 and pip installed on your machine.
# In the VSCode terminal window type the following:
#    pip install -r requirements.txt
#    python runserver.py
#    Navigate to http://localhost:5000 link in terminal window
#    Navigate to http://127.0.0.1:5000/apidocs for the swagger API documentation
#    To stop the server, go to the terminal window and press Ctrl-C

import sys 
import os
sys.dont_write_bytecode = True
from app import create_app


app = create_app()
print(app.url_map)

app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
