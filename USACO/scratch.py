import os


# reversing a dictionary
def dict_reverse(input_dict):
    """"dict_reverse(inputDict) -> dict
    returns dict with keys/values of inputDict swapped"""

    # crete a new blank dictionary
    reversed_dictionary = {}
    # loop through all of the keys in the input dictionary
    for key in input_dict.keys():
        # reverse the element
        reversed_dictionary[input_dict[key]] = key

    return reversed_dictionary


test_dict = {'adam': 80, 'betty': 60, 'charles': 50}
reversed_dict = dict_reverse(test_dict)
print(reversed_dict)
# should be {80:'adam',60:'betty',50:'charles'} in some order

print('-----------------------------------------------------')
# grades
in_file = open('grades.txt', 'r')

grades = {}
for line in in_file:
    name, grade = line.split()
    if name in grades:
        grades[name][0] += int(grade)
        grades[name][1] += 1
    else:
        grades[name] = [int(grade), 1]

for name in grades:
    print(name, "{0:.2f}".format(grades[name][0] / grades[name][1]))

print('-----------------------------------------------------')
# scrabble
words = open('words.txt', 'r')

values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
          'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
          'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

max_word = ''
max_score = -1

for word in words:
    word = word.strip()
    current_score = 0
    word = word.upper()
    for letter in word:
        current_score += values[letter]

    if current_score > max_score:
        max_score = current_score
        max_word = word

print(max_word)
print(max_score)

print('-----------------------------------------------------')


# letter count
def letter_count(input_string):
    """letter_count(inputString) -> None
    prints alphabetized letter count of letters in inputString"""
    # alphabetizing letters
    letters = {}

    for el in 'abcdefghijklmnopqrstuvwxyz':
        letters[el] = 0

    print(letters)

    input_list = input_string.lower().split()
    for word in input_list:
        for el in word:
            if el in 'abcdefghijklmnopqrstuvwxyz':
                letters[el] += 1

    for el in letters:
        if letters[el]:
            print('{}: {}'.format(el, letters[el]))


# example
letter_count("I like learning Python at Art of Problem Solving!")

print('-----------------------------------------------------')


def translate():
    """translate() -> None
    Prompts user to enter dictionary files and input and output files
    Changes words in input file according to the dictionary file
    Write translation in output file"""
    dict_file_name = input('Enter name of dictionary: ')
    text_file_name = input('Enter name of text file to translate: ')
    output_file_name = input('Enter name of output file: ')

    content_path = '/Users/study_together/Desktop/gitMichael/github_tk_python'
    if os.path.isfile('{}/USACO/{}'.format(content_path, dict_file_name)):
        print('DICTIONARY file exists')
    else:
        print('DICTIONARY file does not exist')
        print("---- Don't worry ----")
        print("I created one for you!")

    if os.path.isfile('{}/USACO/{}'.format(content_path, text_file_name)):
        print('INPUT file exists')
    else:
        print('INPUT file does not exist')


translate()
