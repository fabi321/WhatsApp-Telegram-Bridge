from abc import abstractmethod
from os import path

from persistent import Persistent

from Utilities.typings import FilePath, AccountName, AuthID


class UserStorage(Persistent):
    def __init__(self, name: AccountName, picture: bool = False, picture_path: FilePath = None):
        super().__init__()
        assert isinstance(name, AccountName)
        self.name: AccountName = name
        self.type: str = self.get_type_name()
        self.picture: bool = picture
        if picture and (not picture_path or not path.exists(picture_path)):
            raise FileNotFoundError(self.type + ' got picture tag, but no valid picture path for ' + name +
                                    ' with the picture path ' + str(picture_path) + '.')
        if picture:
            assert isinstance(picture_path, FilePath)
        self.picture_path: FilePath = picture_path

    def add_picture(self, picture_path: FilePath):
        if not path.exists(picture_path):
            raise FileNotFoundError('Tried to add picture to ' + self.type + ' ' + self.name +
                                    ' with invalid picture path ' + picture_path + '.')
        self.picture = True
        self.picture_path = picture_path

    def get_picture(self) -> FilePath:
        if not self.picture:
            raise FileNotFoundError('Tried to get a picture for ' + self.type + ' ' + self.name + ' but he had none.')
        return self.picture_path

    @abstractmethod
    def get_type_name(self) -> str:
        return 'User'

    def __str__(self) -> str:
        return str(self.id)

    def auth_id(self) -> AuthID:
        return AuthID(self.id)
