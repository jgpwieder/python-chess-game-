from position import Position
from resource import Resource
from utilsBoard import freshBoard, getPawnDiagonal, formatMove
from pieces import Pawn, Horse, Bishop, Rook, King, Queen, Empty


class Board(Resource):

    def __init__(self):
        self.matrix = freshBoard()
        self.moveLog = []

    def writeToLog(self, move):
        self.moveLog.append(move)

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
        # Empty the startPosition and set the end position:
        self.matrix[startPosition.rank][startPosition.file] = Empty(startPosition)
        self.matrix[endPosition.rank][endPosition.file] = movedPiece
        chessNotationMove = formatMove(startPosition, endPosition)
        self.writeToLog(chessNotationMove)
        print(chessNotationMove)
        self.recalculateBoard()

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
