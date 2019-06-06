#!/usr/bin/python3

import argparse
from pathlib import Path 
import json




########################## SETTING VARIABLES ##################################
user_home = Path.home()
lexcex_dir = '.lexcex'
lexcex_examples_dir = 'examples'




########################## GLOBAL VARIBLES ##################################

selected_command = ''
verbosity = False
listing = False
adding = False 




########################## JSON KEY STRING #################################

COMMAND = 'command'
FLAGS = 'flags'
DESCR = 'description'


################################## ARGUMENTS ###################################

description = '''
Linux commands EXtensible Collection of EXamples.
This tool collects a lot of examples of Linux commands to make easy
remember wich flag you have to use in order to achieved a precise task.
'''

parser = argparse.ArgumentParser(prog="lexcex",
                                 description=description)
parser.add_argument('command', type=str, action="store", required=False,
                    help="Linux Command on wich you wish to add/remove/see examples")
parser.add_argument('--list-commands', '-lc', action="store_true",
                    help="List all commands with at least one examples")
parser.add_argument('--verbosity', '-v', action="store_true")
parser.add_argument('--add', '-a', action="store_true",
                    help="Add examples to selected command")

parse = parser.parse_args()
selected_command = parse.command
listing = parse.listcommands
verbosity = parse.verbosity
adding = parse.add 

if verbosity:
    print("[INFO] Command selected: " + str(selected_command))


############################################################################


def main():
    setUpDirs()
    if adding:
        addExamples()


def addExamples():
    global selected_command
    com = input("Insert complete examples: ")
    desc = input("Insert a short description: ")
    check = input("Would you like insert a short description for flags?[Y/N]:").lower()
    flags = dict()
    if 'y' in check:
        while True:
            flag = input("Type the flag[STOP to end]: ")
            if 'STOP' in flag:
                break
            desc = input("Insert description: ")
            flags[flag] = desc
    command_complete = dict()
    command_complete[COMMAND] = com
    command_complete[DESCR] = desc
    command_complete[FLAGS] = flags
    outfile = str(user_home.joinpath(lexcex_dir)
                 .joinpath(lexcex_examples_dir)
                 .joinpath(selected_command))
    if verbosity:
        print("Examles will be saved in {} ".format(outfile))
    if Path(outfile).exists():
        json.dump(command_complete, Path(outfile).open('a'))
    else:
        json.dump(command_complete, Path(outfile).open('w'))







def setUpDirs():
    '''
    Creates sttings file and directory
    '''
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
