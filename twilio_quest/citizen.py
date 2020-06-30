from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5, sha256

h = generate_password_hash("Hello")
print(h)
print(generate_password_hash("Hello"))


class Citizen:
    """A class that describes a citizen"""
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


def full_name(c):
    return f'{c.first_name} {c.last_name}'


