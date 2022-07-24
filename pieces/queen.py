from resource import Resource
from checks import checkTeam
from utilsMove import topRightMove, topLeftMove, bottomLeftMove, bottomRightMove, rankMoveUp, \
    rankMoveDown, fileMoveRight, fileMoveLeft


def getPossibleMoves(position):
    rank = position.rank
    file = position.file

    moves1 = rankMoveUp(rank, file)
    moves2 = rankMoveDown(rank, file)
    moves3 = fileMoveRight(rank, file)
    moves4 = fileMoveLeft(rank, file)
    moves5 = topRightMove(rank, file)
    moves6 = topLeftMove(rank, file)
    moves7 = bottomLeftMove(rank, file)
    moves8 = bottomRightMove(rank, file)

    return [moves1, moves2, moves3, moves4, moves5, moves6, moves7, moves8]


class Queen(Resource):
    
    def __init__(self, position, team):
        self.position = position
        self.team = checkTeam(team)
        self.moves = getPossibleMoves(position)
        self.type = "Queen"
        self.representation = team[0].lower() + "Q"
        
    def recalculateMoves(self):
        self.moves = getPossibleMoves(self.position)
