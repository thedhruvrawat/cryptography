import secrets

def key_generator(length):
    with open("keys.txt", "w") as f:
        # Generate a random string of 1s and 0s of the required length
        mtpkey = bin(secrets.randbits(length))[2:].zfill(length)
        f.write(mtpkey)
    return "key"

key_generator(2048)