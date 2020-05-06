from DBModels.UserStorage import UserStorage
from Utilities.typings import TgUserId, AccountName, FilePath


class TgUserStorage(UserStorage):
    def __init__(self, id: TgUserId, name: AccountName, picture: bool = False, picture_path: FilePath = None):
        super().__init__(name=name, picture=picture, picture_path=picture_path)
        assert isinstance(id, TgUserId)
        self.id: TgUserId = id

    def get_type_name(self) -> str:
        return 'TgUser'
