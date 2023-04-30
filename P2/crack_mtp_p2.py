import binascii

with open('ciphertext_p2.txt', encoding='utf-8') as file:
    ciphertexts = []
    for line in file:
        hex_str = line.rstrip()
        ciphertexts.append(binascii.unhexlify(hex_str))

plaintexts = []

for ciphertext in ciphertexts:
    ciphertext_length = len(ciphertext)
    cleartext = [0] * ciphertext_length
    for i in range(ciphertext_length):
        cleartext[i] = 42 # *
    plaintexts.append(bytearray(cleartext))

CIPHERLEN = 0
for line in ciphertexts:
    if len(line) > CIPHERLEN:
        CIPHERLEN = len(line)

key = bytearray(CIPHERLEN)

for col in range(CIPHERLEN):
    other_ciphers = []
    for line in ciphertexts:
        if len(line) > col:
            other_ciphers.append(line)
    for cipher in other_ciphers:
        FOUND_SPACE = True
        for row in other_ciphers:
            char = row[col] ^ cipher[col]
            if len(row) < col or (char != 0 and not ((65 <= char <= 90) or (97 <= char <= 122))):
                FOUND_SPACE = False
                break
        if FOUND_SPACE:
            INDEX = 0
            key[col] = cipher[col] ^ 32
            for i, plaintext in enumerate(plaintexts):
                if len(plaintext) != 0 and col < len(plaintext):
                    result = cipher[col] ^ other_ciphers[INDEX][col]
                    if result == 0:
                        plaintext[col] = 32 # ' '
                    elif 97 <= result <= 122:
                        plaintext[col] = result - 32
                    elif 65 <= result <= 90:
                        plaintext[col] = result + 32
                    INDEX += 1
            break

with open('recoveredtext_p2.txt', 'w', encoding='utf-8') as f:
    for line in plaintexts:
        decoded_line = line.decode('ascii')
        f.write(decoded_line + '\n')
