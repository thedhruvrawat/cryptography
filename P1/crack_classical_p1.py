from typing import List
from BitVector import *
import collections
import math
import binascii
import string

def find_spaces_in_ciphertexts(ciphers: List[BitVector], space_bv: BitVector, threshold_val: int) -> List[int]:
    final_key = [None] * 8
    for current_index, i in enumerate(ciphers):
        counter = collections.Counter()
        for index, j in enumerate(ciphers):
            if current_index != index:
                bw_xor = i^j
                cipher_char = bw_xor.get_bitvector_in_ascii()
                for indexOfChar, char in enumerate(cipher_char):
                    if char.isalpha():
                        if char in string.printable:
                            counter[indexOfChar] += 1
        knownSpaceIndexes = [ind for ind, val in counter.items() if val >= threshold_val]
        checking_for_space = i ^ space_bv
        xor_with_spaces = checking_for_space.get_bitvector_in_ascii()
        for index in knownSpaceIndexes:
            hex_value = binascii.hexlify(bytes(xor_with_spaces[index].encode(encoding='ascii'))).decode('ascii')
            final_key[index] = hex_value
    return final_key

def decrypt_file(input_file_path: str, output_file_path: str, passphrase: str) -> None:    
    ciphers = list()  
    decode = list()
    cipher_block = BitVector(size=0) 
    last_block = BitVector(size=64)
    with open(input_file_path, 'rb') as f:
        for temp in iter(lambda: f.read(16), b''):
            read_block = BitVector(hexstring=temp.decode('ascii'))
            ciphers.append(read_block)
            decode.append(read_block)
    # XOR and update the ciphertext blocks
    for i in range(len(ciphers)):
        cipher_block = ciphers[i] ^ last_block
        last_block = ciphers[i].deep_copy()
        ciphers[i] = cipher_block
    init_vector = BitVector(bitlist=[0] * 64)
    for i in range(0, len(passphrase) // 8):
        start_index = i*8
        end_index = (i+1)*8
        sample = passphrase[start_index:end_index]
        init_vector ^= BitVector(textstring=sample)      
    last_block = init_vector
    space_bv = BitVector(textstring=' ' * 8)
    threshold_val = math.floor(0.75*len(ciphers))
    if ciphers:
        ciphers.pop(0)    
    final_key = find_spaces_in_ciphertexts(ciphers, space_bv, threshold_val)    
    final_key_hex = ''
    for val in final_key:
        if val is not None:
            final_key_hex += val
        else:
            final_key_hex += '00'    
    secret_key = BitVector(hexstring=final_key_hex)
    final_msg_decrypted = BitVector(size=0)
    # XOR and append the decrypted blocks
    for i in range(len(decode)):
        xor_val = last_block ^ secret_key
        decrypted_block = decode[i] ^ xor_val
        last_block = decode[i].deep_copy()
        final_msg_decrypted += decrypted_block
    final_output = final_msg_decrypted.get_bitvector_in_ascii()
    FILEOUT = open(output_file_path, 'w')
    FILEOUT.write(final_output)
    FILEOUT.close()
    final_key_ascii = bytes.fromhex(final_key_hex).decode('ascii')  
    print('Recovered Secret key: ' + final_key_ascii)  

def main():
    input_file = 'ciphertext.txt'
    output_file = 'recoveredtext.txt'
    PassPhrase = "Cryptography is the art of  secret writing"
    try:
        decrypt_file(input_file, output_file, PassPhrase)
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

if __name__ == '__main__':
    main()