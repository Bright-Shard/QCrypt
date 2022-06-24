import qiskit
import math
import qcrypt.gen_key
import qcrypt.utils
from qcrypt.key import QCryptKey
from qcrypt.message import QCryptMessage
from qiskit import QuantumCircuit, IBMQ, Aer, QuantumRegister, ClassicalRegister


class QCrypt:
    def __init__(self, qubits: int, api_key: str, server: str, *args, use_ibmq: bool = True) -> None:
        self.__message: QCryptMessage = QCryptMessage()
        self.__key: QCryptKey = QCryptKey()
        self.__circuit: QuantumCircuit = QuantumCircuit(qubits)
        self.use_ibmq = use_ibmq

        # The quantum circuit for entanglement
        self.qubits: QuantumRegister = QuantumRegister(2, "qubits")  # qubits[0] = cipherbit, qubits[1] = entanglebit
        self.bits: ClassicalRegister = ClassicalRegister(2, "bits")  # Same as above
        self.circuit: QuantumCircuit = QuantumCircuit(self.qubits, self.bits)  # The actual circuit
        self.runner = Aer.get_backend("qasm_simulator")  # Aer to run the program

        if use_ibmq:
            IBMQ.save_account(api_key)
            self.__backend = IBMQ.load_account().get_backend(server)

    # MESSAGE
    def set_message(self, new_message: str, *args, use_raw_length: bool = False) -> None:
        self.__message = QCryptMessage(new_message, use_raw_length=use_raw_length)

    def get_message(self) -> str:
        return self.__message.message_raw()

    def get_message_binary(self) -> str:
        return self.__message.bytes()

    # KEY
    def set_key(self, new_key: str, *args, use_raw_length: bool = False) -> None:
        self.__key = QCryptKey(new_key, use_raw_length=use_raw_length)

    def get_key(self) -> str:
        return self.__key.key_raw()

    def get_key_binary(self) -> str:
        return self.__key.bytes()

    # ENCRYPTION
    def encrypt(self) -> bin:
        print("\n------------\n------------\nENCRYPTING MESSAGE\n------------\n------------\n")
        # The key-encrypted part
        newkey: bin = utils.size_key(self.__key, self.__message)
        halfmsg: bin = self.__message.bytes()[:self.__message.len_half()]
        xor = int(newkey, 2) ^ int(halfmsg, 2)
        ciphertext: bin = bin(xor)[2:].zfill(len(newkey))

        # The entangled part
        #print("------\nENTANGLEMENT RESULTS:\n")
        for index in range(self.__message.len_half()):
            #print("Circuit iteration " + str(index))
            cipherbit: int = int(ciphertext[index])  # The XOR'd ciphertexts bit
            entanglebit: int = int(self.__message.bytes()[self.__message.len_half() + index])  # The not-XOR'd texts bit
            #print(cipherbit, entanglebit)

            # Make the qubit values reflect the cipherbit/entanglebit values
            if cipherbit == 1:
                self.circuit.x(self.qubits[1])
            if entanglebit == 1:
                self.circuit.x(self.qubits[0])
            # Entangle the qubits
            self.circuit.cx(self.qubits[1], self.qubits[0])
            # Measure the qubit states & store it in the classical register
            self.circuit.measure(self.qubits, self.bits)

            # Run
            execute = qiskit.execute(self.circuit, self.runner, shots=1200)
            resultsList: dict = dict(execute.result().get_counts())
            finalResult: dict = {"state": "", "chance": 0}
            for state in resultsList.keys():
                chance = resultsList[state]
                if int(chance) > finalResult["chance"]:
                    finalResult["state"] = state
                    finalResult["chance"] = chance

            #print(f"FINAL CIRCUIT RESULT: {finalResult}\nRAW RESULTS: {resultsList}\n")
            ciphertext += finalResult["state"][1]
            self.circuit.reset(self.qubits)  # Reset the quantum circuit

        print(f"------\nKEY: {newkey} ({len(newkey)} bits)\n" +
              f"MSG: {self.__message.bytes()[:self.__message.len_half()]} ({self.__message.len_half()} bits)\n" +
              f"XOR: {bin(xor)[2:].zfill(len(newkey))} ({len(bin(xor)[2:].zfill(len(newkey)))} bits)\n" +
              f"CIPHER: {ciphertext} ({len(ciphertext)} bits)\n------")
        return ciphertext

    # DECRYPTION
    def decrypt(self) -> str:
        print("------------\n------------\nDECRYPTING MESSAGE\n------------\n------------\n")
        # The key-encrypted part
        newkey: bin = utils.size_key(self.__key, self.__message)
        halfmsg: bin = self.__message.message_raw()[:self.__message.len_half()]
        xor = int(newkey, 2) ^ int(halfmsg, 2)
        plaintext: bin = bin(xor)[2:].zfill(len(newkey))

        # The entangled part
        #print("------\nENTANGLEMENT RUNNING\n")
        for index in range(self.__message.len_half()):
            #print("Circuit iteration " + str(index))
            cipherbit: int = int(plaintext[index])  # The XOR'd ciphertexts bit
            entanglebit: int = int(self.__message.message_raw()[self.__message.len_half() + index])  # The not-XOR'd texts bit
            #print(cipherbit, entanglebit)

            # Make the qubit values reflect the cipherbit/entanglebit values
            if cipherbit == 1:
                self.circuit.x(self.qubits[1])
            if entanglebit == 1:
                self.circuit.x(self.qubits[0])
            # Entangle the qubits
            self.circuit.cx(self.qubits[1], self.qubits[0])
            # Measure the qubit states & store it in the classical register
            self.circuit.measure(self.qubits, self.bits)

            # Run
            execute = qiskit.execute(self.circuit, self.runner, shots=1200)
            resultsList: dict = dict(execute.result().get_counts())
            finalResult: dict = {"state": "", "chance": 0}
            for state in resultsList.keys():
                chance = resultsList[state]
                if int(chance) > finalResult["chance"]:
                    finalResult["state"] = state
                    finalResult["chance"] = chance

            #print(f"FINAL CIRCUIT RESULT: {finalResult}\nRAW RESULTS: {resultsList}\n")
            plaintext += finalResult["state"][1]
            self.circuit.reset(self.qubits)  # Reset the quantum circuit

        # Change binary to text
        newText: str = ""
        for iterator in range(math.floor(len(plaintext) / 8)):
            newText += chr(int(plaintext[iterator:iterator + 7]))
        plaintext = newText

        print(f"------\nKEY: {newkey} ({len(newkey)} bits)\n" +
              f"MSG: {self.__message.message_raw()[:self.__message.len_half()]} ({self.__message.len_half()} bits)\n" +
              f"XOR: {bin(xor)[2:].zfill(len(newkey))} ({len(bin(xor)[2:].zfill(len(newkey)))} bits)\n" +
              f"PLAINTEXT: {plaintext} ({len(plaintext)} chars)\n------")

        return plaintext
