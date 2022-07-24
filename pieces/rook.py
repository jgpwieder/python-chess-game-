from resource import Resource
from checks import checkTeam
from utilsMove import rankMoveUp, rankMoveDown, fileMoveRight, fileMoveLeft


def getPossibleMoves(position):
    rank = position.rank
    file = position.file

    moves1 = rankMoveUp(rank, file)
    moves2 = rankMoveDown(rank, file)
    moves3 = fileMoveRight(rank, file)
    moves4 = fileMoveLeft(rank, file)

    return [moves1, moves2, moves3, moves4]


class Rook(Resource):
    def __init__(self, position, team):
        self.position = position
        self.team = checkTeam(team)
        self.moves = getPossibleMoves(position)
        self.type = "Rook"
        self.representation = team[0].lower() + "R"

    def recalculateMoves(self):
        self.moves = getPossibleMoves(self.position)
