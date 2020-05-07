from secrets import token_urlsafe

from bcrypt import gensalt, hashpw

from DBModels.TgBotStorage import TgBotStorage
from DBModels.UserStorage import UserStorage
from Utilities.typings import WaNumber, AccountName, TgBotId, TgBotToken, FilePath, Password


class WaUserStorage(UserStorage):
    def __init__(self, id: WaNumber, name: AccountName, tg_bot_id: TgBotId, tg_bot_token: TgBotToken,
                 picture: bool = False, picture_path: FilePath = None):
        super().__init__(name=name, picture=picture, picture_path=picture_path)
        assert isinstance(id, WaNumber)
        self.id: WaNumber = id
        self.password: bytes = b'changeme'
        self.tg_bot: TgBotStorage = TgBotStorage(id=tg_bot_id, token=tg_bot_token, wa_user=self)

    def get_type_name(self) -> str:
        return 'WaUser'

    def generate_password(self) -> Password:
        password: Password = Password(token_urlsafe(16))
        salt: bytes = gensalt(13)
        self.password = hashpw(password=password.encode(), salt=salt)
        return password

    def change_password(self, password: Password):
        assert isinstance(password, Password)
        salt: bytes = gensalt(13)
        self.password = hashpw(password=password.encode(), salt=salt)

    def get_password_hash(self) -> str:
        if self.password == b'changeme':
            raise AttributeError('Read password hash before one was generated')
        return self.password.decode()
