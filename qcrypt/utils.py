import math
from qcrypt.key import QCryptKey
from qcrypt.message import QCryptMessage


def size_key(key: QCryptKey, msg: QCryptMessage) -> bin:
    print(f"MSG BINARY SIZE: {msg.len()}\n   HALF: {msg.len_half()}")

    if key.len() > msg.len_half():
        newkey: str = key.bytes()[:msg.len_half()]
    else:
        remainder: int = msg.len_half() % key.len()
        #print(f"REMAINDER: {remainder}")
        multiple: int = math.floor(msg.len_half() / key.len())
        #print(f"MULTIPLE: {multiple}")
        newkey: str = (key.bytes() * multiple) + \
                      (key.bytes()[:remainder] if remainder > 0 else "")

    print(f"OLD KEY SIZE: {key.len()}\n   NEW SIZE: {len(newkey)}\nOLD KEY: {key.bytes()}\n   NEW KEY: {newkey}")
    return newkey
