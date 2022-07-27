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
        self._position = position
        self.team = checkTeam(team)
        self.moves = getPossibleMoves(position, team)
        self._type = "Pawn"
        self.representation = team[0].lower() + "P"

    @property
    def position(self):
        return self._position

    @property
    def type(self):
        return self._type

    @position.setter
    def position(self, position):
        if position.rank == 7 and self.team == "White":
            self._type = "Promoted"
        if position.rank == 0 and self.team == "Black":
            self._type = "Promoted"
        self._position = position

    def recalculateMoves(self):
        self.moves = getPossibleMoves(self.position, self.team)
