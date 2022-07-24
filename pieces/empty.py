from resource import Resource


class Empty(Resource):
    
    def __init__(self, position):
        self.position = position
        self.team = None
        self.moves = None
        self.type = None
        self.representation = "--"

    def recalculateMoves(self):
        self.moves = None
