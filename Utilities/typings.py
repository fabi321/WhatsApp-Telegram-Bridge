from typing import NewType


class WaNumber(int):
    pass


class AccountName(str):
    pass


class TgBotToken(str):
    pass


class TgBotId(int):
    pass


class TgBotName(str):
    pass


class TgUserId(str):
    pass


class MessageText(str):
    pass


class TgMessageId(int):
    pass


class WaMessageId(int):
    pass


class WaGroupId(str):
    pass


class TgGroupId(int):
    pass


class GroupName(str):
    pass


class GroupDescription(str):
    pass


class FilePath(str):
    pass


class AuthID(str):
    def __new__(cls, value):
        value = value.replace('-', 'm')
        value = value.replace('+', 'p')
        return str.__new__(cls, value)
