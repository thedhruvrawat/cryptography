cipher_text_file = input("Enter the ciphertext file name: ")
key_file = input("Enter the keys file name: ")
plain_text_file = input("Enter the plaintext file name: ")

with open(cipher_text_file, "rb") as input, open(key_file, "rb") as key, open(plain_text_file, "wb") as output:
        while True:
            input_hex = input.read(2)
            if not input_hex:
                break
            input_byte = bytes.fromhex(input_hex.decode("utf-8"))
            key_byte = key.read(1)
            if not input_byte or not key_byte:
                break
            output_byte = bytes([input_byte[0] ^ key_byte[0]])
            output.write(output_byte)

print(f"Decoded plaintext saved to file '{plain_text_file}'.")