from rent_o_matic.domain import room as r


class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self):
        return [r.Room.from_dict(i) for i in self.data]
