#!/usr/bin/env python3

# Reverse Caesar cipher with incremental shift
# Used to decode the SnowCrash level09 token

hex_string = "66 34 6b 6d 6d 36 70 7c 3d 82 7f 70 82 6e 83 82 44 42 83 44 75 7b 7f 8c 89"

hex_bytes = hex_string.split()
shift = 0
decoded = ""

for byte in hex_bytes:
    decimal = int(byte, 16) - shift  # reverse the shifting pattern
    # On s'assure que le caractère reste dans la plage ASCII imprimable
    decimal %= 256
    decoded += chr(decimal)
    shift += 1

print(decoded)
