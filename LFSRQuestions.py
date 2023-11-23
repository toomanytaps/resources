import random
from functools import reduce


# Q4 Linear Feedback Shift Register
# A LFSR generates a pseudo random stream of bits that repeat at some known time. This can then be used to synchronise
# clocks and spread a signal across a bandwidth (which reduces errors)

# Program a LFSR. Your program should take in the order of the LFSR (how many shifts there are) and where the taps
# are (i.e some representation of the polynomial). Your program should output the linear recursive sequence generated
# by the LFSR, and the number of recursions that it took to generate the sequence.


class LFSR:
    def __init__(self, num_stages, taps_list, fill):
        """
        Initialise the LFSR
        :param stages: Int, the number of stages
        :param taps: A list of the tap points. The number should be the polynomial order and don't include the 0
        (e.g x**4 + x + 1 = [4, 1])
        :param fill: String, how the stages should be filled. Options are 'ones', 'random', or you can enter
        a custom binary string (e.g. '10110') and that will be filled into the stages. If the custom string is too
        long it will be trimmed, if it's too short it raises an error
        """
        self.num_stages = num_stages
        self.taps = [i-1 for i in taps_list]

        self.stages = []
        self.fill_stages(fill=fill)

        # Start the sequence off with the stage fill
        self.sequence = self.stages.copy()

        # The fingerprint below is used to look for repetition of the output sequence
        self.fingerprint = self.sequence.copy()
        self.repeat = False

    def fill_stages(self, fill='ones'):
        """
        Fill the stages with ones, random bits, or a custom sting
        :param fill: string, 'ones', 'random', or a custom binary string e.g. '10001010'
        """
        # Ones and random fills
        if fill == 'ones' or fill == 'random':
            for i in range(self.num_stages):
                if fill == 'ones':
                    self.stages += [1]
                elif fill == 'random':
                    self.stages += [random.randint(0, 1)]

        # Custom fill
        else:
            if len(fill) < self.num_stages:
                raise ValueError("fill must be 'ones', 'random', or a binary string with length"
                                 " >= the number of stages")

            for i in range(self.num_stages):
                fill_num = int(fill[i])
                self.stages += [fill_num]

    def xor_taps(self):
        """
        Performs an XOR function on the current tap values
        """
        values = [self.stages[i] for i in self.taps]
        out = reduce(lambda i, j: int(i) ^ int(j), values)

        return out

    def cycle(self):
        """
        Cycles the LSFR one step
        """
        # Xor the tap outputs to produce the new input to the system and the next digit in the sequence
        new_input = self.xor_taps()
        self.sequence += [new_input]

        # Insert the new input and shuffle the numbers through the register
        self.stages.insert(0, new_input)
        self.stages = self.stages[:-1]

        # Check for repetition
        self.check_repeat()

    def check_repeat(self):
        """
        Checks to see if the LSR has repeated
        """
        # Pass the first time
        if len(self.sequence) == len(self.fingerprint):
            pass

        # Create the check region as the last n bits of the sequence
        check_region = self.sequence[-1*self.num_stages:]
        # See if the check region is the fingerprint
        if check_region == self.fingerprint:
            self.repeat = True

    def run_lfsr(self, print_output=True, cycles=None):
        """
        Cycles the LFSR until it repeats or if cycles are given until that number is reached
        """
        max_cycles = 100000000000000000000

        for i in range(max_cycles): # just do a big number
            # if (i % 10000000) == 0:
            #     print(f"On cycle {i}")

            self.cycle()
            if print_output:
                self.print_state()

            if cycles:
                if i >= cycles:
                    break

            if self.repeat:
                self.sequence = self.sequence[:-len(self.fingerprint)]
                s_print = ''.join([str(i) for i in self.sequence])
                f_print = ''.join([str(i) for i in self.fingerprint])
                print(f"Sequence has repeated!\nSequence:{s_print}\nFingerprint:{f_print}")
                print(f"The sequence length for this LFSR is {len(self.sequence)}")
                break

    def print_state(self):
        print(self.sequence)
        print(self.fingerprint)
        print(self.num_stages)


# lfsr = LFSR(16, [16, 14, 13, 11], fill='ones')
# lfsr.run_lfsr(print_output=False)


# Q4b - EXTENSION
# A LSFR with 8 registers was initially seeded with 1's. It produced the following sequence:

# 1111111100001011110001101000000010001110001001011100000011001001001101110010000010101101101011001011000011111011011
# 1101011101000100001101100011110011100110001011010010001010010101001110111011001111011111101001100110101000110000011
# 1010101011111001010000100


# Where were the taps placed?

# Answer
# lfsr = LFSR(8, [8, 6, 5, 4], fill='ones')
# lfsr.run_lfsr(print_output=False)

# Q4c - EXTENSION
# The maximum sequence length is given by (2**n)-1, where n is the number of registers.
# Starting with a register length of 3, find the tap positions which give the maximum length sequence.
# Once that is found increase the number of registers to 4. How high can you go?

# Solution






