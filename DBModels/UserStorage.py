from abc import abstractmethod

from DBModels.Redirectable import Redirectable
from Utilities.typings import FilePath, AccountName, AuthID


class UserStorage(Redirectable):
    def __init__(self, name: AccountName, picture: bool = False, picture_path: FilePath = None):
        super().__init__()
        assert isinstance(name, AccountName)
        self.name: AccountName = name
        self.type: str = self.get_type_name()
        assert not picture_path or isinstance(picture_path, FilePath)
        self.picture: bool = picture
        self.id = 'changeme'
        if picture and (not picture_path or not picture_path.exists()):
            raise FileNotFoundError(self.type + ' got picture tag, but no valid picture path for ' + name +
                                    ' with the picture path ' + str(picture_path) + '.')
        self.picture_path: FilePath = picture_path

    def add_picture(self, picture_path: FilePath):
        if not picture_path.exists():
            raise FileNotFoundError('Tried to add picture to ' + self.type + ' ' + self.name +
                                    ' with invalid picture path ' + str(picture_path) + '.')
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
        return f'{self.id}'

    def __repr__(self):
        return (f'UserStorage({self.name!r}, picture={self.picture}'
                f'{", picture_path=" + self.picture_path.__repr__() if self.picture_path else ""})')

    def __eq__(self, other):
        if str(other) == self.__str__():
            return True
        return False

    def auth_id(self) -> AuthID:
        return AuthID(self.id)

    def get_pipe_name(self) -> str:
        return 'MessageUser'

    def get_pipe_id(self) -> str:
        return str(self.id)
