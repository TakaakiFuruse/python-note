from rent_o_matic.response_objects import response_objects as res

class RoomListUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, request):
        rooms = self.repo.list()
        return res.ResponseSuccess(rooms)
