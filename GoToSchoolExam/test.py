from flask import Flask, render_template, request, jsonify
import json
import sqlite3

app = Flask(__name__)
co = sqlite3.connect('texts.sqlite')
cu = co.cursor()
cu.execute("DELETE FROM information")
co.commit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cipher', methods=["POST"])
def calculate():
    # one type byte to string second string to dict
    information = json.loads(json.loads(request.data))

    print(request)
    print(type(information))

    functions = [rot, pig_latin]

    t = check_type(int(information['cipher']))
    if t == 2:
        new_text = ""
    else:
        new_text = functions[t](information['txt'], int(information['cipher']))

    connection = sqlite3.connect('texts.sqlite')
    cursor = connection.cursor()

    listing = [int(information['cipher']), information['txt'], new_text]
    cursor.execute("INSERT INTO information (cipher, inp, outp) VALUES (?, ?, ?)", listing)
    cursor.execute("")
    connection.commit()

    print("INPUT text:" + information['txt'])
    print("CIPHER type:" + information['cipher'])
    print("OUTPUT text:" + new_text)

    return jsonify({"text": new_text})


def rot(string, num):
    converted_string = ""
    alphabet = "".join([chr(i) for i in range(ord('A'), ord('Z') + 1)]) + \
               "".join([chr(i) for i in range(ord('a'), ord('z') + 1)]).lower()
    for letter in string:
        if letter in alphabet:
            is_lower_char = min((ord(letter) - ord('A')) // 26, 1)
            converted_string += alphabet[26 * is_lower_char + (ord(letter) - ord('A') - 6 * is_lower_char + num) % 26]
        else:
            converted_string += letter
    return converted_string


def rot_decipher(string, num):
    deciphered_string = ""
    alphabet = "".join([chr(i) for i in range(ord('A'), ord('Z') + 1)]) + \
               "".join([chr(i) for i in range(ord('a'), ord('z') + 1)]).lower()

    for letter in string:
        if letter in alphabet:
            is_lower_char = min((ord(letter) - ord('A')) // 26, 1)
            deciphered_string += alphabet[26 * is_lower_char + (ord(letter) - ord('A') - 6 * is_lower_char - num) % 26]
        else:
            deciphered_string += letter

    return deciphered_string


def pig_latin(string, n=None):
    new_string = ""
    current_word = ""
    alphabet = 'acbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    string += " "

    for c in string:
        if c in alphabet:
            current_word += c
        else:
            prefix = ''
            count = 0
            for l in current_word:
                if count != 0 and l in 'aeiou':
                    break
                else:
                    count += 1
                    prefix += l

            if current_word == "":
                new_string += c
            else:
                new_string += current_word[count:] + prefix + "ay" + c
            current_word = ""

    return new_string


def check_type(cipher_id):
    if 0 < cipher_id < 26:
        return 0
    elif cipher_id == 26:
        return 1
    elif cipher_id == 0:
        return 2


app.run(debug=True)
