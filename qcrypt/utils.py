from qcrypt.datatypes import QCryptMessage, QCryptKey


# Half of the data is encrypted via XORing the data with the key
def xor_msg(key: QCryptKey, msg: QCryptMessage) -> bin:
    # Ensure the key is the right length
    key.resize_from_msg(msg)

    # XOR the key by the first half of the data
    xor: bin = bin(int(key.resized_value(), 2) ^ int(msg.half_one(), 2))
    # Format the xor variable so it reads like proper binary
    xor: bin = xor[2:].zfill(key.resized_length())

    return xor


# Transform binary to unicode text
def bin_to_text(binary: bin) -> str:
    # Special thanks: https://stackoverflow.com/a/40559005
    return ''.join(chr(int(binary[i*8:i*8+8], 2)) for i in range(len(binary) // 8))
