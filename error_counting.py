import os
import xlsxwriter
import questionFunctions as qf
from question import Question
from summaryAluno import SummaryAluno

workbook = xlsxwriter.Workbook('summary.xlsx')
worksheet = workbook.add_worksheet()

provasCorrigidas = [
    "Engenharia - Grupo VIII 2011",
    "Engenharia 2014",
    "Engenharia de Produção 2014",
    "Engenharia Elétrica 2014",
    "Engenharia Florestal 2014",
    "Engenharia Mecânica 2014",
    "Engenharia Química 2014",
    "Teatro 2009",
    "Tecnologia em Marketing 2018",
    "Geografia 2011",
    "História 2011",          #Correção rápida
    "Filosofia 2011",
    "Letras 2011",
    "Física 2011",
    "Tecnologia em Gastronomia 2009",
    "Tecnologia em Design de Moda 2009",
    "Tecnologia em Gestão de Recursos Humanos 2009",
    "Secretariado Executivo 2009",
    "Relações Internacionais 2009",
    "Psicologia 2009"
]

#This is the base folder of all the students that has all the exams and questions .xml
#Este é o diretório da pasta que contem todos os alunos com todas as suas provas e questões .xml
baseDirName = "C:\\Users\\vinic\\Documents\\Projeto Enade - 2 010521\\Projeto Enade - 2"
#baseDirName = os.path.dirname(__file__) + "./Projeto Enade - 2" 
alunosDir = os.listdir(baseDirName)

summary = []
cursos = {}
for alunoName in alunosDir:
    if(alunoName.find(".") == -1):
    #if(alunoName.find(".") == -1 and alunoName == "Vinícius Pereira Duarte"):
        summaryAluno = SummaryAluno(alunoName)
        provasDirName = baseDirName + "/" + alunoName
        provasDir = os.listdir(provasDirName)
        for originalProvaName in provasDir:
            if(originalProvaName.find(".") == -1 and originalProvaName.lower().find("corrigid") == -1):#and (provaName in provasCorrigidas)):
                questionsDirName = provasDirName + "/" + originalProvaName
                questionsDir = os.listdir(questionsDirName)
                provaName = originalProvaName.replace("(1)","").replace("_"," ").replace(" – "," ").replace(" - "," ").replace(" (Irregulares de anos anteriores)", " ").replace("  "," ").replace("Físicia","Física").replace("Sistema de Informação", "Sistemas de Informação").replace("Analise", "Análise").strip()
                provaNameArray = provaName.split(" ")
                provaAnoString = provaNameArray[len(provaNameArray) - 1]
                cursoNameArray = provaNameArray[:len(provaNameArray) - 1]
                cursoName = " ".join(cursoNameArray)
                if not (cursoName in cursos):
                    cursos[cursoName] = 0
                cursos[cursoName] += 1
                if(cursoName == ''):
                    print(originalProvaName)
                    print(provaNameArray)
                try:
                    provaAno = int(provaAnoString)
                    for questionName in questionsDir:
                        if(questionName.endswith(".xml") and questionName != "current_question.xml" ):#and questionName == "tecnologia_em_gastronomia_2009_m_23.xml"):
                            question = Question(questionName, questionsDirName)
                            with open(question.path,'r+', encoding='utf-8') as questionFile:
                                question.setText(questionFile.read())

                                qf.analyseVerifications(question, summaryAluno)
                                qf.verifySources(question,summaryAluno)
                                qf.verifySecondPqs(question, summaryAluno)       
                                qf.verifyInternalQuestions(question,provaAno, summaryAluno)
                                qf.verifyAnswerOptions(question, summaryAluno, provaAno)
                                qf.verifyLists(question, summaryAluno)
                                qf.verifyComments(question, summaryAluno)

                                #print(question.text)
                                question.changeFile = False
                                if question.changeFile:
                                    questionFile.truncate(0)
                                    questionFile.seek(0)
                                    questionFile.write(question.text)
                    #print("("+provaName+")" + " Error Count = "+str(errorCount)+"\n\n\n\n")
                    summaryAluno.provas += 1
                except(ValueError):
                    pass
        summary.append(summaryAluno)

s = "Verificação das provas do grupo 2 Enade\n\n"
stringSummaryArray = map(lambda x : x.generateTextSummary(), summary)
stringSummary = '\n\n'.join(stringSummaryArray)
s+=stringSummary
#print(s)
with open("./log.txt",'w', encoding='utf-8') as logFile:
    logFile.seek(0)
    logFile.write(s)

s = ""
countErros = 0
for summaryAluno in summary:
    countErrosAluno = 0
    for errorType in summaryAluno.errorTypes:
        countErrosAluno += summaryAluno.errorTypes[errorType]
    s += summaryAluno.name + " - Total de erros: "+str(countErrosAluno)
    s += "\n" + str(summaryAluno.errorTypes) + "\n\n"
    countErros += countErrosAluno
s+= "Total de erros: "+str(countErros)

with open("./log_tipo_erros.txt",'w', encoding='utf-8') as logErrosFile:
    logErrosFile.seek(0)
    logErrosFile.write(s)

rows = [SummaryAluno().getTableDescriptionRow()]
for summaryAluno in summary:
    rows.append(summaryAluno.getTableRow())
for y in range(len(rows)):
    row = rows[y]
    #print(row)
    for x in range(len(row)):
        value = row[x]
        worksheet.write(y,x,value)

cursoNameList = list(cursos.keys())
cursoNameList.sort()

s = "Número de nomes de cursos distintos: "+str(len(cursoNameList))+"\n\n"
s += "\n".join(cursoNameList)
with open("./nome_cursos_enade.txt",'w', encoding='utf-8') as nomeCursosFile:
    nomeCursosFile.seek(0)
    nomeCursosFile.write(s)
#print("\n".join(map(lambda a: repr(a), cursoNameList)))
#print(len(cursoNameList))

workbook.close()
        
