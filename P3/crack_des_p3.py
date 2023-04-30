import sys
import os
from BitVector import BitVector

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def updateProgressBar(total, progress):
    """
    Displays or updates a console progress bar.

    Original source: https://stackoverflow.com/a/15860757/1391441
    """
    barLength, status = 50, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r{} {:.0f}% {}".format(
        "█" * block + "-" * (barLength - block), round(progress * 100, 0),
        status)
    sys.stdout.write(text)
    sys.stdout.flush()

SBOX = [
          [ [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
            [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
            [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
            [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
          [ [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
            [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
            [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
            [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
          [ [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
            [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
            [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
            [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
          [ [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
            [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
            [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
            [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
          [ [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
            [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
            [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
            [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
          [ [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
            [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
            [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
            [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
          [ [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
            [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
            [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
            [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
          [ [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
            [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
            [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
            [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
       ]



def sBoxSubstitution(expanded_half_block):
    substitution_result = BitVector(size=32)
    # segments = [expanded_half_block[x*6:(x+1)*6] for x in range(8)]
    segments = []  # create an empty list to store the segments
    for i in range(8):
        start_index = i * 6
        end_index = (i + 1) * 6
        segment = expanded_half_block[start_index:end_index]
        segments.append(segment)  # append the extracted segment to the list of segments
    for sindex, segment in enumerate(segments):
    # extract the first and last element of the segment and calculate row value
      first_elem, last_elem = segment[0], segment[-1]
      row = 2 * first_elem + last_elem
      
      # extract the second to fifth element of the segment and convert to int for column value
      column_str = segment[1:5]
      column = int(column_str)
      
      # calculate the start and end indices for the output sub-list
      start_index = sindex * 4
      end_index = (sindex + 1) * 4
      
      # get the S-box value for the given row and column, and store as a BitVector
      s_box_value = SBOX[sindex][row][column]
      bit_vector = BitVector(intVal=s_box_value, size=4)
      
      # assign the BitVector to the appropriate slice of the output list
      substitution_result[start_index:end_index] = bit_vector
    return substitution_result

def permuteBitvector(bv, permutation_table, unpermute):
    """
    This function takes in a BitVector object `bv` and a permutation table `permutation_table`
    and returns a new BitVector object with the bits of `bv` permuted according to `permutation_table`.
    """
    # if len(bv) != len(permutation_table):
    #     raise ValueError("The length of the BitVector object does not match the length of the permutation table")
    if not unpermute:
      permuted_bv = bv.permute(permutation_table)
    else :
      permuted_bv = bv.unpermute(permutation_table)
    return permuted_bv



PERMUTATION_BOX = [ 15, 6,  19, 20, 28, 11, 27, 16, 
                    0, 14,  22, 25, 4,  17, 30, 9, 
                    1,  7,  23, 13, 31, 26, 2,  8,
                    18,12,  29, 5,  21, 10, 3,  24 ]


EXPANSION_PERMUTATION_TABLE = [ 31, 0,  1,  2,  3,  4,  
                                 3, 4,  5,  6,  7,  8,
                                 7, 8,  9,  10, 11, 12,
                                11, 12, 13, 14, 15, 16, 
                                15, 16, 17, 18, 19, 20, 
                                19, 20, 21, 22, 23, 24, 
                                23, 24, 25, 26, 27, 28, 
                                27, 28, 29, 30, 31, 0 ]


def mergeBlocks(left, right):
    return left + right

def decoder(round_keys, block):
    # divide the block into two halves
    leftBlock, rightBlock = block[:32], block[32:]
    # perform the feistel function for each round
    for key in round_keys:
        expandedRightBlock = permuteBitvector(rightBlock, EXPANSION_PERMUTATION_TABLE, False)
        temp_xor = expandedRightBlock ^ key
        temp_sboxes = sBoxSubstitution(temp_xor)
        res = permuteBitvector(temp_sboxes, PERMUTATION_BOX, False)
        modLeftBlock = leftBlock ^ res
        leftBlock, rightBlock = rightBlock, modLeftBlock

    # concatenate the left and right halves
    encrypted_bits = mergeBlocks(rightBlock, leftBlock)

    # return the encrypted block as a BitVector
    return encrypted_bits

def shift_left(key, shift):
    return key << shift


ROUND_KEY_SHIFT = [
                  1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1
              ]


PERMUTATION_TABLE = [
                        13, 16, 10, 23, 0,  4,  2,  27,
                        14, 5,  20, 9,  22, 18, 11, 3,
                        25, 7,  15, 6,  26, 19, 12, 1,
                        40, 51, 30, 36, 46, 54, 29, 39,
                        50, 44, 32, 47, 43, 48, 38, 55,
                        33, 52, 45, 41, 49, 35, 28, 31
                    ]


def roundKeyGenerator(encryption_key):

    round_keys = []
    key = encryption_key.deep_copy()
    for round_count in range(2):
        left_key, right_key = key[:28], key[28:]
        shift = ROUND_KEY_SHIFT[round_count]
        left_key = shift_left(left_key, shift)
        right_key = shift_left(right_key, shift)
        key = mergeBlocks(left_key, right_key)
        round_key = permuteBitvector(key, PERMUTATION_TABLE, False)
        round_keys.append(round_key)
    return round_keys

def chunkifyFile(filename):
    bitvector_list = []
    with open(filename, "rb") as file:
        file_contents = file.read()
        bv = BitVector(bitstring=''.join(format(byte, '08b') for byte in file_contents))
        bv_len = bv.length()
        for i in range(0, bv_len, 64):
            if i + 64 > bv_len:
                bitvector_chunk = bv[i:bv_len]
                padding_len = 64 - bitvector_chunk.length()
                bitvector_chunk.pad_from_right(padding_len)
            else:
                bitvector_chunk = bv[i:i+64]
            bitvector_list.append(bitvector_chunk)    
    return bitvector_list



INVERSE_SBOX = [[ [28,1,  62, 59],    [6, 15, 34, 45],    [8, 11, 44, 39],    [16,29, 56, 53] ,
                  [2, 7,  32, 41],    [24,27, 60, 49],    [20,19, 42, 61],    [30,5,  54, 47] ,
                  [14,31, 38, 37],    [26,25, 52, 43],    [18,17, 58, 57],    [12,23, 46, 51] ,
                  [22,21, 50, 35],    [4, 13, 40, 63],    [0, 9,  36, 55],    [10,3,  48, 33]],
                [ [26,19, 32, 57],    [2, 21, 46, 39],    [20,11, 60, 47],    [12,1,  58, 41] ,
                  [14,5,  42, 45],    [28,31, 48, 59],    [8, 25, 54, 51],    [18,7,  36, 53] ,
                  [4, 13, 50, 35],    [16,27, 56, 63],    [30,23, 40, 37],    [10,29, 38, 49] ,
                  [24,17, 52, 55],    [22,3,  44, 33],    [6, 15, 34, 61],    [0, 9,  62, 43]],
                [ [2, 5,  46, 39],    [16,31, 50, 33],    [28,17, 52, 61],    [10,9,  44, 55] ,
                  [26,11, 36, 49],    [14,21, 56, 59],    [8, 13, 34, 41],    [22,3,  62, 47] ,
                  [30,19, 40, 45],    [4, 7,  38, 43],    [0, 15, 58, 35],    [24,27, 48, 57] ,
                  [20,25, 54, 63],    [18,1,  32, 37],    [6, 23, 60, 53],    [12,29, 42, 51]],
                [ [8, 13, 38, 37],    [16,25, 50, 43],    [18,21, 58, 61],    [6, 15, 52, 33] ,
                  [28,17, 62, 51],    [22,7,  56, 53],    [10,9,  34, 39],    [0, 19, 44, 59] ,
                  [20,3,  60, 47],    [12,31, 36, 49],    [14,27, 32, 41],    [24,5,  42, 55] ,
                  [26,23, 40, 57],    [2, 1,  46, 45],    [4, 29, 54, 63],    [30,11, 48, 35]],
                [ [26,19, 60, 53],    [6, 15, 36, 41],    [0, 5,  34, 45],    [20,25, 58, 63] ,
                  [4, 9,  32, 59],    [18,17, 54, 61],    [14,31, 56, 49],    [8, 11, 44, 39] ,
                  [16,29, 46, 35],    [30,27, 50, 55],    [10,23, 40, 57],    [12,3,  38, 33] ,
                  [2, 7,  52, 37],    [24,13, 42, 47],    [28,1,  62, 43],    [22,21, 48, 51]],
                [ [16,25, 50, 59],    [2, 19, 56, 53],    [10,7,  40, 37],    [20,29, 46, 35] ,
                  [22,5,  52, 33],    [28,15, 38, 43],    [12,17, 62, 57],    [26,9,  48, 55] ,
                  [14,31, 42, 61],    [8, 13, 32, 41],    [4, 1,  54, 47],    [30,27, 60, 49] ,
                  [0, 11, 44, 39],    [18,21, 58, 63],    [24,23, 34, 51],    [6, 3,  36, 45]],
                [ [10,3,  56, 53],    [30,13, 32, 41],    [4, 25, 62, 59],    [16,19, 42, 61] ,
                  [0, 9,  34, 43],    [24,21, 58, 51],    [28,31, 52, 33],    [22,7,  44, 47] ,
                  [12,29, 54, 39],    [20,11, 60, 49],    [26,15, 48, 45],    [2, 5,  36, 35] ,
                  [18,23, 40, 63],    [14,1,  38, 37],    [6, 17, 46, 57],    [8, 27, 50, 55]],
                [ [26,25, 48, 55],    [14,1,  38, 35],    [2, 31, 46, 33],    [20,11, 58, 57] ,
                  [6, 15, 36, 41],    [24,19, 60, 59],    [8, 21, 50, 61],    [30,13, 32, 39] ,
                  [4, 7,  62, 45],    [18,29, 40, 53],    [16,9,  52, 43],    [12,23, 34, 63] ,
                  [28,17, 42, 51],    [0, 5,  54, 47],    [22,27, 44, 37],    [10,3,  56, 49]]]


def sBoxInvertor(sbox_out):
    segments = [sbox_out[x * 4: x * 4 + 4] for x in range(8)]
    pos = [INVERSE_SBOX[sindex][int(segment)] for sindex, segment in enumerate(segments)]

    def generate_inputs(pos, current_input=BitVector(size=0)):
        if not pos:
            yield current_input
            return
        for i in pos[0]:
            yield from generate_inputs(pos[1:], current_input + BitVector(intVal=i, size=6))

    return list(generate_inputs(pos))

XOR_MASK = []
AND_MASK = []

def keyMaskCheck(sboxlist, exp_inp, roundnumber):
    xor_temp = XOR_MASK[roundnumber]
    and_temp = AND_MASK[roundnumber]
    return [str(i ^ exp_inp) for i in sboxlist if not int(((i ^ exp_inp) ^ xor_temp) & and_temp)]

def positionBitmask(positions, key):
    """
    Create a bitmask from `key` based on the position values in `positions`.
    """
    permuted_pos = {PERMUTATION_TABLE.index(i): key[PERMUTATION_TABLE.index(i)] for i in positions}
    xorm = BitVector(bitlist=[permuted_pos.get(i, 0) for i in range(48)])
    andm = BitVector(bitlist=[1 if i in permuted_pos else 0 for i in range(48)])
    XOR_MASK.append(xorm)
    AND_MASK.append(andm)

def main():
    ENCRYPTED_FILE = 'target_ciphertext_p3.txt'
    DECRYPTED_FILE  = 'des_plaintext_p3.txt'

    if os.path.isfile(DECRYPTED_FILE):
        os.remove(DECRYPTED_FILE)
    
    print(f"\n{bcolors.BOLD}{bcolors.HEADER}FINDING ROUND KEYS ...{bcolors.ENDC}")
    
    plainblocks = chunkifyFile("sample_plaintext_p3.txt")
    cipherblocks = chunkifyFile("sample_ciphertext_p3.txt")

    partial_key = "000000a" # we know the last character is "a"
    partial_key_bv = BitVector(textstring = partial_key)
    partial_round_keys = roundKeyGenerator(partial_key_bv)
    positions = [46,47,48,49,50,51,52,54]
    positionBitmask(positions[-7:],partial_round_keys[0])
    positionBitmask(positions[:7],partial_round_keys[1])

    rkey = {i: [] for i in range(2)}

    BAR = 100
    BAR_PROGRESS = 0
    for plaintext, ciphertext in zip(plainblocks, cipherblocks):
        BAR_PROGRESS = BAR_PROGRESS+1
        updateProgressBar(BAR, BAR_PROGRESS)

        plain_length = plaintext.length()
        cipher_length = ciphertext.length()

        plain_length = plain_length // 2
        cipher_length = cipher_length // 2

        plain_left = plaintext[0:plain_length]
        plain_right = plaintext[plain_length:]

        cipher_left = ciphertext[0:cipher_length]
        cipher_right = ciphertext[cipher_length:]

        round1Input, round2Input = plain_right, cipher_right
        round1Output = plain_left ^ cipher_right
        round2Output = plain_right ^ cipher_left

        expand_round1Input = permuteBitvector(round1Input, EXPANSION_PERMUTATION_TABLE, False)
        expand_round2Input = permuteBitvector(round2Input, EXPANSION_PERMUTATION_TABLE, False)
        round1Output_b4pbox = permuteBitvector(round1Output, PERMUTATION_BOX, True)
        round2Output_b4pbox = permuteBitvector(round2Output, PERMUTATION_BOX, True)

        inverse_sbox_r1 = sBoxInvertor(round1Output_b4pbox)
        BAR_PROGRESS = BAR_PROGRESS+5
        updateProgressBar(BAR, BAR_PROGRESS)
        # print("inverse done 1")
        inverse_sbox_r2 = sBoxInvertor(round2Output_b4pbox)
        BAR_PROGRESS = BAR_PROGRESS+5
        updateProgressBar(BAR, BAR_PROGRESS)
        # print("inverse done 2")
        possible_keys_r1 = keyMaskCheck(inverse_sbox_r1,expand_round1Input,0)
        BAR_PROGRESS = BAR_PROGRESS+7
        updateProgressBar(BAR, BAR_PROGRESS)
        # print("possible keys done 1")
        possible_keys_r2 = keyMaskCheck(inverse_sbox_r2,expand_round2Input,1)
        BAR_PROGRESS = BAR_PROGRESS+7
        updateProgressBar(BAR, BAR_PROGRESS)
        # print("possible keys done 2")
        rkey[0] = list(set(rkey[0]) & set(possible_keys_r1)) if len(rkey[0]) != 0 else list(set(possible_keys_r1) & set(possible_keys_r1))
        rkey[1] = list(set(rkey[1]) & set(possible_keys_r2)) if len(rkey[1]) != 0 else list(set(possible_keys_r2) & set(possible_keys_r2))

        key1Length = len(rkey[0])
        key2Length = len(rkey[1])

        #we stop when we narrow down to 1 key per round
        if key1Length == key2Length == 1:
          break
        
    if len(rkey[0]) > 1 and len(rkey[1]) > 1:
        print("More than one possibility for round key found")
    # print(rkey[0])
    # print(rkey[1])
    encryption_round_keys = [BitVector(bitstring = rkey[0][0]), BitVector(bitstring=rkey[1][0])]

    print("\nDECRYPTING TARGET CIPHER TEXT....")
    encryption_round_keys = encryption_round_keys[::-1]

    with open(DECRYPTED_FILE, 'ab') as FILE_OUT:
      with open(ENCRYPTED_FILE, 'rb') as FILE_IN:
        file_contents = FILE_IN.read()
        bv = BitVector(bitstring=''.join(format(byte, '08b') for byte in file_contents))
        bv_len = bv.length()
        for i in range(0, bv_len, 64):
            if i + 64 > bv_len:
                bitvector_chunk = bv[i:bv_len]
                padding_len = 64 - bitvector_chunk.length()
                bitvector_chunk.pad_from_right(padding_len)
            else:
                bitvector_chunk = bv[i:i+64]
            bv_decoded = decoder(encryption_round_keys, bitvector_chunk)
            bv_decoded.write_to_file(FILE_OUT)

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}\nDecoded plaintext written to file {DECRYPTED_FILE} {bcolors.ENDC}")


main()