import time
import pygame
from board import Board
from utilsMain import moveRelay, flipTeam


pygame.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
GAME_FONT = pygame.font.Font(pygame.font.get_default_font(), 30)


def loadImages():
    imageNames = [
        "bB", "bK", "bN", "bP", "bQ", "bR",
        "wB", "wK", "wN", "wP", "wQ", "wR",
    ]
    for name in imageNames:
        IMAGES[name] = pygame.transform.scale(
            pygame.image.load("images/" + name + ".png"),
            (SQ_SIZE, SQ_SIZE)
        )


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    board = Board()
    loadImages()

    end = False
    squareSelected = ()  # Keep track of last user click
    playerClicks = []  # Keep track of player clicks: two tuple [(startRow, startColumn), (endRow, end Column)]
    while not end:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                end = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # (x, y) location fo mouse
                column = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if squareSelected == (row, column):  # check if user clicked at the same square twice
                    squareSelected = ()  # clear the clicks and selections
                    playerClicks = []
                    printMessage(screen, "Invalid Move")
                else:
                    squareSelected = (row, column)
                    playerClicks.append(squareSelected)

                if len(playerClicks) == 1:  # if a piece was selected to be moved
                    pieces = board.getMobilePiecesPosition(board.team)  # check if piece is a valid piece to be moved
                    startPosition = moveRelay(playerClicks[0])  # translate the position
                    if [startPosition.rank, startPosition.file] not in pieces:
                        printMessage(screen, "Invalid Piece")
                        squareSelected = ()
                        playerClicks = []

                if len(playerClicks) == 2:  # if this is the second input, make a move
                    startPosition = moveRelay(playerClicks[0])
                    endPosition = moveRelay(playerClicks[1])  # flip rows of positions

                    moves = board.legalMoves(startPosition)
                    if [endPosition.rank, endPosition.file] not in moves:
                        printMessage(screen, "Invalid Move")
                        squareSelected = ()
                        playerClicks = []
                        continue

                    board.movePiece(startPosition, endPosition)
                    board.resetTeam()
                    squareSelected = ()
                    playerClicks = []

        drawGameBoard(screen, board)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def drawGameBoard(screen, board):
    drawBoardFrame(screen)
    drawPieces(screen, board.matrix)


def printMessage(screen, message):
    textSurface = GAME_FONT.render(message, True, pygame.Color("black"), pygame.Color("dark gray"))
    screen.blit(textSurface, dest=(2.5 * SQ_SIZE, 3.75 * SQ_SIZE))
    pygame.display.flip()
    time.sleep(0.2)


def drawBoardFrame(screen):
    colors = [pygame.Color("light gray"), pygame.Color("dark green")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            remainder = (row + column) % 2
            squareColor = colors[remainder]
            pygame.draw.rect(
                screen,
                squareColor,
                pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def drawPieces(screen, matrix):
    # Relay for pygame, need to reverse the rows to fit the GUI
    boardMatrix = matrix[:]
    boardMatrix.reverse()
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = boardMatrix[row][column].representation
            if piece != "--":
                screen.blit(
                    IMAGES[piece],
                    pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )


if __name__ == "__main__":
    main()
