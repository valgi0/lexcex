import argparse
from pathlib import Path 

########################## SETTING VARIABLES ##################################
user_home = Path.home()
lexcex_dir = '.lexcex'
lexcex_examples_dir = 'examples'



########################## GLOBAL VARIBLES ##################################

selected_command = ''
verbosity = False
listing = False

###############################################################################
description = '''
Linux commands EXtensible Collection of EXamples\n\n
This tool collects a lot of examples of Linux commands to make easy
remember wich flag you have to use in order to achieved a precise task.
'''

parser = argparse.ArgumentParser(prog="lexcex",
                                 description=description)
parser.add_argument('command', type=str, action="store",
                    help="Linux Command on wich you wish to add/remove/see examples")
parser.add_argument('--list', '-l', action="store_true",
                    help="List all commands with at least one examples")
parser.add_argument('--verbosity', '-v', action="store_true")

parse = parser.parse_args()
selected_command = parse.command
listing = parse.list
verbosity = parse.verbosity
if verbosity:
    print("[INFO] Command selected: " + str(selected_command))


############################################################################


def main():
    setUpDirs()


def setUpDirs():
    directory_path = user_home.joinpath(lexcex_dir)
    directory = str(directory_path)
    if verbosity:
        print("[INFO] Checks if {} exists".format(directory))
    if Path(directory).exists():
        if verbosity:
            print("[INFO] {} exists".format(directory))
    else:     
        if verbosity:
            print("[INFO] {} not exists".format(directory))
        Path(directory).mkdir() 
        if verbosity:
            print("[INFO] {} Created".format(directory))
        directory_path.joinpath(lexcex_examples_dir).mkdir()
        if verbosity:
            print("[INFO] {} Created".format(lexcex_examples_dir))


if __name__ == "__main__":
    main()
