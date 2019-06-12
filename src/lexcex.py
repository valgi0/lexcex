#!/usr/bin/python3

import argparse
from pathlib import Path
import json
import os

# ------------------------- SETTING VARIABLES ----------------------------
user_home = Path.home()
lexcex_dir = '.lexcex'
lexcex_examples_dir = 'examples'


# ------------------------ GLOBAL VARIBLES -----------------------------
selected_command = ''
verbosity = False
listing = False
adding = False
cleaning = False
removing = False

# -------------------------- JSON KEY STRING -------------------------
COMMAND = 'command'
FLAGS = 'flags'
DESCR = 'description'


# ----------------------------- ARGUMENTS -----------------------------
description = '''
Linux commands EXtensible Collection of EXamples.
This tool collects a lot of examples of Linux commands to make easy
remember wich flag you have to use in order to achieved a precise task.
'''


parser = argparse.ArgumentParser(prog="lexcex",
                                 description=description)
parser.add_argument('--command', '-c', nargs=1, type=str, action="store",
                    default=['none'],
                    help='''Linux Command on wich you wish
                    to add/remove/see examples''')
parser.add_argument('--list', '-l', action="store_true",
                    help="List all commands with at least one examples")
parser.add_argument('--verbosity', '-v', action="store_true")
parser.add_argument('--add', '-a', action="store_true",
                    help="Add examples to selected command")
parser.add_argument('--clean', action="store_true",
                    help='Clean all examples')
parser.add_argument('--remove', action='store_true',
                    help='Remove all examples of a single command')
parse = parser.parse_args()
selected_command = parse.command[0]
listing = parse.list
verbosity = parse.verbosity
adding = parse.add
cleaning = parse.clean
removing = parse.remove

if verbosity:
    print("[INFO] Command selected: " + str(selected_command))


############################################################################


def main():
    setUpDirs()
    checkFlags()
    if listing:
        listCommands()
        exit()
    if adding:
        addExamples()
        exit()
    if removing:
        deleteOne()
    if cleaning:
        deleteAll()
    menu()


def checkFlags():
    if adding and selected_command == 'none':
        print('You MUST specify for wich command an example is being added')
        exit()
    if removing and selected_command == 'none':
        print('You MUST specify the command to remove')
        exit()
    if cleaning and (removing | adding | listing):
        print("You can select more commands at once.. do better next time")
        exit()
    if adding and (listing | removing):
        print("You can select more commands at once.. do better next time")
        exit()
    if (removing and listing):
        print("You can select more commands at once.. do better next time")
        exit()


def menu():
    os.system('clear')
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
    choise = -1
    while int(choise) != 5:
        if int(choise) != -1:
            os.system('clear')
        print("*"*50)
        print("\tMenu: \n")
        print("*"*50)
        print("\n1. Add examples")
        print("2. View examples")
        print("3. List all commands")
        print("4. Delete Section")
        print("5. Exit")
        choise = input('\nDo your choise: ')
        if int(choise) not in range(1, 6):
            print("Just 1,2,3,4, allowed mate... What did you think?")
            exit()
        if int(choise) == 1:
            askCommand()
            addExamples()
            input("Press any key to continue....")
        if int(choise) == 3:
            listCommands()
            input("Press any key to continue....")
        if int(choise) == 2:
            askCommand()
            printExamples()
            input("Press any key to continue....")
        if int(choise) == 4:
            deleteMenu()
            input("Press any key to continue....")


def deleteMenu():
    ok = True
    choise = ''
    while ok:
        os.system('clear')
        print("\n---- Delete Menu ---- ")
        print("\n1. Delete All Commands")
        print("2. Delete Single Command")
        print("3. Delete Examples")
        choise = input('do your choise: ')
        if int(choise) not in range(1, 6):
            input("Just 1,2,3,4, allowed mate... What did you think?")
        else:
            ok = False
    if int(choise) == 1:
        deleteAll()
    if int(choise) == 2:
        deleteOne()
    if int(choise) == 3:
        deleteExample()


def deleteAll():
    listCommands()
    choise = input("\n Proceed?[Y/N]: ")
    if 'y' in choise.lower():
        directory = (user_home.joinpath(lexcex_dir)
                     .joinpath(lexcex_examples_dir))
        for cmd in directory.iterdir():
            cmd.unlink()


def deleteOne():
    global selected_command
    if selected_command == 'none':
        askCommand()
    choise = input("Remove {}?[Y/N]: ".format(selected_command))
    if 'y' in choise.lower():
        (user_home.joinpath(lexcex_dir)
         .joinpath(lexcex_examples_dir)
         .joinpath(selected_command)
         .unlink())


def deleteExample():
    print("Currently not implemented... ;*(")
    print("Delete it directly in json file man!")


def printExamples():
    example = (user_home.joinpath(lexcex_dir)
               .joinpath(lexcex_examples_dir)
               .joinpath(selected_command))
    if example.exists():
        fd = example.open('r')
        os.system('clear')
        for line in fd.readlines():
            printExample(json.loads(line))
    print("#"*80)

def printExample(example):
    print('\n' + "#"*80+"\n")
    print("Command:  " + example[COMMAND])
    print("\nDescription: \n" + example[DESCR])
    if len(example[FLAGS]) >= 1:
        print("------------ FLAGS ------------")
        for key, value in example[FLAGS].items():
            print("Flag: {}  => {} ".format(key, value))
    

def askCommand():
    global selected_command
    print("Existing commands: ")
    listCommands(' ')
    selected_command = input("\n\n--->Type the command desired: ")


def listCommands(endchar='\n'):
    commands_dir = user_home.joinpath(lexcex_dir).joinpath(lexcex_examples_dir)
    commands = [c.name for c in commands_dir.iterdir() if c.is_file()]
    os.system('clear')
    print("#" * 80)
    print("\t\t List section ")
    print("#" * 80)
    print('\n' + '-'*80)
    print('Command found {} \t|\n'.format(len(commands)))
    print('-----------------------')
    for c in commands:
        print(c, end=endchar)
    print('\n' + '-'*80)


def addExamples():
    global selected_command
    com = input("Insert complete examples: ")
    desc = input("Insert a short description: ")
    check = input("Would you like insert a short description for flags?[Y/N]:")
    flags = dict()
    if 'y' in check.lower():
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
