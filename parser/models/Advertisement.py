

class Advertisement:
    def __init__(self):
        self.id = 0
        self.cost = 0
        self.city = "Unknown"
        self.year = 0
        self.brand = "Unknown"
        self.model = "Unknown"
        self.date = "00.00.0000"
        self.engine = "Unknown"
        self.power = 0
        self.gear = "Unknown"
        self.sWheel = "Unknown"
        self.probeg = 0

    @staticmethod
    def getColumns():
        return ['id', 'cost', 'city', 'year', 'brand', 'model', 'date', 'engine', 'power', 'gear', 'sWheel', 'probeg']
