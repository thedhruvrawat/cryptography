# BITS F463: Cryptography Assignment

## P1: Breaking of a Classical Cipher

The `Python` script (`encrypt_classical.py`) provided along with this assignment implements an encryption algorithm (cipher), that takes a plaintext message file as input and produces an encrypted file as the output. As a sample to demonstrate the working of the cipher, a `sample_plaintext_p1.txt` and its corresponding `sample_ciphertext_p1.txt` is also provided. The key that has been used to produce this sample ciphertext is `bits@f463`. As part of this problem of the assignment you are supposed to do the following tasks.

1. Explain the encryption algorithm implemented by the `Python` script `encrypt_classical_p1.py`. 
2. Write the corresponding decryption script which will take output generated by the encryption script and
generate the same plaintext as the output that was given to the encryption script as the input. Consider that
both the encryption and decryption scripts are executed with the same key. 
3. You are supposed to submit a **CRACK** code (`crack_classical_p1.py`) which when supplied with a
ciphertext generated by the cipher should produce the corresponding plaintext. 

## P2: Many-Time Pad is not secure

In class, we discussed that OTP has perfect security but when the same key used multiple times it could lead to an insecure cipher.  
1. Write the encryption (`encrypt_mtp_p2.py`) and decryption (`decrypt_mtp_p2.py`) and a key generation
(`key_mtp_p2.py`) program for MTP (Multi time pad) cipher. Assume the plaintext is encoded as ASCII
characters.  
2. Develop a **CRACK** code (`CRACK_p2.py`) which when supplied with a number of ciphertext (say 10)
generated by the cipher using the same key, should produce the corresponding plaintext for all the ciphers.

## P3: 2-Round DES is not secure

The DES performs 16 rounds. You are provided plaintext and a corresponding cipheterext pair in the files `sample_plaintext_p3.txt` and `sample_ciphertext_p3.txt` respectively. The ciphertext has been generated using the DES algorithm with 2 rounds only. The 56-bit key used for encryption is derived for a password containing exactly 7 ASCII characters (8 bit character), where the last character of the password is the character '`a`'. Please note that the password contains ASCII characters not just the alphabets. Your task is to find the plaintext of the ciphertext given in the file named `target_ciphertext_p3.txt`. The last character of the password is revealed to reduce your effort of performing bruteforce attack and make the attack feasible. 