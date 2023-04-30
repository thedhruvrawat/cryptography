#!/usr/bin/env python
# The decryption algorithm would work in a similar way as the encryption algorithm
import sys
from BitVector import *

if len(sys.argv) != 3:                                      
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

PassPhrase = "Cryptography is the art of  secret writing"

BLOCKSIZE = 64 
numbytes = BLOCKSIZE // 8 

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)
for i in range(0,len(PassPhrase) // numbytes):
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
    bv_iv ^= BitVector(textstring=textstr)

# Get key from user:
key = None
if sys.version_info[0] == 3:
    key = input("Enter key: ")
else:
    key = raw_input("Enter key: ")
key = key.strip()

# Reduce the key to a bit array of size BLOCKSIZE:
key_bv = BitVector(bitlist = [0]*BLOCKSIZE)
for i in range(0, len(key) // numbytes):
    keyblock = key[i*numbytes:(i+1)*numbytes]
    key_bv ^= BitVector( textstring = keyblock )

# Open the input file and read the ciphertext bitvector:
FILEIN = open(sys.argv[1])
msg_encrypted_bv = BitVector(hexstring=FILEIN.read().strip())
FILEIN.close()

# Create a bitvector for storing the decrypted bit array:
msg_decrypted_bv = BitVector(size=0)

# Carry out differential XORing of bit blocks and decryption:
previous_block = bv_iv
for i in range(0, len(msg_encrypted_bv) // BLOCKSIZE):
    bv_read = msg_encrypted_bv[i * BLOCKSIZE:(i + 1) * BLOCKSIZE]
    if len(bv_read) < BLOCKSIZE:                         
        bv_read += BitVector(size = (BLOCKSIZE - len(bv_read))) 
    bv_read_copy = bv_read.deep_copy()
    bv_read ^= previous_block
    bv_read ^= key_bv
    previous_block = bv_read_copy
    msg_decrypted_bv += bv_read

# Write decrypted bitvector to the output file:
FILEOUT = open(sys.argv[2], "w")
FILEOUT.write(msg_decrypted_bv.get_bitvector_in_ascii())
FILEOUT.close()
