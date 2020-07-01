# making a terminal interpretation in python using OS and shutil
import os
import shutil


def valid_command(c):
    """Returns if a command is valid or not"""
    # if len(c) == 0:
    #     # no command was given and if we return True everything will ignore it and nothing prints
    #     return True
    #
    # elif
    return True


# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory/5137509#5137509
# https://stackoverflow.com/a/10989155

content_path = os.getcwd()  # gives us the current path
root_path = '/'.join(content_path.split('/')[:3])  # gives us the result if you were to do cd ~ (Users, current_user)
logged_user = root_path.split("/")[-1]  # getting the user that's logged in
comp_user = os.uname()[1]

# os.getcwd()
# os.chdir()
# os.listdir(path=content_path)

while True:
    # getting current directory
    curr_dir = content_path.split("/")[-1]

    if curr_dir == '':
        # we are at the highest level therefore we set it to '/'
        curr_dir = '/'
    elif curr_dir == logged_user:
        # we are at the root therefore we denote it with tilda
        curr_dir = '~'
    elif content_path.count('/') < 2:
        # /Users or /otherdir with only on slash we are below root
        curr_dir = f'/{curr_dir}'

    # setting a message for the terminal command request
    message = f'{logged_user}@{comp_user} {curr_dir}'

    # ask for a terminal command and display the current working directory with the variable message
    command = input(f'{message} % ').strip()

    if valid_command(command):
        # execute command given to us

        if command == 'pwd':
            # print the current path
            print(content_path)

        elif command[:2] == 'ls':
            # get all files (hidden and non-hidden)
            ls_files = os.listdir(path=content_path)

            # strip all elements
            for i in range(len(ls_files)):
                ls_files[i] = ls_files[i].strip()

            # we check if its a normal ls or ls -la
            if command == 'ls':
                # list all non hidden files (without the dots at the start)
                for el in ls_files:
                    if el[0] == '.':
                        # This is a hidden file therefore we ignore it
                        pass
                    else:
                        print(el)
            elif command == 'ls -la':
                # list all files including hidden files
                for el in ls_files:
                    print(el)

        elif command[:2] == 'cd':
            # command cd
            if len(command) < 4:
                # throw an error
                print('No given directory.')
            elif command[3] == '~':
                # go to root no matter the location
                content_path = root_path
                os.chdir(content_path)
            elif command[3:5] == '..':
                # move one directory up
                content_path = '/'.join(content_path.split('/')[:-1])

                # check if the content path is empty therefore we set it to '/'
                if content_path == '':
                    content_path = '/'

                os.chdir(content_path)
            else:
                # we are switching to a directory
                dir_name = command[3:].strip()
                print(dir_name)
                if os.path.isdir(f'{content_path}/{dir_name}'):
                    # directory exists therefore we move into it
                    content_path = f'{content_path}/{dir_name}'
                    os.chdir(content_path)
                else:
                    print("This directory doesn't exist.")
    else:git
        # throw an error
        print('Invalid command')

