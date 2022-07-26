from checks import checkMoveBoundary, checkMovesBoundary
from pieces import Empty, Pawn, Rook, Horse, Bishop, King, Queen
from position import Position
from utils import translateMove


def freshBoard():
    return [
        setPieceRank("White"),
        setPawnRank("White"),
        setEmptyRank(2),
        setEmptyRank(3),
        setEmptyRank(4),
        setEmptyRank(5),
        setPawnRank("Black"),
        setPieceRank("Black"),
    ]


def setPieceRank(team):
    rank = 0
    if team == "Black":
        rank = 7
    return [
        Rook(Position(rank, 0), team),
        Horse(Position(rank, 1), team),
        Bishop(Position(rank, 2), team),
        Queen(Position(rank, 3), team),
        King(Position(rank, 4), team),
        Bishop(Position(rank, 5), team),
        Horse(Position(rank, 6), team),
        Rook(Position(rank, 7), team),
    ]


def setPawnRank(team):
    rank = 1
    if team == "Black":
        rank = 6

    rankList = []
    for file in range(0, 8):
        position = Position(rank, file)
        rankList.append(Pawn(position, team))
    return rankList


def setEmptyRank(rank):
    rankList = []
    for file in range(0, 8):
        rankList.append(Empty(Position(rank, file)))
    return rankList


def formatMove(startPosition, endPosition):
    start = translateMove([startPosition.rank, startPosition.file])
    end = translateMove([endPosition.rank, endPosition.file])
    return start + end


def getPawnDiagonal(matrix, piece, position):
    rank = position.rank
    file = position.file
    otherTeam = getOtherTeam(piece.team)
    legalMoves = []
    if piece.type == "Pawn" and piece.team == "White":
        move = [rank + 1, file + 1]
        if checkMoveBoundary(move):
            rightPiece = matrix[rank + 1][file + 1]
            if rightPiece.team == otherTeam:
                legalMoves.append([move])

        move = [rank + 1, file - 1]
        if checkMoveBoundary(move):
            leftPiece = matrix[rank + 1][file - 1]
            if leftPiece.team == otherTeam:
                legalMoves.append([move])

    if piece.type == "Pawn" and piece.team == "Black":
        move = [rank - 1, file + 1]
        if checkMoveBoundary(move):
            rightPiece = matrix[rank - 1][file + 1]
            if rightPiece.team == otherTeam:
                legalMoves.append([move])

        move = [rank - 1, file - 1]
        if checkMoveBoundary(move):
            leftPiece = matrix[rank - 1][file - 1]
            if leftPiece.team == otherTeam:
                legalMoves.append([move])
    return legalMoves


def getOtherTeam(team):
    otherTeam = "Black"
    if team == "Black":
        otherTeam = "White"
    if not team:
        return None
    return otherTeam


def buildLine(opponentRayOfMoves):
    if len(opponentRayOfMoves) < 2:
        return []
    move1 = opponentRayOfMoves[0]
    move2 = opponentRayOfMoves[1]

    # If it is not a diagonal ray of move:
    if move1[0] == move2[0]:
        rank = move1[0]
        return [[rank, 0], [rank, 1], [rank, 2], [rank, 3], [rank, 4], [rank, 5], [rank, 6], [rank, 7]]
    if move1[1] == move2[1]:
        file = move1[1]
        return [[0, file], [1, file], [2, file], [3, file], [4, file], [5, file], [6, file], [7, file]]

    # If it is a diagonal move to/from the top right (add|subtract one to both rank and file):
    moveToTopRight = [move1[0] + 1, move1[1] + 1]
    moveFomTopRight = [move1[0] - 1, move1[1] - 1]
    if move2 == moveToTopRight or move2 == moveFomTopRight:
        line = []
        for adder in range(-7, +8):
            line.append([move1[0] + adder, move1[1] + adder])
        return checkMovesBoundary(line)

    # else, it is a move in to or from the top left:
    line = []
    for adder in range(-7, +8):
        line.append([move1[0] - adder, move1[1] + adder])
    return checkMovesBoundary(line)
