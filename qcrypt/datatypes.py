import math


class QCryptData:
    def __init__(self, data: str) -> None:
        self.__data: bin = ""
        self.set(data)

    def set(self, new_data: str) -> None:
        self.__data = "".join(format(ord(i), "08b") for i in new_data)

    def set_bin(self, new_data: bin) -> None:
        self.__data = new_data

    def data(self) -> bin:
        return self.__data

    def len(self) -> int:
        return len(self.data())

    def len_half(self) -> int:
        return math.floor(len(self.data()) / 2)


class QCryptMessage(QCryptData):
    def __init__(self, msg: str = "Hello, world!") -> None:
        super().__init__(msg)

    def half_one(self) -> bin:
        return self.data()[:self.len_half()]

    def half_two(self) -> bin:
        return self.data()[self.len_half():]


class QCryptKey(QCryptData):
    def __init__(self, key: str = "$eCuR1k3Y") -> None:
        super().__init__(key)
        self.__resized_key: bin = self.data()

    def __matches_size(self, size: int) -> bool:
        if len(self.__resized_key) == size:
            return True
        else:
            return False

    def resized_value(self) -> bin:
        return self.__resized_key

    def resized_length(self) -> int:
        return len(self.__resized_key)

    def resize_from_msg(self, msg: QCryptMessage) -> bin:
        key_length: int = self.len()
        msg_half: int = msg.len_half()

        if self.__matches_size(msg_half):
            return self.__resized_key

        print(f"MSG BINARY SIZE: {msg.len()}\n   HALF: {msg_half}")

        if key_length > msg_half:
            new_key: bin = self.data()[:msg_half]
        else:
            remainder: int = msg_half % key_length
            multiple: int = math.floor(msg_half / key_length)
            new_key: bin = (self.data() * multiple) + (self.data()[:remainder] if remainder > 0 else "")

        print(f"OLD KEY SIZE: {key_length}\n   NEW SIZE: {len(new_key)}\nOLD KEY: {self.data()}\n   NEW KEY: {new_key}")
        self.__resized_key: bin = new_key
        return new_key
