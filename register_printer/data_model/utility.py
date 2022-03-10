
import math

def msb_to_bytes(msb):
    bytes = msb // 8 + 1
    return 2 ** math.ceil(math.log(bytes, 2))
