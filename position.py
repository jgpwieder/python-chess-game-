from resource import Resource
from checks import checkPosition


def getColor(rank, file):
    if ((rank + file) % 2) == 0:
        return"Black"
    return "White"


class Position(Resource):

    def __init__(self, rank, file):
        rank, file = checkPosition(rank, file)

        self.rank = rank
        self.file = file
        self.color = getColor(rank, file)
