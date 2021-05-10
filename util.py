def removeWhiteSpaces(string):
    return string.replace(" ","").replace("\n","").replace("  ","")

def insertAtIndex(string, index, text):
    return string[:index] + text + string[index:]

def removeAtIndex(string, index, quantity):
    return string[:index]+string[index+quantity:]

def replaceAtIndex(string, index, text):
    return string[:index]+text+string[index+len(text):]

def splice(string, index, quantity):
    return string[:index]+string[index+quantity:]

def getWordBetween(string, index, orLeftString, orRightString = None): #or means or of elements of a list
    maximumIndex = len(string) - 1
    if orRightString is None:
        orRightString = orLeftString.copy()
    maximumLeftIndex = 0
    maximumLeftString = string[maximumLeftIndex]
    for leftString in orLeftString:
        leftIndex = string.rfind(leftString, 0, index)
        if(leftIndex > maximumLeftIndex and leftIndex != -1):
            maximumLeftIndex = leftIndex
            maximumLeftString = leftString
    minimumRightIndex = maximumIndex
    minimumRightString = string[minimumRightIndex]
    for rightString in orRightString:
        rightIndex = string.find(rightString, index+1, maximumIndex+1)
        if(rightIndex < minimumRightIndex and rightIndex != -1):
            minimumRightIndex = rightIndex
            minimumRightString = rightString
    return string[maximumLeftIndex+len(maximumLeftString):minimumRightIndex]

def checkSimpleOutsideTagSpaces(string, index, beforeString, afterString):   #Check if its inside, assuming XML is Correct (Simplest) like <b> e </b>
    leftString = string[:index]

    beforeIndexes = []
    beforeIndex = 0
    while(True):
        #print(beforeString,beforeIndex)
        beforeIndex = leftString.find(beforeString, beforeIndex)
        beforeIndexes.append(beforeIndex)
        if(beforeIndex == -1):
            break
        beforeIndex += 1
    beforeIndexes.pop()

    afterIndexes = []
    afterIndex = 0
    while(True):
        afterIndex = leftString.find(afterString, afterIndex)
        afterIndexes.append(afterIndex)
        if(afterIndex == -1):
            break
        afterIndex += 1
    afterIndexes.pop()

    while(not(len(afterIndexes) == 0 or len(beforeIndexes) == 0) and afterIndexes[0] < beforeIndexes[0]):
        afterIndexes.pop(0)

    return len(beforeIndexes) > len(afterIndexes)

def findNextAfterString(text, startIndex, beforeString, afterString):
    incrementedStartIndex = startIndex + 1
    while(True):
        #print(startIndex)
        endIndexAux = text.find(afterString, incrementedStartIndex)
        if(endIndexAux == -1):
            return -1
        startIndexAux = text.find(beforeString, incrementedStartIndex)
        if startIndexAux == -1 or startIndexAux >= endIndexAux:
            return endIndexAux
        else:
            endIndexInternAux = findNextAfterString(text, startIndexAux, beforeString, afterString)
            if endIndexInternAux == -1:
                return -1
            #print("Intern item found: ")
            #print(text[startIndexAux+len(beforeString):endIndexInternAux])
            startIndexNextInternAux = text.find(beforeString, endIndexInternAux+1)
            endIndexNextInternAux = text.find(afterString, endIndexInternAux+1)
            if startIndexNextInternAux == -1 or startIndexNextInternAux > endIndexNextInternAux:
                return endIndexNextInternAux
            else:
                incrementedStartIndex = startIndexNextInternAux

#def checkOutsideTagSpaces(string, index, beforeString, afterString):
