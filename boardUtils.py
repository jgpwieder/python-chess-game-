from pieces import Empty, Pawn, Rook, Horse, Bishop, King, Queen
from position import Position


def freshBoard():
    return [
        setPieceRank("white"),
        setPawnRank("white"),
        setEmptyRank(2),
        setEmptyRank(3),
        setEmptyRank(4),
        setEmptyRank(5),
        setPawnRank("black"),
        setPieceRank("black"),
    ]


def setPieceRank(team):
    rank = 0
    if team == "black":
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
    if team == "black":
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
