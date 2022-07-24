

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


def translateMove(move):
    rank = outputDictFile[str(move[1])]
    file = str(move[0] + 1)
    return f"{rank}{file}"


def zfill(value, length):
    while len(value) < length:
        value += " "
    return value


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
