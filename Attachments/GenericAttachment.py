from persistent import Persistent


class GenericAttachment(Persistent):
    def __init__(self):
        super().__init__()
