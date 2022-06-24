import math


class QCryptMessage:
    def __init__(self, message: str = "Hello, world!", *args, use_raw_length: bool = False) -> None:
        if not use_raw_length:
            self.__message: str = message
            self.__length: int = len(self.bytes())
            self.__half: int = math.floor(self.__length / 2)
        else:
            self.__message: str = message
            self.__length: int = len(message)
            self.__half: int = math.floor(self.__length / 2)

    def message_raw(self) -> str:
        return self.__message

    def bytes(self) -> str:
        return ''.join(format(ord(i), '08b') for i in self.__message)

    def len(self) -> int:
        return self.__length

    def len_half(self) -> int:
        return self.__half
