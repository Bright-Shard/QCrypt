class QCryptKey:
    def __init__(self, key: str = "key", *args, use_raw_length: bool = False) -> None:
        if not use_raw_length:
            self.__key: str = key
            self.__length: int = len(self.bytes())
        else:
            self.__key: str = key
            self.__length: int = len(key)

    def key_raw(self) -> str:
        return self.__key

    def bytes(self) -> str:
        return ''.join(format(ord(i), '08b') for i in self.__key)

    def len(self) -> int:
        return self.__length
