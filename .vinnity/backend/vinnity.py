#vinnity.py
#Management and main file
import os
import sys
import subprocess
import time
import server
import setup
import argparse as args

logo = """
 _    ___             _ __           __  ___                                                  __ 
| |  / (_)___  ____  (_) /___  __   /  |/  /___ _____  ____ _____ ____  ____ ___  ___  ____  / /_
| | / / / __ \/ __ \/ / __/ / / /  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ __ `__ \/ _ \/ __ \/ __/
| |/ / / / / / / / / / /_/ /_/ /  / /  / / /_/ / / / / /_/ / /_/ /  __/ / / / / /  __/ / / / /_  
|___/_/_/ /_/_/ /_/_/\__/\__, /  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/ /_/ /_/\___/_/ /_/\__/  
                        /____/                            /____/                                 
"""

parser = args.ArgumentParser(description="All commands is there")
parser.add_argument("-dlt", "--delete", help="Delete vinnity from your server or personal computer.")
parser.add_argument("-s", "--server", help="You should use it with an command." )
parser.add_argument("-o", "--off", help="Turns off the server.")
parser.add_argument("-O", "--on", help="Turns on the server.")
parser.add_argument("-m", "--messages", help="Shows messages")
