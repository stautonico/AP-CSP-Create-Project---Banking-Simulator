import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)


def register(username, password):
    password = password.encode()
    hashed_password = hash_password(password)
    return username, hashed_password


username, password = register('tman540', "password")

print(len(password))
