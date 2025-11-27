
from werkzeug.security import generate_password_hash, check_password_hash

password = "test"

pwhash = generate_password_hash(password)

if check_password_hash(pwhash, password):
    print("Password is valid")