inputDictRank = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
}

outputDictFile = {
    "0": "A",
    "1": "B",
    "2": "C",
    "3": "D",
    "4": "E",
    "5": "F",
    "6": "G",
    "7": "H",
}


def splitInputs(inputs):
    listInp = [int(inputs[1]) - 1, inputDictRank[inputs[0]]]
    return listInp


def translateMoves(moves):
    strMoves = ""
    for move in moves:
        result = translateMove(move)
        strMoves += result + ", "
    return strMoves


def coordinatesToScreen(coordinates):
    # Two flips were required to math the board matrix to pygame:
    # Here I had to flip the rows of the input since in the method
    # drawPieces I had to flip the rows
    return [7 - coordinates[0], coordinates[1]]


def translateMove(move):
    rank = outputDictFile[str(move[1])]
    file = str(move[0] + 1)
    return f"{rank}{file}"


def zfill(value, length):
    while len(value) < length:
        value += " "
    return value


def movesFromRaysOfMoves(moves):
    """Transform a list of lists of ray of moves into a list of piece's moves"""
    formattedMoves = []
    for rayOfMoves in moves:
        for move in rayOfMoves:
            formattedMoves.append(move)
    return formattedMoves


def formatBoard(matrix):
    result = ["    A        B        C        D        E        F        G        H"]
    for rank in range(0, 8):
        row = "| "
        for file in range(0, 8):
            name = matrix[rank][file].__name__()
            if name == "Empty":
                name = " "
            name = zfill(name, 6)

            row += f"{name} | "
        result.append("-------------------------------------------------------------------------")
        result.append(row + str(rank + 1))

    result.append("-------------------------------------------------------------------------")
    result.append("    A        B        C        D        E        F        G        H")
    result.reverse()
    return result


def getDistanceFromStart(targetElement, elementList):
    index = 0
    for el in elementList:
        if el == targetElement:
            return index
        index += 1
    return None


def splitList(targetElement, elementList):
    index = 0
    for element in elementList:
        if element == targetElement:
            return elementList[0:index], elementList[index + 1:]
        index += 1
    return []


def splitListBetween(targetElement1, targetElement2, elementList):
    distance1 = getDistanceFromStart(targetElement1, elementList)
    distance2 = getDistanceFromStart(targetElement2, elementList)

    if distance1 is None or distance2 is None:
        return []
    if distance1 < distance2:
        returnList = splitList(targetElement1, elementList)
        if len(returnList) > 1:
            returnList = returnList[1]
        returnList = splitList(targetElement2, returnList)
        if len(returnList) > 1:
            returnList = returnList[0]
        return returnList

    returnList = splitList(targetElement2, elementList)
    if len(returnList) > 1:
        returnList = returnList[1]
    returnList = splitList(targetElement1, returnList)
    if len(returnList) > 1:
        returnList = returnList[0]
    return returnList
