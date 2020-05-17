from abc import abstractmethod
from typing import List

from DBModels.MessageStorage import MessageStorage
from DBModels.WaGroupStorage import WaGroupStorage
from DBModels.WaUserStorage import WaUserStorage
from Handlers.GeneralStorageManager import GeneralStorageManager
from Utilities.Pipes import Pipes


class WaBotHandler(GeneralStorageManager):
    def __init__(self, ):
        super().__init__()
        self.pipe = Pipes(str('wa_manager'))

    def __call__(self, *args, **kwargs):
        self.start_bot()

    def endless_loop(self):
        status = True
        while status:
            pipe_output: str = self.pipe.read_pipe()
            status = self.handle_pipe_output(pipe_output)

    def handle_pipe_output(self, pipe_string: str):
        splitted: List[str] = pipe_string.split(':')
        if splitted[0] == 'MessageUser':
            message: MessageStorage = self.root.messages[splitted[1]]
            user: WaUserStorage = self.root.wa_users[splitted[2]]
            self.send_message_to_user(message=message, user=user)
            self.commit()
        elif splitted[0] == 'MessageGroup':
            message: MessageStorage = self.root.messages[splitted[1]]
            group: WaGroupStorage = self.root.wa_groups[splitted[2]]
            self.send_message_to_group(message=message, group=group)
            self.commit()
        elif splitted[0] == 'Quit':
            self.__del__()
            return False
        return True

    def __del__(self):
        self.stop_bot()
        self._connection.close()

    @abstractmethod
    def start_bot(self):
        raise NotImplementedError()

    @abstractmethod
    def send_message_to_user(self, message: MessageStorage, user: WaUserStorage):
        raise NotImplementedError()

    @abstractmethod
    def send_message_to_group(self, message: MessageStorage, group: WaGroupStorage):
        raise NotImplementedError()

    @abstractmethod
    def stop_bot(self):
        raise NotImplementedError()
