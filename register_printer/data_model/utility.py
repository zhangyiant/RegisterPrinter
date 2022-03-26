import math


def msb_to_bytes(msb):
    num_of_bytes = msb // 8 + 1
    return 2 ** math.ceil(math.log(num_of_bytes, 2))
