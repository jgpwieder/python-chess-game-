from utils import splitInputs, formatBoard, translateMoves
from position import Position


def runGame(board, team):
    # Print Board:
    formattedBoard = formatBoard(board.matrix)
    print(*formattedBoard, sep='\n')

    # Get the piece to be moved:
    pieces = board.getMobilePiecesPosition(team)
    positionString = translateMoves(pieces)
    print(f"\n{team}'s turn! \nThese are the pieces available to be moved: {positionString}")

    while True:
        inputString = input(f"\nInput the location of piece you want to move:")
        if inputString in positionString and inputString:
            break
        print(f"\nNot a valid input. Options: {positionString}")

    rank, file = splitInputs(inputString)
    startPosition = Position(rank, file)

    # Get the move:
    moves = translateMoves(board.legalMoves(startPosition))
    print(f"\nAvailable moves: {moves}")

    # Input the move and check if valid:
    while True:
        inputString = input(f"\nInput your move:")
        if inputString in moves and inputString:
            break
        print(f"\nNot a valid input. Options: {moves}")

    rank, file = splitInputs(inputString)
    endPosition = Position(rank, file)
    board.movePiece(startPosition, endPosition)
    board.recalculateBoard()
    print("\n\n\n")

    newTeam = "White"
    if team == "White":
        newTeam = "Black"

    return newTeam, board


def runGameWithGui(board, team):

    # Get the piece to be moved:
    pieces = board.getMobilePiecesPosition(team)
    positionString = translateMoves(pieces)
    print(f"\n{team}'s turn! \nThese are the pieces available to be moved: {positionString}")

    while True:
        inputString = input(f"\nInput the location of piece you want to move:")
        if inputString in positionString and inputString:
            break
        print(f"\nNot a valid input. Options: {positionString}")

    rank, file = splitInputs(inputString)
    startPosition = Position(rank, file)

    # Get the move:
    moves = translateMoves(board.legalMoves(startPosition))
    print(f"\nAvailable moves: {moves}")

    # Input the move and check if valid:
    while True:
        inputString = input(f"\nInput your move:")
        if inputString in moves and inputString:
            break
        print(f"\nNot a valid input. Options: {moves}")

    rank, file = splitInputs(inputString)
    endPosition = Position(rank, file)
    board.movePiece(startPosition, endPosition)
    print("\n\n\n")

    newTeam = "White"
    if team == "White":
        newTeam = "Black"

    return newTeam, board


def moveRelay(playerClick):
    # Two flips were required to math the board matrix to pygame:
    # Here I had to flip the rows of the input since in the method
    # drawPieces I had to flip the rows
    click = [7 - playerClick[0], playerClick[1]]
    startPosition = Position(click[0], click[1])
    return startPosition


def flipTeam(team):
    newTeam = "White"
    if team == "White":
        newTeam = "Black"
    return newTeam
