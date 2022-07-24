

def checkPosition(rank, file):
    if rank > 7 or rank < 0:
        raise Exception("Rank is out of range")
    if file > 7 or file < 0:
        raise Exception("File is out of range")
    return rank, file


def checkColor(color):
    if color != "White" and color != "Black":
        raise Exception("Invalid color")
    return color


def checkTeam(team):
    if team != "White" and team != "Black":
        raise Exception("Invalid team")
    return team


def checkMovesListBoundary(movesList):
    validMoves = []
    for moves in movesList:
        validMoves.append(checkMovesBoundary(moves))
    return validMoves


def checkMovesBoundary(moves):
    validMoves = []
    for move in moves:
        if checkMoveBoundary(move):
            validMoves.append(move)
    return validMoves


def checkMoveBoundary(move):
    if move[0] > 7 or move[0] < 0:
        return None
    if move[1] > 7 or move[1] < 0:
        return None
    return move
