from typing import List

from persistent import Persistent
from persistent.list import PersistentList

from DBModels.UserStorage import UserStorage
from Utilities.typings import GroupDescription, GroupName, AuthID


class GroupStorage(Persistent):
    def __init__(self, name: GroupName, description: GroupDescription, users: List[UserStorage] = None):
        super().__init__()
        assert isinstance(name, GroupName)
        self.name: GroupName = name
        assert isinstance(description, GroupDescription)
        self.description: GroupDescription = description
        if users:
            assert all([isinstance(i, UserStorage) for i in users])
        self.users: PersistentList[UserStorage] = PersistentList(users)

    def add_user(self, user: UserStorage):
        assert isinstance(user, UserStorage)
        if user not in self.users:
            self.users += [user]

    def remove_user(self, user: UserStorage):
        if user not in self.users:
            raise NotImplementedError('Tried to remove user ' + str(user) + ' from group ' + self.name +
                                      ' without being in the List.')
        self.users.pop(self.users.index(user))

    def __str__(self) -> str:
        return str(self.id)

    def auth_id(self) -> AuthID:
        return AuthID(self.id)
