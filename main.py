import os
from dotenv import load_dotenv
from qcrypt import QCrypt
load_dotenv()

qcrypt: QCrypt = QCrypt(5, os.getenv("IBM_KEY"), "server_name", use_ibmq=False)

print("------")
print(f"KEY: |{qcrypt.get_key()}| ({len(qcrypt.get_key())} chars)")
print(f"|{qcrypt.get_key_binary()}| ({len(qcrypt.get_key_binary())} bits)")
print("------")
print(f"MESSAGE: |{qcrypt.get_message()}| ({len(qcrypt.get_message())} chars)")
print(f"|{qcrypt.get_message_binary()}| ({len(qcrypt.get_message_binary())} bits)")
print("------")
qcrypt.set_message(qcrypt.encrypt(), use_raw_length=True)
qcrypt.decrypt()
