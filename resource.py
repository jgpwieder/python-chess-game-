

class Resource:

    def __str__(self):
        dictObj = self.__dict__
        stringObj = str(type(self)).split(".")[-1]
        stringObj = stringObj.split("'>")[0]

        returnObject = stringObj + ": {"
        if stringObj == "Position":
            for key in dictObj.keys():
                returnObject += f"\n\t\t{key}: {dictObj[key]},"
            returnObject += "\n\t}"
            return returnObject

        returnObject = stringObj + ": {"
        for key in dictObj.keys():
            returnObject += f"\n\t{key}: {dictObj[key]},"
        returnObject += "\n}"

        return returnObject

    def __name__(self):
        stringObj = str(type(self)).split(".")[-1]
        return stringObj.split("'>")[0]
