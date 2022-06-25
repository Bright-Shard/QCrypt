# QCrypt
*Quantum encryption on classical computers.*

**NOTE:** QCrypt was written by a board 15-year-old (that's me! :D) in 2-3 days for a summer camp. It's a proof-of-concept, please don't actually try to rely on this for security.

**NOTE 2:** If you're lost, there's a definitions section at the bottom that might help :P

### About QCrypt

QCrypt uses IBM Quantum to encrypt and decrypt text on a quantum computer or emulator, then sends the result back to your classical machine. This essentially allows for a lower-quality form of quantum encryption to run on classical machines!

Even if you don't have access to IMB-Q, you can still run QCrypt with a quantum emulator, which basically pretends to be a quantum computer. However, this can take a lot of compute resources (see the performance section below).

### How QCrypt Works

QCrypt uses what I'm naming a half-key system: essentially, the key can only encrypt/decrypt half of a message. The other half uses quantum entanglement to encrypt/decrypt a message. This effectively means that, when implemented correctly, the half-key system ensures that a key can only decrypt half of an encrypted message!

### Flaws & Fixes

The most obvious flaw is QCrypt's reliance on entanglement. While this ensures anyone *without* a quantum computer/simulator can't decrypt a half-key message, essentially anyone who does have a quantum computer can, because all quantum computers have entanglement. To get around this, QCrypt adds a second transposition key (coming soon™) that tells the sender and receiver how to rearrange the message in a specific way. When the message is rearranged, it's impossible to tell which bits were formed with the key and which bits were formed with entanglement, ensuring the security of the half-key system.

TL;DR: QCrypt uses multiple keys instead of just one, so each key can only decrypt a portion of the message.

### Performance Notes

Quantum computers are still *very* new, and simulating them gets exponentially more costly for classical computers. Because of this, QCrypt only uses 2 qubits at a time, and then stores the results. Those two qubits are essentially reset and recycled over and over again during the encryption/decryption process. This lessens computational requirements, but probably makes QCrypt slower, so in the future support will be added to specify the max number of qubits QCrypt can use.

# Definitions
**Quantum vs classical computers:**

Quantum computers use quantum physics and a bunch of fancy math to make a new generation of computers - computers *much* more powerful than the ones we have today. The computers we have today - which (mostly) rely on classical physics instead of quantum physics - are called classical computers.

**Qubits:**

Similarly to how classical computers use 0s/1s in the form of bits to process information, quantum computers use qubits to process information. However, due to some weird rules in quantum physics, qubits can exist in a state in between 0 and 1 - allowing them to process more information at once.

**Entanglement:**

Another weird rule of quantum mechanics, entanglement creates relationships between qubits. You can measure the state of one qubit (0 or 1) depending on the state of another qubit that is entangled to it. This creates a new kind of logic gate (which is how QCrypt uses entanglement), but it can also allow quantum computers to process information twice as fast by performing calculations on two entangled qubits at once!
