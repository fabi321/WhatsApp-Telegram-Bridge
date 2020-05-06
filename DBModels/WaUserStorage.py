from DBModels.UserStorage import UserStorage
from DBModels.TgBotStorage import TgBotStorage
from Utilities.typings import WaNumber, AccountName, TgBotId, TgBotToken, FilePath


class WaUserStorage(UserStorage):
    def __init__(self, id: WaNumber, name: AccountName, tg_bot_id: TgBotId, tg_bot_token: TgBotToken,
                 picture: bool = False, picture_path: FilePath = None):
        super().__init__(name=name, picture=picture, picture_path=picture_path)
        assert isinstance(id, WaNumber)
        self.id: WaNumber = id
        self.tg_bot: TgBotStorage = TgBotStorage(id=tg_bot_id, token=tg_bot_token, wa_user=self)

    def get_type_name(self) -> str:
        return 'WaUser'
