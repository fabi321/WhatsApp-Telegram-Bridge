from __future__ import annotations

from DBModels import WaUserStorage
from DBModels.UserStorage import UserStorage
from Utilities.typings import TgBotId, TgBotToken


class TgBotStorage(UserStorage):
    def __init__(self, id: TgBotId, token: TgBotToken, wa_user: WaUserStorage.WaUserStorage):
        assert isinstance(wa_user, WaUserStorage.WaUserStorage)
        super().__init__(name=wa_user.name, picture=wa_user.picture, picture_path=wa_user.picture_path)
        assert isinstance(id, TgBotId)
        self.id: TgBotId = id
        assert isinstance(token, TgBotToken)
        self.token: TgBotToken = token
        self.wa_user: WaUserStorage.WaUserStorage = wa_user

    def get_type_name(self) -> str:
        return 'TgBot'

    def __repr__(self):
        return f'TgBotStorage({self.id!r}, {self.token!r}, {self.wa_user!r})'
