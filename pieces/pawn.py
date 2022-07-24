from resource import Resource
from checks import checkTeam, checkMovesBoundary


def getPossibleMoves(position, team):
    moves = []
    if team == "White":
        moves.append([position.rank + 1, position.file])
        if position.rank == 1:
            moves.append([3, position.file])

    if team == "Black":
        moves.append([position.rank - 1, position.file])
        if position.rank == 6:
            moves.append([4, position.file])

    return [checkMovesBoundary(moves)]


class Pawn(Resource):
    """ # Pawn object:
        - position [Position object]: contains position information
        - team [string]: team of the piece. Options: "Black", "White"
        - moves [nested list]: list of lists, each list inside defines moves in a specific direction,
                               if the first is blocked the next ones are not available
    """

    def __init__(self, position, team):
        self.position = position
        self.team = checkTeam(team)
        self.moves = getPossibleMoves(position, team)
        self.type = "Pawn"
        self.representation = team[0].lower() + "P"

    def recalculateMoves(self):
        self.moves = getPossibleMoves(self.position, self.team)
