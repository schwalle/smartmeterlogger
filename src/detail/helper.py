

import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def create_hex_dump(data: bytes, colums = 16) -> str:
    numbytes = len(data)
    result = ''
    i = 0
    while i + colums < numbytes:
        result+=(' '.join(f'0x{b:02X}' for b in data[i:i+colums])) + '\n'
        i+=colums
    
    if i < numbytes:
        result += (' '.join(f'0x{b:02X}' for b in data[i:]))

    return result
