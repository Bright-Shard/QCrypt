import os
from dotenv import load_dotenv
from qcrypt import QCrypt
load_dotenv()

qcrypt: QCrypt = QCrypt(5, os.getenv("IBM_KEY"), "server_name", use_ibmq=False)

print("------")
print(f"KEY: |{qcrypt.key.data()}| ({qcrypt.key.len()} chars)")
print("------")
print(f"MESSAGE: |{qcrypt.message.data()}| ({qcrypt.message.len()} chars)")
print("------")

encrypted_msg: str = qcrypt.encrypt()
qcrypt.set_message(encrypted_msg, binary=True)

print("------")
print(f"KEY: |{qcrypt.key.data()}| ({qcrypt.key.len()} chars)")
print("------")
print(f"MESSAGE: |{qcrypt.message.data()}| ({qcrypt.message.len()} chars)")
print("------")

decrypted_msg: str = qcrypt.decrypt()
