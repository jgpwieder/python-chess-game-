import copy
from position import Position
from resource import Resource
from utilsBoard import freshBoard, getPawnDiagonal, formatMove
from pieces import Empty


class Board(Resource):
    """ Board object:
        - matrix [nested list] list of ranks. Ranks are lists of pieces
        - capturedPieces [list of pieces]: list of pieces that were captured with the position that they were captured
        - movedPieces [list of pieces]: list of pieces that moved with the start position
        - moveLog [list of strings]: list of strings that represent every move
    """
    def __init__(self):
        self.matrix = freshBoard()
        self.capturedPieces = []
        self.movedPieces = []
        self.moveLog = []
        self.team = "White"

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
        # for piece in self.capturedPieces:
        #     print("captured:")
        #     print(piece)
        # for piece in self.movedPieces:
        #     print("moved:")
        #     print(piece)

    def recalculateBoard(self):
        for row in range(0, 8):
            for file in range(0, 8):
                piece = self.matrix[row][file]
                piece.recalculateMoves()

    def getPiece(self, position):
        matrix = self.matrix
        return matrix[position.rank][position.file]

    def movePiece(self, startPosition, endPosition):
        if [endPosition.rank, endPosition.file] not in self.legalMoves(startPosition):
            raise Exception("Invalid move")
        # Get the info from the piece, change its position and recalculate moves:
        movedPiece = self.getPiece(startPosition)
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
    def legalMoves(self, startPosition, checkingKing=False):
        # Need to add the condition so that the king cannot move
        # to check and so that pieces can't move on absolute pins
        piece = self.matrix[startPosition.rank][startPosition.file]
        legalMoves = getPawnDiagonal(self.matrix, piece, startPosition)
        listOfMoves = piece.moves

        if piece.type == "King" and not checkingKing:
            listOfMoves = self.getKingMoves(listOfMoves, piece.team)

        if not piece.team:  # If it is an empty piece
            return []
        for moves in listOfMoves:
            blockedMoves = False
            for move in moves:
                targetPiece = self.matrix[move[0]][move[1]]
                if blockedMoves:
                    break
                if not targetPiece.team:
                    legalMoves.append(move)
                    continue
                blockedMoves = True
                if piece.team != targetPiece.team and piece.type != "Pawn":
                    legalMoves.append(move)
                    continue
        return legalMoves

    def getMobilePiecesPosition(self, team, checkingKing=False):
        mobilePieces = []
        for rank in range(0, 8):
            for file in range(0, 8):
                position = Position(rank, file)
                piece = self.getPiece(position)
                if self.legalMoves(position, checkingKing) and piece.team == team:
                    mobilePieces.append([
                        piece.position.rank,
                        piece.position.file,
                    ])

        return mobilePieces

    def getOpponentMoves(self, team, checkingKing=False):
        mobilePiecesPosition = self.getMobilePiecesPosition(team, checkingKing)
        moves = []
        for piecePosition in mobilePiecesPosition:
            piece = self.matrix[piecePosition[0]][piecePosition[1]]
            moves += piece.moves
        return moves

    def getKingMoves(self, listOfMoves, team):
        # This is a function specifically for the king
        allowedMoves = []
        opponentMoves = self.getOpponentMoves(team, checkingKing=True)
        for moves in listOfMoves:
            if not moves:
                continue
            move = moves[0]
            if move not in opponentMoves:
                allowedMoves.append([move])
        return allowedMoves
