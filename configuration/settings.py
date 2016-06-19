import os, binascii
from datetime import timedelta
from passlib.hash import sha512_crypt

auth_token_timeout = timedelta(minutes=10)
connection_string = "sqlite:///tmp.sqlite3.db"
password_salt = "saltyvader"
listen_address = "0.0.0.0"
token_generator = lambda: binascii.hexlify(os.urandom(20))
password_encryptor = lambda the_password: sha512_crypt.encrypt(the_password, rounds=5000, salt=password_salt)