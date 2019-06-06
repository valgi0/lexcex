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
parser.add_argument('--command', '-c', nargs=1, type=str, action="store",
                    default=['none'],
                    help="Linux Command on wich you wish to add/remove/see examples")
parser.add_argument('--list', '-l', action="store_true",
                    help="List all commands with at least one examples")
parser.add_argument('--verbosity', '-v', action="store_true")
parser.add_argument('--add', '-a', action="store_true",
                    help="Add examples to selected command")

parse = parser.parse_args()
selected_command = parse.command[0]
listing = parse.list
verbosity = parse.verbosity
adding = parse.add 

if verbosity:
    print("[INFO] Command selected: " + str(selected_command))


############################################################################


def main():
    setUpDirs()
    if listing:
        listCommands()
        exit()
    if adding:
        addExamples()
        exit()
    menu()


def menu():
    print('''
 ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄       ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄       ▄
▐░▌          ▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌
▐░▌          ▐░█▀▀▀▀▀▀▀▀▀  ▐░▌   ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▐░▌   ▐░▌
▐░▌          ▐░▌            ▐░▌ ▐░▌  ▐░▌          ▐░▌            ▐░▌ ▐░▌
▐░▌          ▐░█▄▄▄▄▄▄▄▄▄    ▐░▐░▌   ▐░▌          ▐░█▄▄▄▄▄▄▄▄▄    ▐░▐░▌
▐░▌          ▐░░░░░░░░░░░▌    ▐░▌    ▐░▌          ▐░░░░░░░░░░░▌    ▐░▌
▐░▌          ▐░█▀▀▀▀▀▀▀▀▀    ▐░▌░▌   ▐░▌          ▐░█▀▀▀▀▀▀▀▀▀    ▐░▌░▌
▐░▌          ▐░▌            ▐░▌ ▐░▌  ▐░▌          ▐░▌            ▐░▌ ▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▐░▌   ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▐░▌   ▐░▌
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀       ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀       ▀
          ''')
    print('\n')
    print('''
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
          ''')
    print("Menu: \n")
    print("1. Add examples")
    print("2. View examples")
    print("3. List all commands")
    print("4. Exit")
    choise = input('Do your choise: ')
    if int(choise) not in range(1,5):
        print("Just 1,2,3,4, allowed mate... What did you think?")
        exit()
    if int(choise) == 1:
        askCommand()
        addExamples()
    if int(choise) == 3:
        listCommands()
    if int(choise) == 2:
        askCommand()
        printExamples()



def printExamples():
    example = (user_home.joinpath(lexcex_dir)
               .joinpath(lexcex_examples_dir)
               .joinpath(selected_command))
    if example.exists():
        fd = example.open('r')
        for line in fd.readlines():
            printExample(json.loads(line))


def printExample(example):
    print("#"*80+"\n")
    print("Command: " + example[COMMAND])
    print("Description: " + example[DESCR])
    if len(example[FLAGS]) >= 1:
        print("FLAGS: ")
        for key, value in example[FLAGS].items():
            print("Flag: {}  => {} ".format(key, value))


def askCommand():
    global selected_command
    print("Add example section")
    selected_command = input("Type the command you wish add example for: ")




def listCommands():
    commands_dir = user_home.joinpath(lexcex_dir).joinpath(lexcex_examples_dir)
    commands = [c.name for c in commands_dir.iterdir() if c.is_file()]
    print('Command found {}\n'.format(len(commands)))
    for c in commands:
        print(c)



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
    Path(outfile).open('a').write('\n')




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
