from resource import Resource
from checks import checkTeam, checkMovesListBoundary


def getPossibleMoves(position):
    moves = []
    rank = position.rank
    file = position.file

    moves.append([[rank + 2, file + 1]])
    moves.append([[rank + 2, file - 1]])
    moves.append([[rank - 2, file + 1]])
    moves.append([[rank - 2, file - 1]])

    moves.append([[rank + 1, file + 2]])
    moves.append([[rank + 1, file - 2]])
    moves.append([[rank - 1, file + 2]])
    moves.append([[rank - 1, file - 2]])

    moves = checkMovesListBoundary(moves)
    return moves


class Horse(Resource):
    def __init__(self, position, team):
        self.position = position
        self.team = checkTeam(team)
        self.moves = getPossibleMoves(position)
        self.type = "Horse"
        self.representation = team[0].lower() + "N"

    def recalculateMoves(self):
        self.moves = getPossibleMoves(self.position)
