class TagSpace():
    def __init__(self, start, end, outerStart, outerEnd):
        self.indexes = [outerStart,start,end,outerEnd]
    def incrementAll(self, quantity):
        self.indexes = list(map(lambda x : x + quantity, self.indexes))
    def incrementFrom(self, quantity, argIndex):
        for i in range(len(self.indexes)):
            if(self.indexes[i] >= argIndex):
                self.indexes[i] += quantity
    def getOuterStart(self):
        return self.indexes[0]
    def getStart(self):
        return self.indexes[1]
    def getEnd(self):
        return self.indexes[2]
    def getOuterEnd(self):
        return self.indexes[3]