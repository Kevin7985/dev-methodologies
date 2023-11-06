from random import randint


def generateToken():
    alphabet = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
    token = "bookcrossing."

    for i in range(100):
        token += alphabet[randint(0, len(alphabet) - 1)]

    return token
