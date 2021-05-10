class SummaryAluno():
    def __init__(self, name = "aluno"):
        self.name = name
        self.provas = 0
        self.questions = 0
        self.verifiedQuestions = 0
        self.errorCount = 0
        self.okCount = 0
        self.calculatePercentages()
        self.errorTypes = {}
    def calculatePercentages(self):
        if self.questions > 0:
            self.pVerified = self.verifiedQuestions/self.questions
            self.errorPerQuestion = self.errorCount/self.questions
        else:
            self.pVerified = 0
            self.errorPerQuestion = 0
        if self.verifiedQuestions > 0:
            self.pVerifiedOk = self.okCount/self.verifiedQuestions
            self.errorPerVerifiedQuestion = self.errorCount/self.verifiedQuestions
        else:
            self.pVerifiedOk = 0
            self.errorPerVerifiedQuestion = 0
    def generateTextSummary(self):
        self.calculatePercentages()
        s =  "Verificação de Provas por "+self.name+"\n\n"
        s += "Total Number Of Provas: " + str(self.provas)+"\n"
        s += "Total Number Of Questions: "+ str(self.questions)+"\n"
        s += "Total Verified Number of Questions: "+str(self.verifiedQuestions)+"\n"
        s += "Percentage of Questions Verified: "+str(self.pVerified)+"\n"
        s += "Number of errors: "+str(self.errorCount)+"\n"
        s += "Number of Oks: "+str(self.okCount)+"\n"
        s += "Percentage of Verified Questions Ok: "+str(self.pVerifiedOk)+"\n"
        s += "Errors per question: "+str(self.errorPerQuestion)+"\n"
        s += "Errors per verified question: "+str(self.errorPerVerifiedQuestion)
        return s
    def getTableModel(self):
        return {
            "Aluno": self.name,
            "Provas": self.provas,
            "Questões": self.questions,
            "Verificadas pelo Aluno": self.verifiedQuestions,
            "% Verificadas pelo Aluno": self.pVerified,
            "Erros reportados": self.errorCount,
            "Ok's nas Questões": self.okCount,
            "% OK's em Verificadas": self.pVerifiedOk,
            "Erros por questão": self.errorPerQuestion,
            "Erros por Verificada": self.errorPerVerifiedQuestion
        }
    def getTableDescriptionRow(self):
        return list(self.getTableModel().keys())
    def getTableRow(self):
        return list(self.getTableModel().values())
    def incrementErrorType(self, errorType):
        if not (errorType in self.errorTypes):
            self.errorTypes[errorType] = 0
        self.errorTypes[errorType] += 1
