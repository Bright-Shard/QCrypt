import qcrypt.gen_key
import qcrypt.utils
from qcrypt.datatypes import QCryptMessage, QCryptKey
from qcrypt.circuit import QCryptCircuit


class QCrypt:
    # CONSTRUCTOR
    def __init__(self, api_key: str, server: str, *args, use_ibmq: bool = True) -> None:
        # Message, key, and whether to use IBMQ or a simulator
        self.message: QCryptMessage = QCryptMessage()
        self.key: QCryptKey = QCryptKey()
        self.use_ibmq: bool = use_ibmq

        # The quantum circuit for entanglement
        self.circuit = QCryptCircuit()

    # MESSAGE/KEY OVERRIDE
    def set_message(self, new_message, *args, binary: bool = False):
        self.message.set(new_message) if not binary else self.message.set_bin(new_message)

    def set_key(self, new_key, *args, binary: bool = False):
        self.key.set(new_key) if not binary else self.key.set_bin(new_key)

    # ENCRYPTION
    def encrypt(self) -> bin:
        print("\n------------\n------------\nENCRYPTING MESSAGE\n------------\n------------\n")

        # Init variables
        ciphertext: bin = ""
        newkey: bin = self.key.resize_from_msg(self.message)

        # Entangle the second half of the data based off of the raw, un-XORed data's first half
        print("Starting quantum entanglement...")
        ciphertext += self.circuit.run(self.message.half_one(), self.message.half_two())
        print("Done.")

        # XOR the first half of the data
        print("Starting XOR operation...")
        xor: bin = utils.xor_msg(self.key, self.message)
        ciphertext = xor + ciphertext
        print("Done.")

        print(f"------\nKEY: {newkey} ({len(newkey)} bits)\n" +
              f"MSG: {self.message.half_one()} ({self.message.len_half()} bits)\n" +
              f"XOR: {xor} ({len(xor)} bits)\n" +
              f"CIPHER BITS: {ciphertext} ({len(ciphertext)} bits)\n------")
        return ciphertext

    # DECRYPTION
    def decrypt(self) -> str:
        print("------------\n------------\nDECRYPTING MESSAGE\n------------\n------------\n")

        # Init variables
        plaintext_bin: bin = ""
        newkey: bin = self.key.resize_from_msg(self.message)

        # XOR the first half of the data
        print("Starting XOR operation...")
        xor: bin = utils.xor_msg(self.key, self.message)
        plaintext_bin += xor
        print("Done.")

        # Entangle the second half of the data
        print("Starting quantum entanglement...")
        plaintext_bin += self.circuit.run(xor, self.message.half_two())
        print("Done.")

        print("Converting binary to text...")
        plaintext: str = utils.bin_to_text(plaintext_bin)
        print("Done.")

        print(f"------\nKEY: {newkey} ({len(newkey)} bits)\n" +
              f"MSG: {self.message.half_one()} ({self.message.len_half()} bits)\n" +
              f"XOR: {xor} ({len(xor)} bits)\n" +
              f"PLAINTEXT: {plaintext} ({len(plaintext)} chars)\n"
              f"PLAINTEXT BITS: {plaintext_bin} ({len(plaintext_bin)} bits)\n------")

        return plaintext
