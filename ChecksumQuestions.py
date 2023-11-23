import random
random.seed(1234) # Don't change this


# **********************************************************************************************************************


# Q1a
# Create a function which computes the bitwise AND of two binary strings of the same length. This functions looks at
# each bit from two strings and returns a 1 if they are both 1, and a 0 otherwise. The output should be a single string.
# For example. perfoming '1110' AND '0011' = '0010'


# Solution
def bin_and(s1, s2):
    out = ''

    for i in range(len(s1)):
        if s1[i] == "1" and s2[i] == "1":
            out += "1"
        else:
            out += "0"

    return out


# Faster solution
def better_bin_and(s1, s2):
    # Convert to decimal and perform the and
    out = int(s1, 2) & int(s2, 2)
    # Convert back to binary and trim
    out = bin(out)[2:]
    # Pad to original length (because converting to binary trims leading 0s)
    out = '0' * (len(s1) - len(out)) + out

    return out


# **********************************************************************************************************************


# Q1b
# Create a function which computes the bitwise XOR of two binary strings of the same length. XOR returns a 1 if the
# bits are different, and a 0 if the bits are the same.
# For example, '1110' XOR '0010' = '1100'


# Solution
def bin_xor(s1, s2):
    out = ''

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            out += "1"
        else:
            out += "0"

    return out


# Another solution
def better_xor(s1, s2):
    # ^ is actually the XOR operator, so this performs bitwise XOR of the binary strings s1 and s2 in
    # a list comprehension
    out = [int(s1[i]) ^ int(s2[i]) for i in range(len(s1))]
    # Convert from list to string
    out = ''.join([str(i) for i in out])
    return out


# **********************************************************************************************************************


# Q1c
# Create a function which performs binary addition on two strings of the same length. If the resulting string is longer
# than the initial strings, cut off the extra digit that is created (i.e. drop the carry).
# E.g
# '1110'    +
# '0010'    =
# '10000'
# However the output string is longer than the input, so we drop the new digit and return '0000'

# Solution
# This solution steps through the addition as a human would do it
def bin_add(s1, s2):
    out = [0 for i in s1] # A list of zeroes the same length as s1
    carry = [0 for i in s1] + [0] # Add an extra zero for the carry (incase we carry into it!)

    # Reverse s1 and s2 to make addition easier
    s1_rev = s1[::-1]
    s2_rev = s2[::-1]

    for i in range(len(s1_rev)):
        x = int(s1_rev[i]) + int(s2_rev[i]) + int(carry[i])

        if x > 2:
            carry[i+1] = x - 2
            out[i] = x % 2
        elif x == 2:
            carry[i+1] = 1
            out[i] = 0
        elif x == 1:
            out[i] = 1
        elif x == 0:
            out[i] = 0

    # Convert the output to a string
    out = ''.join([str(i) for i in out])
    # reverse the output (because we reversed the input!)
    out = out[::-1]

    return out


# Much much easier solution converting to decimal
def better_bin_add(s1, s2):
    # Convert to decimal
    a = int(s1, 2)
    b = int(s2, 2)

    # Perform the addition and convert back to binary
    out = bin(a + b)
    # Get rid of the '0b' at the start to preserve our representation
    out = out[2:]

    # cutoff the overflow
    length_difference = len(out) - len(s1)
    out = out[length_difference:]

    return out


# **********************************************************************************************************************


# Q2
# Use your solutions from Q1 to code the longitudinal redundancy check (aka parity byte checksum). This is
# a single byte which is added to the end of a frame of data which can be used to identify if an error has occured in
# the sequence. The pseudo code for the LRC (as defined in ISO-1155) is below:

#     lrc := 0
#     for each byte b in the buffer do
#         lrc := (lrc + b) and 0xFF
#     lrc := (((lrc XOR 0xFF) + 1) and 0xFF)

# Note that 0xFF is simply '11111111' in hex. Your function should only use binary and not hex, this is simply how it
# is written in the ISO.

# Check your solution on the following data. The parity byte that you calculate should be '01110110'


def make_data(n=10000):
    out = []
    for i in range(n):
        byte = ""

        for j in range(8):
            byte += str(random.randint(0, 1))

        out += [byte]

    return out


# Solution
def LRC(data):
    lrc = '00000000'
    # 0xFF = 255 = '11111111'
    ones = '11111111'

    for byte in data:
        lrc = bin_add(lrc, byte)
        lrc = bin_and(lrc, ones)

    lrc = bin_xor(lrc, ones)
    lrc = bin_add(lrc, '00000001')
    lrc = bin_and(lrc, ones)

    return lrc


dataset = make_data()
lrc = LRC(dataset)


# **********************************************************************************************************************


# Q3a
# Next we're going to implement the basic checksum
# This checksum works by splitting the frame of data into bytes and then performing binary addition of those bytes
# to create a checksum. Basic checksum also introduces an idea called end around carry.
#
# In Q1c we performed binary addition, and if the sum of the two binary numbers was a binary number with a longer
# length, we simply dropped the extra digit. In practice this still works however we are discarding information about
# the data we are transmitting. Instead what we might do is perform end around carry on that digit.

# End around carry is simply where you take the extra bit and move it to the initial column of a new binary string. From
# there the string is summed back in.
# E.G, length of 4
#  1111 +
#  1001 =
# 11000
# 11000 is longer than our length of four, so we wrap the first digit back around and add it in:
# 1000 +
# 0001 =
# 1001
# If you have more than one extra digit, wrap them both around (so 111000 would go to 1000 + 0011
# where 0011 is the wrap)

# Rewrite your binary addition function from Q1c to include end around carry
# Solution
# This is a painful but "honest" way, a less painful way is just to swap it to decimal!
def bin_add_carry(s1, s2):
    out = [0 for i in s1] # A list of zeroes the same length as s1
    carry = [0 for i in s1] + [0, 0] # I think two units is the max carry possible. it might be 1 though

    # Reverse s1 and s2 to make addition easier
    s1_rev = s1[::-1]
    s2_rev = s2[::-1]

    for i in range(len(s1_rev)):
        x = int(s1_rev[i]) + int(s2_rev[i]) + int(carry[i])

        if x > 2:
            carry[i+1] = x - 2
            out[i] = x % 2
        elif x == 2:
            carry[i+1] = 1
            out[i] = 0
        elif x == 1:
            out[i] = 1
        elif x == 0:
            out[i] = 0

    # so now we need to wrap the carry around and add it back in
    # We take the last two digits of the carry and reverse them and pad that out with zeroes
    wrap = [0] * (len(s1)-2) + carry[-2:][::-1]
    wrap = wrap[::-1] # reverse the wrap

    while sum(wrap) > 0:
        carry = [0 for i in s1] + [0, 0] # reset the carry

        # Add the out and the wrap
        for i in range(len(out)):
            x = int(out[i]) + int(wrap[i]) + int(carry[i])

            if x > 2:
                carry[i + 1] = x - 2
                out[i] = x % 2
            elif x == 2:
                carry[i + 1] = 1
                out[i] = 0
            elif x == 1:
                out[i] = 1
            elif x == 0:
                out[i] = 0

        # Recalc the wrap
        wrap = [0] * (len(s1) - 2) + carry[-2:][::-1]
        wrap = wrap[::-1]  # reverse the wrap

    # Convert the output to a string
    out = ''.join([str(i) for i in out])
    # reverse the output (because we reversed the input!)
    out = out[::-1]

    return out


# Much easier solution converting to decimal
def better_bin_add_carry(s1, s2):
    # Convert to decimal
    a = int(s1, 2)
    b = int(s2, 2)

    # Perform the addition and convert back to binary
    out = bin(a + b)
    # Get rid of the '0b' at the start to preserve our representation
    out = out[2:]

    # Now we need to wrap the overflow and add it back in
    while len(out) > len(s1):
        length_diff = len(out) - len(s1)
        wrap = out[:length_diff]
        out = out[length_diff:]

        # Add wrap and out together
        # Convert to decimal
        a = int(wrap, 2)
        b = int(out, 2)

        # Perform the addition and convert back to binary
        out = bin(a + b)
        # Get rid of the '0b' at the start to preserve our representation
        out = out[2:]

    return out


# **********************************************************************************************************************


# Q3b Time to implement the basic checksum! The way the basic checksum works, is it simply performs binary addition
# on fixed lengths of the data and is then attached to the end of the data frame. Similar to Q2, you will be given
# N bytes of data. Use your solution from Q3a to calculate the basic checksum for these bytes!

datasetq3 = make_data(20000)

# Solution
def basic_checksum(data):
    out = None

    for byte in data:
        if not out:
            out = byte
        else:
            out = bin_add_carry(out, byte)

    return out


basic_cs = basic_checksum(datasetq3)


# **********************************************************************************************************************


# Q3c - Ones Complement
# The Ones complement is simply the inverse of the basic checksum. It takes the basic checksum and changes and 1 into
# a 0, and any 0 into a 1. Write this function and apply it to your answer from Q3b
# Solution
def ones_complement(checksum):
    """
    Inverts a checksum (a binary string)
    :param check_sum: A binary string used to check the integrity of a frame of data e.g, the basic checksum
    :return: The Ones Complement checksum
    """
    ones = ''
    for letter in checksum:
        if letter == '1':
            ones += "0"

        elif letter == "0":
            ones += "1"

        else:
            raise ValueError("Input must be binary")

    return ones


ones_comp = ones_complement(basic_cs)


# **********************************************************************************************************************


# Q3d - Twos Complement
# The Twos Complement takes the Ones Complement as input and adds a single bit to it.
# You may want to use your binary addtiion function from Q3a
# e.g. '1001' +
#      '0001' =
#      '1010'

# Write this FUNction!
# Solution
def twos_complement(ones):
    """
    Calculates the Twos Complement of a Ones Complement checksum. The Twos Complement is found by adding a single
    bit to the Ones Complement. e.g. '0010' + '0001' = '0011'. When the twos_complement is added to a basic checksum
    the result will be all 0s unless the original data has been corrupted
    :param ones: The Ones Complement of a basic checksum
    :return: The Twos Complement
    """
    N = len(ones)
    complement = ones + '0' * (N-1) + '1'

    twos = bin_add_carry(complement, ones)

    return twos












