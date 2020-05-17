from pathlib import Path
from typing import Type


class StrRepr(str):
    def __repr__(self):
        return f'{self.__class__.__name__}({self})'


class IntRepr(int):
    def __repr__(self):
        return f'{self.__class__.__name__}({int(self)})'


class WaNumber(IntRepr):
    pass


class AccountName(StrRepr):
    pass


class TgBotToken(StrRepr):
    pass


class TgBotId(IntRepr):
    pass


class TgBotName(StrRepr):
    pass


class TgUserId(StrRepr):
    pass


class MessageText(StrRepr):
    pass


class TgMessageId(IntRepr):
    pass


class WaMessageId(IntRepr):
    pass


class WaGroupId(StrRepr):
    pass


class TgGroupId(IntRepr):
    pass


class GroupName(StrRepr):
    pass


class GroupDescription(StrRepr):
    pass


FilePath: Type[Path] = Path


class AuthID(StrRepr):
    def __new__(cls, value):
        value = value.replace('-', 'm')
        value = value.replace('+', 'p')
        return str.__new__(cls, value)


class Password(StrRepr):
    pass
