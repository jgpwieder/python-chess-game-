from resource import Resource
from checks import checkTeam, checkMovesListBoundary


def getPossibleMoves(position):
    moves = []
    rank = position.rank
    file = position.file

    moves.append([[rank + 1, file + 1]])
    moves.append([[rank + 1, file]])
    moves.append([[rank + 1, file - 1]])

    moves.append([[rank, file + 1]])
    moves.append([[rank, file - 1]])

    moves.append([[rank - 1, file + 1]])
    moves.append([[rank - 1, file]])
    moves.append([[rank - 1, file - 1]])

    return checkMovesListBoundary(moves)


class King(Resource):
    
    def __init__(self, position, team):
        self.position = position
        self.team = checkTeam(team)
        self.moves = getPossibleMoves(position)
        self.type = "King"
        self.representation = team[0].lower() + "K"

    def recalculateMoves(self):
        self.moves = getPossibleMoves(self.position)
