from checks import checkTeam
from resource import Resource
from utilsMove import topRightMove, topLeftMove, bottomLeftMove, bottomRightMove



def getPossibleMoves(position):
    rank = position.rank
    file = position.file

    moves1 = topRightMove(rank, file)
    moves2 = topLeftMove(rank, file)
    moves3 = bottomLeftMove(rank, file)
    moves4 = bottomRightMove(rank, file)

    return [moves1, moves2, moves3, moves4]


class Bishop(Resource):
    
    def __init__(self, position, team):
        self.position = position
        self.team = checkTeam(team)
        self.moves = getPossibleMoves(position)
        self.type = "Bishop"
        self.representation = team[0].lower() + "B"
        
    def recalculateMoves(self):
        self.moves = getPossibleMoves(self.position)
