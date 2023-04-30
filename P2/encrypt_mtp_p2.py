plain_text_file = input("Enter the plaintext file name: ")
key_file = input("Enter the keys file name: ")
cipher_text_file = input("Enter the ciphertext file name: ")

with open(plain_text_file, "rb") as input_file, open(key_file, "rb") as key_file, open(cipher_text_file, "wb") as output_file:
        while True:
            input_byte = input_file.read(1)
            key_byte = key_file.read(1)
            if not input_byte or not key_byte:
                break
            output_byte = bytes([input_byte[0] ^ key_byte[0]])
            output_file.write(output_byte.hex().encode("utf-8"))

print(f"Ciphertext saved to file '{cipher_text_file}' in hexadecimal format.")