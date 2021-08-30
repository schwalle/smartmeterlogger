
from src.detail.helper import create_hex_dump

def test_hexdump():
    result = create_hex_dump(b'123456789abcdefghijklmnopqrstuvxyz')
    assert(result == """0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x61 0x62 0x63 0x64 0x65 0x66 0x67
0x68 0x69 0x6A 0x6B 0x6C 0x6D 0x6E 0x6F 0x70 0x71 0x72 0x73 0x74 0x75 0x76 0x78
0x79 0x7A""")
