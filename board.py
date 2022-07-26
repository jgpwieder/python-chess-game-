import copy
from pieces import Empty
from position import Position
from resource import Resource
from utils import movesFromRaysOfMoves, splitListBetween
from utilsBoard import freshBoard, getPawnDiagonal, formatMove, getOtherTeam, buildLine


class Board(Resource):
    """ Board object:
        - matrix [nested list] list of ranks. Ranks are lists of pieces
        - capturedPieces [list of pieces]: list of pieces that were captured with the position that they were captured
        - movedPieces [list of pieces]: list of pieces that moved with the start position
        - moveLog [list of strings]: list of strings that represent every move
        - team [string]: color of the pieces playing.
        - whiteKingPosition [Position]: position of the white king
        - blackKingPosition [Position]: position of the black king
    """

    def __init__(self):
        self.matrix = freshBoard()
        self.capturedPieces = []
        self.movedPieces = []
        self.moveLog = []
        self.team = "White"
        self.whiteKingPosition = Position(0, 4)
        self.blackKingPosition = Position(7, 4)

    def getTeamKingPosition(self):
        if self.team == "White":
            return self.whiteKingPosition
        return self.blackKingPosition

    def resetTeam(self):
        otherTeam = "Black"
        if self.team == "Black":
            otherTeam = "White"
        self.team = otherTeam

    """Set the log, movedPieces and capturedPieces. Called in the movePiece method"""

    def registerMove(self, move, startPosition, movedPiece, capturedPiece):
        movPiece = copy.deepcopy(movedPiece)
        movPiece.position = startPosition  # Reset the location of the moved piece for storage
        self.moveLog.append(move)
        self.capturedPieces.append(capturedPiece)
        self.movedPieces.append(movPiece)

    def recalculateBoard(self):
        for row in range(0, 8):
            for file in range(0, 8):
                piece = self.matrix[row][file]
                piece.recalculateMoves()

    def getPiece(self, position):
        matrix = self.matrix
        return matrix[position.rank][position.file]

    def movePiece(self, startPosition, endPosition):
        # Get the info from the piece, change its position and recalculate moves:
        movedPiece = self.getPiece(startPosition)

        if movedPiece.representation == "bK":  # Move king
            self.blackKingPosition = endPosition
        if movedPiece.representation == "wK":
            self.whiteKingPosition = endPosition

        movedPiece.position = endPosition
        capturedPiece = self.matrix[endPosition.rank][endPosition.file]

        # Empty the startPosition and set the end position:
        self.matrix[startPosition.rank][startPosition.file] = Empty(startPosition)
        self.matrix[endPosition.rank][endPosition.file] = movedPiece

        # Register the move to the log and also store the pieces involved on the board state
        chessNotationMove = formatMove(startPosition, endPosition)
        self.registerMove(
            chessNotationMove,
            startPosition,
            movedPiece,
            capturedPiece
        )

        print(chessNotationMove)
        self.recalculateBoard()

    def undoMove(self):
        if len(self.moveLog) != 0:
            movedPiece = self.movedPieces.pop()
            capturedPiece = self.capturedPieces.pop()
            self.matrix[movedPiece.position.rank][movedPiece.position.file] = movedPiece
            self.matrix[capturedPiece.position.rank][capturedPiece.position.file] = capturedPiece
            self.resetTeam()
            print("UNDO")
            self.recalculateBoard()
            self.moveLog.pop()

    # this functions goes to the piece on the start position and checks if the
    # possible moves it has are legal in respect to the rest of the board
    """
        checkKing, ignoreKing, checkingPins = if this function is being called a second time for a specific reason and 
        we dont want it to become recursive, use this variables
    """
    def legalMoves(self, startPosition, checkingKing=False, ignoreKing=False, checkingPins=False):
        piece = self.matrix[startPosition.rank][startPosition.file]
        legalMoves = getPawnDiagonal(self.matrix, piece, startPosition)  # If Pawn, add possibility to capture
        listOfMoves = piece.moves

        if piece.type != "King" and not checkingPins:  # Check if the piece to be moved is pinned
            isPined, allowedMoves = self.checkForPins(startPosition, listOfMoves)
            if isPined:  # if it is pinned reset list of moves to the allowed moves
                listOfMoves = allowedMoves

        if piece.type == "King" and not checkingKing and not ignoreKing:
            listOfMoves = self.getKingMoves(listOfMoves, piece.team)  # If it is a king move, check for invalid Moves

        if not piece.team:  # If you chose an empty piece.
            return []
        for rayOfMoves in listOfMoves:  # check if the moving position is available:
            legalRayOfMoves = []
            blockedMoves = False
            for move in rayOfMoves:
                targetPiece = self.matrix[move[0]][move[1]]
                if blockedMoves:
                    break
                if targetPiece.representation == "--":
                    legalRayOfMoves.append(move)
                    continue
                blockedMoves = True
                if piece.team != targetPiece.team and piece.type != "Pawn":  # Pawns can't capture in moving direction
                    legalRayOfMoves.append(move)
                    continue
            legalMoves.append(legalRayOfMoves)
        return legalMoves

    def getMobilePiecesPosition(self, team, checkingKing=False, ignoreKing=False, checkingPins=False):
        mobilePieces = []
        for rank in range(0, 8):
            for file in range(0, 8):
                position = Position(rank, file)
                piece = self.getPiece(position)
                legalMoves = movesFromRaysOfMoves(self.legalMoves(position, checkingKing, ignoreKing, checkingPins))
                if legalMoves and piece.team == team:
                    mobilePieces.append([
                        piece.position.rank,
                        piece.position.file,
                    ])

        return mobilePieces

    def getOpponentMoves(self, team):
        # Get the opponent's pieces that can move but ignore calculating the
        # moves that the other king cannot do due to my pieces blocking it
        # and also calculating their pinned pieces
        mobilePiecesPosition = self.getMobilePiecesPosition(
            team=getOtherTeam(team),
            checkingKing=True,
            ignoreKing=True,
            checkingPins=True,
        )  # get opponent pieces allowed moving
        moves = []
        for piecePosition in mobilePiecesPosition:
            piece = self.matrix[piecePosition[0]][piecePosition[1]]
            moves.append(self.legalMoves(   # this output does not take into consideration the Rays of Moves
                startPosition=piece.position,
                checkingKing=True,
                checkingPins=True
            ))
        return moves

    def getKingMoves(self, listOfMoves, team):
        allowedMoves = []
        opponentMovesList = movesFromRaysOfMoves(self.getOpponentMoves(team))
        for moves in listOfMoves:
            if not moves:
                continue
            move = moves[0]

            doAppend = True
            for opponentMoveList in opponentMovesList: 
                if move in opponentMoveList:
                    doAppend = False

            if self.isProtected(move, team):
                doAppend = False

            if doAppend:
                allowedMoves.append([move])
        return allowedMoves

    def isProtected(self, move, team):
        copyBoard = copy.deepcopy(self)
        # Set the position of the move empty and see if it is in the list of opponent's moves:
        copyBoard.matrix[move[0]][move[1]] = Empty(Position(move[0], move[1]))
        opponentMoves = copyBoard.getOpponentMoves(team)
        for pieceMoves in opponentMoves:
            for rayOfMoves in pieceMoves:
                if [move[0], move[1]] in rayOfMoves:
                    return True
        return False

    def checkForPins(self, startPosition, moves):
        if not moves:
            return False, []
        # Check if a ray of moves contains both the current team's king and the piece analyzed
        piecePosition = [startPosition.rank, startPosition.file]
        kPosition = self.getTeamKingPosition()
        kingPosition = [kPosition.rank, kPosition.file]
        opponentMovesList = self.getOpponentMoves(self.team)

        # For every ray of opponent's moves, check if the ray contains the piece you want to
        # move and the king, if it does the piece is pinned.
        for opponentPiecesMoves in opponentMovesList:  # opponentPiecesMoves = [[rayOfMove1, rayOfMove2]]
            for opponentRayOfMoves in opponentPiecesMoves:
                line = buildLine(opponentRayOfMoves)
                if piecePosition in opponentRayOfMoves:
                    # Check for pieces between the king and the attacking piece, if there is, the piece is free to move:
                    print(opponentRayOfMoves)
                    if self.piecesBlockingKing(line, kingPosition, opponentRayOfMoves[0], piecePosition):
                        return False, []

                    if kingPosition in line:
                        # The piece is pinned, only one pin can exist for each piece, therefore,
                        # if the move and the king are contained in the opponentRayOfMoves, it is a legal move

                        legalMoves = []
                        # Go over every move possible for the piece, and check if is blocking the king from check
                        for rayOfMoves in moves:
                            for move in rayOfMoves:
                                if move in opponentRayOfMoves:
                                    legalMoves.append(move)
                        return True, [legalMoves]
        return False, []

    def piecesBlockingKing(self, line, kingPosition, attackingPiecePosition, piecePosition):
        betweenPiecesPosition = []
        betweenPositions = splitListBetween(kingPosition, attackingPiecePosition, line)

        for position in betweenPositions:
            piece = self.matrix[position[0]][position[1]]
            if piece.representation != "--" and position != piecePosition:
                betweenPiecesPosition.append(position)
        return betweenPiecesPosition
