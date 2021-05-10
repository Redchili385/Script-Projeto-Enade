import util
from tagSpace import TagSpace

class Question():
    def __init__(self, name, dirName):
        self.text = None
        self.name = name
        self.dirName = dirName
        self.path = self.dirName + "/" + self.name
        self.nameArray = self.name.replace(".xml","",1).split('_')
        self.updateNumberAndType()
        self.changeFile = False
        self.addCommentsAfterCorrected = False
    def updateNumberAndType(self):
        l = len(self.nameArray)
        try:
            self.number = int(self.nameArray[l-1])
            self.type = self.nameArray[l-2]
        except ValueError:
            try:
                self.number = int(self.nameArray[l-2])
                self.type = self.nameArray[l-3]
            except:
                self.number = self.nameArray[l-1]
                self.type = self.nameArray[l-2]
    def setText(self, text):
        self.text = text
    def findAllTagSpacesBetween(self, beforeString, afterString, string = None, getInner = False):
        if string is None: string = self.text
        tagSpaces = []
        startIndex = 0
        endIndex = 0
        while(True):
            #print("Primeiro While")
            startIndex = string.find(beforeString, endIndex)
            if(startIndex == -1):
                break
            if(getInner):
                endIndex = string.find(afterString, startIndex)
            else:
                endIndex = util.findNextAfterString(string, startIndex, beforeString, afterString)
            if(endIndex == -1):
                break
            tagSpaces.append(TagSpace(startIndex+len(beforeString), endIndex, startIndex, endIndex+len(afterString)))
        return tagSpaces
    def findAllBetween(self, beforeString, afterString, string = None, getInner = False):
        if string is None: string = self.text
        pieces = []
        tagSpaces = self.findAllTagSpacesBetween(beforeString, afterString, string, getInner)
        for tagSpace in tagSpaces:
            pieces.append(self.getInnerText(tagSpace, string))        
        return pieces
    def getAllCommentsOnNextSpace(self, index):
        subString = self.text[index:self.findNextNonCommentTag(index)]
        return self.findAllBetween("<!--","-->", subString)
    def findNextNonCommentTag(self, startIndex):
        while True:
            tagIndex = self.text.find("<", startIndex)
            commentIndex = self.text.find("<!--", startIndex)
            if(tagIndex == -1):
                return None
            if(tagIndex == commentIndex):
                endCommentIndex = self.text.find("-->",commentIndex)
                if(endCommentIndex == -1):
                    return None
                else:
                    startIndex = endCommentIndex+3
            else:
                return tagIndex
            #print(string[tagIndex:])
    def insertAtIndex(self, index, text, tagSpaces = []):
        self.text = util.insertAtIndex(self.text, index, text)
        l = len(text)
        for tagSpace in tagSpaces:
            tagSpace.incrementFrom(l, index)
    def removeAtIndex(self, index, quantity, tagSpaces = []):
        self.text = util.removeAtIndex(self.text, index, quantity)
        for tagSpace in tagSpaces:
            tagSpace.incrementFrom(-1 * quantity, index + 1)
    def replaceAtIndex(self, index, text, tagSpaces = []):
        lQuestion = len(self.text[index:])
        lText = len(text)
        l = lText -  lQuestion
        self.text = util.replaceAtIndex(self.text, index, text)
        if(l > 0):
            for tagSpace in tagSpaces:
                tagSpace.incrementFrom(l, index + lText + 1)
    def getInnerText(self, tagSpace, string = None):
        if string is None: string = self.text
        return string[tagSpace.getStart():tagSpace.getEnd()]
    def addCommentAfterIndex(self, index, newComment, similarComments = [], tagSpaces = [], forceComment = False):
        if(forceComment or self.addCommentsAfterCorrected):
            minimumCommentIndex = index
            maximumCommentIndex = self.findNextNonCommentTag(minimumCommentIndex)
            similarComments.insert(0, newComment)
            flagFound = False
            for similarComment in similarComments:
                if(util.removeWhiteSpaces(self.text[minimumCommentIndex:maximumCommentIndex]).find(util.removeWhiteSpaces(similarComment)) != -1):
                    flagFound = True
            if(not flagFound):
                self.insertAtIndex(minimumCommentIndex, newComment, tagSpaces)
            return not flagFound  #CommentNotFound, Added to String
        return False
