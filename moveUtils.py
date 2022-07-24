from checks import checkMovesBoundary


#  Rook moves:
def rankMoveUp(rank, file):
    moves = []
    for moveRank in range(rank + 1, 8):
        moves.append([moveRank, file])
    return checkMovesBoundary(moves)


def rankMoveDown(rank, file):
    moves = []
    for moveRank in range(0, rank):
        moves.append([moveRank, file])
    moves = checkMovesBoundary(moves)
    moves.reverse()
    return moves


def fileMoveRight(rank, file):
    moves = []
    for moveFile in range(file + 1, 8):
        moves.append([rank, moveFile])
    return checkMovesBoundary(moves)


def fileMoveLeft(rank, file):
    moves = []
    for moveFile in range(0, file):
        moves.append([rank, moveFile])
    moves = checkMovesBoundary(moves)
    moves.reverse()
    return moves


# Bishop moves:
def topRightMove(rank, file):
    moveCount = min([7 - rank, 7 - file])
    moves = []
    for move in range(1, moveCount + 1):
        moves.append([rank + move, file + move])
    return checkMovesBoundary(moves)


def topLeftMove(rank, file):
    moveCount = min([7 - rank, file])
    moves = []
    for move in range(1, moveCount + 1):
        moves.append([rank + move, file - move])
    return checkMovesBoundary(moves)


def bottomLeftMove(rank, file):
    moveCount = min([rank, file])
    moves = []
    for move in range(1, moveCount + 1):
        moves.append([rank - move, file - move])
    return checkMovesBoundary(moves)


def bottomRightMove(rank, file):
    moveCount = min([rank, 7 - file])
    moves = []
    for move in range(1, moveCount + 1):
        moves.append([rank - move, file + move])
    return checkMovesBoundary(moves)
