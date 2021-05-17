import util

def analyseVerifications(question, summaryAluno): 
    comments = []
    commentsWithOk = question.findAllBetween("<!--","-->")
    for comment in commentsWithOk:
        foundComment = util.removeWhiteSpaces(comment.lower())
        okComments = ["ok","corrigido"]
        flagFound = False
        for okComment in okComments:
            if(foundComment.find(okComment) != -1):
                flagFound = True
                break
        if(flagFound):
            summaryAluno.okCount += 1
        else:
            comments.append(comment)
            summaryAluno.errorCount += 1
    #if len(comments) > 0 and summaryAluno.name == "Vinícius Pereira Duarte":
    #    print(comments)
    if(len(commentsWithOk) > 0):
        summaryAluno.verifiedQuestions += 1
    else:pass
        #print("Erro: Prova sem Verificar")
        #print(questionName)
    summaryAluno.questions += 1

def verifySources(question, summaryAluno):
    sourceSpaces = question.findAllTagSpacesBetween("<source>","</source>")
    #print(list(map(lambda x: question.getInnerText(x),sourceSpaces)))
    for sourceSpace in sourceSpaces:
        italicWords = {"et al": "et al", " In: ": "In"}  #Identification: Real word
        for italicWord in italicWords:
            source = question.getInnerText(sourceSpace)
            italicWordComment = italicWords[italicWord]
            italicIndex = source.find(italicWord)
            if(italicIndex != -1):
                if(source.find("<italic>") != -1): pass
                    #print(questionName)
                    #print("Encontrado Itálico com "+italicWord)
                else:
                    newComment = "\n<!-- Faltou Itálico em \""+italicWordComment+"\" -->"
                    question.addCommentAfterIndex(sourceSpace.getOuterEnd(), newComment, [], sourceSpaces)
                    summaryAluno.incrementErrorType("Faltou Itálico em "+italicWordComment)
                    startIndex = sourceSpace.getStart()+italicIndex+italicWord.find(italicWordComment)
                    question.insertAtIndex(startIndex, "<italic>", sourceSpaces)
                    question.insertAtIndex(startIndex+len(italicWordComment)+len("<italic>"),"</italic>", sourceSpaces)
                    #print(question.name)
                    #print(question.text)
        
        source = question.getInnerText(sourceSpace)
        linkIdentifiers = ["http","www.",".com",".br",".gov",".shtml",".xml",".jpg",".pdf"]
        linkIndex = None
        for linkIndentifier in linkIdentifiers:
            index = source.find(linkIndentifier)
            if index != -1:
                linkIndex = index
                break
        if(linkIndex != None):
            links = question.findAllBetween("<link>","</link>", source)
            if len(links) == 0:
                newComment = "Faltou o link no XML"
                summaryAluno.incrementErrorType(newComment)
                link = util.getWordBetween(source, linkIndex, [" ",'\n','<','>','&lt;','&gt;','(',')'])
                if(link[-1:] == ','): link = link[:-1]
                if(link[-1:] == '.'): link = link[:-1]
                if(link[0:1] == '.'): link = link[1:]
                startIndex = sourceSpace.getStart()+source.find(link)
                if(source.find(link) == -1):
                    print("ERRRROOOOOO")
                question.insertAtIndex(startIndex, "<link>", sourceSpaces)
                question.insertAtIndex(startIndex + len("<link>") + len(link), "</link>", sourceSpaces)
                #print("|"+link+"|")
                comments = question.getAllCommentsOnNextSpace(sourceSpace.getOuterEnd())
                writtenComment = None
                for comment in comments:
                    if(comment.upper().find("link".upper()) != -1 ):
                        writtenComment = comment
                        break
                if(writtenComment is None):
                    newComment = "\n<!-- "+newComment+" -->"
                    question.addCommentAfterIndex(sourceSpace.getOuterEnd(), newComment, [], sourceSpaces)
                    #print("LINKS NOT FOUND")
                    #print("Erro de link e source, Questão "+questionName+" da Prova "+provaName)
                    #print(source)
                    #print(question.text)
                else: pass
                    #print(writtenComment)
            
            source = question.getInnerText(sourceSpace)
            linkSpaces = question.findAllTagSpacesBetween("<link>","</link>", source)  #Rescanning
            #links = list(map(lambda x: question.getInnerText(x, source),linkSpaces))
            if len(links) != 0:
                gtIndex = source.find("&gt")
                ltIndex = source.find("&lt")
                if gtIndex != -1 and ltIndex != -1 and gtIndex > ltIndex:
                    print("Link em perfeito estado encontrado, com <>")
                    print(question.name)
                    print(source)
                else:
                    newComment = "Faltou o <> nas extremidades do link (&lt; e &gt;)"
                    summaryAluno.incrementErrorType(newComment)

                    for linkSpace in linkSpaces:
                        leftString = "&lt;"
                        if(question.getInnerText(sourceSpace)[:linkSpace.getOuterStart()].find(leftString) == -1):
                            question.insertAtIndex(linkSpace.getOuterStart() + sourceSpace.getStart(), leftString, sourceSpaces)
                            linkSpace.incrementFrom(len(leftString), linkSpace.getOuterStart())
                        rightString = "&gt;"
                        if(question.getInnerText(sourceSpace)[linkSpace.getOuterEnd():].find(rightString) == -1):
                            question.insertAtIndex(linkSpace.getOuterEnd() + sourceSpace.getStart(), rightString, sourceSpaces)
                            linkSpace.incrementFrom(len(rightString), linkSpace.getOuterEnd())

                    comments = question.getAllCommentsOnNextSpace(sourceSpace.getOuterEnd())
                    flagFound = False
                    for comment in comments:
                        if comment.find("&gt;") != -1 or comment.find("&lt;") != -1:
                            flagFound = True
                            break
                    if(not flagFound):
                        newCommentXML = "\n<!-- "+newComment+" -->"
                        result = question.addCommentAfterIndex(sourceSpace.getOuterEnd(), newCommentXML, [
                            "\n<!-- Faltou o <> nas extremidades do link -->"
                        ], sourceSpaces)

def verifySecondPqs(question, summaryAluno):  #Analisar numeros romanos nos porquês
    secondPqSpaces = question.findAllTagSpacesBetween("<second>", "</second>")
    for secondPqSpace in secondPqSpaces:
        secondPq = question.getInnerText(secondPqSpace)
        if(secondPq.strip()[1] == '\n' or secondPq.strip()[2] == '\n' or secondPq.strip()[3] == '\n'):
            #print("E detectado")
            newComment = "Palavra \"E\" não deveria estar presente no segundo parágrafo do porque"
            summaryAluno.incrementErrorType(newComment)
            
            secondPqStartIndex = secondPqSpace.getStart()
            newLineIndex = secondPq.find(secondPq.strip()) + secondPq.strip().find("\n")
            quantity = newLineIndex + 1
            #print(quantity)
            question.removeAtIndex(secondPqStartIndex, quantity, secondPqSpaces)

            newCommentXML = "\n    <!-- "+newComment+" -->"
            question.addCommentAfterIndex(secondPqSpace.getOuterEnd(), newCommentXML, [], secondPqSpaces)

            #print("|"+repr(question.getInnerText(secondPqSpace))+"|")
            #print(question.text)

def verifyInternalQuestions(question, provaAno, summaryAluno):
    internalQuestionSpaces = question.findAllTagSpacesBetween("<question>", "</question>")
    l = len(internalQuestionSpaces)
    if(l != 1):
        newComment = "Erro no número de questões internas"
        newCommentXML = "\n<!-- "+newComment+": "+str(l)+" -->"
        summaryAluno.incrementErrorType(newComment)
        question.addCommentAfterIndex(len(question.text),newCommentXML, [], internalQuestionSpaces, True)
        if(l == 0):
            comments = question.findAllBetween("<!--","-->")
            flagFound = False
            for comment in comments:
                if comment.upper().find("question".upper()) != -1:
                    flagFound = True
                    break
            if(not flagFound): pass
                #print("Erro no número de questões internas")
                #print(len(internalQuestionSpaces))
                #print(questionName)
        else:
            questionCommentCounter = 0
            for internalQuestionSpace in internalQuestionSpaces:
                #internalQuestion = question[internalQuestionIndex["start"]:internalQuestionIndex["end"]]
                comments = question.getAllCommentsOnNextSpace(internalQuestionSpace.getOuterEnd())
                flagFound = False
                for comment in comments:
                    if comment.upper().find("question".upper()) != -1:
                        flagFound = True
                        break
                if(not flagFound):
                    questionCommentCounter += 1
            if(questionCommentCounter != len(internalQuestionSpaces) - 1): pass
                #print("Erro no número de questões internas")
                #print(questionName)
    else:
        if(provaAno == 2009 ):#and not(provaName in provasCorrigidas)):
            newComment = "O parágrafo acima deveria estar todo em negrito"
            newCommentXML = "\n<!-- "+newComment+" -->"
            for internalQuestionSpace in internalQuestionSpaces:
                internalQuestion = question.getInnerText(internalQuestionSpace)
                #print("Checking")
                if(util.checkSimpleOutsideTagSpaces(question.text, internalQuestionSpace.getStart(), "<b>","</b>") or
                   (internalQuestion.find("<b>") != -1 and internalQuestion.find("</b>") != -1 )): pass
                    #print(question.name)
                else:
                    summaryAluno.incrementErrorType(newComment)
                    question.insertAtIndex(internalQuestionSpace.getStart(), "<b>", internalQuestionSpaces)
                    question.insertAtIndex(internalQuestionSpace.getEnd(), "</b>", internalQuestionSpaces)
                    question.addCommentAfterIndex(internalQuestionSpace.getOuterEnd(), newCommentXML, [
                        "Faltou negrito na frase inteira acima",
                        "Faltou Negrito em toda frase acima", 
                        "A frase acima deveria estar toda em negrito"
                    ], internalQuestionSpaces)
                    #print(question.text)

def verifyAnswerOptions(question, summaryAluno, provaAno):
    answerOptionSpaces = question.findAllTagSpacesBetween("<answer_options>", "</answer_options>")
    if(question.type == "m"):
        if(len(answerOptionSpaces) != 1):
            newComment = "Erro no número de tags de answer_options"
            newCommentXML = "\n<!-- "+newComment+" -->"
            summaryAluno.incrementErrorType(newComment)
            question.addCommentAfterIndex(len(question.text),newCommentXML, [], answerOptionSpaces, True)
            #print("Erro no número de tags de answer_options")
            #print(len(answerOptionIndexes))
            #print(question.name)
            #print(question.text)
        else:
            #print(questionName)
            #print(answerOptionTags)
            answerOptionSpace = answerOptionSpaces[0]
            answerOption = question.getInnerText(answerOptionSpace)
            if(provaAno == 2009):
                questionOptions = question.findAllBetween("<question_options>", "</question_options>")
                if(len(questionOptions) > 0 and answerOption.find("<b>") == -1):
                    #print(answerOption)
                    newComment = "Os números romanos devem estar todos em negrito"
                    newCommentXML = "\n<!-- "+newComment+" -->"
                    oldL = len(answerOption)
                    summaryAluno.incrementErrorType(newComment)

                    answerOption = answerOption.replace(" I "  ," <b>I</b> ")
                    answerOption = answerOption.replace(" II " ," <b>II</b> ")
                    answerOption = answerOption.replace(" III "," <b>III</b> ")
                    answerOption = answerOption.replace(" IV " ," <b>IV</b> ")
                    answerOption = answerOption.replace(" V "  ," <b>V</b> ")
                    answerOption = answerOption.replace(" VI " ," <b>VI</b> ")

                    answerOption = answerOption.replace(" I."  ," <b>I</b>.")
                    answerOption = answerOption.replace(" II." ," <b>II</b>.")
                    answerOption = answerOption.replace(" III."," <b>III</b>.")
                    answerOption = answerOption.replace(" IV." ," <b>IV</b>.")
                    answerOption = answerOption.replace(" V."  ," <b>V</b>.")
                    answerOption = answerOption.replace(" VI." ," <b>VI</b>.")

                    answerOption = answerOption.replace(" I,"  ," <b>I</b>,")
                    answerOption = answerOption.replace(" II," ," <b>II</b>,")
                    answerOption = answerOption.replace(" III,"," <b>III</b>,")
                    answerOption = answerOption.replace(" IV," ," <b>IV</b>,")
                    answerOption = answerOption.replace(" V,"  ," <b>V</b>,")
                    answerOption = answerOption.replace(" VI," ," <b>VI</b>,")

                    question.removeAtIndex(answerOptionSpace.getStart(), oldL, answerOptionSpaces)
                    question.insertAtIndex(answerOptionSpace.getStart(), answerOption, answerOptionSpaces)
                    question.addCommentAfterIndex(answerOptionSpace.getOuterEnd(), newCommentXML, [], answerOptionSpaces)
                    #print(question.text)
            answerOption = question.getInnerText(answerOptionSpace)
            items = question.findAllBetween("<item>", "</item>", answerOption)
            if(len(items) != 5):
                newComment = "Erro no número de items de uma questão de Múltipla Escolha"
                newCommentXML = "\n<!-- "+newComment+" -->"
                summaryAluno.incrementErrorType(newComment)
                question.addCommentAfterIndex(answerOptionSpace.getOuterEnd(),newCommentXML, [], answerOptionSpaces, True)
    elif(question.type == "d"):
        pass
    else: pass
        #print(question.type)

def verifyLists(question, summaryAluno):
    listSpaces = question.findAllTagSpacesBetween("<list>", "</list>")
    if(question.type == "d"):
        if(len(listSpaces) > 0):
            #print("\n"+questionName+"\n")
            for listSpace in listSpaces:
                List = question.getInnerText(listSpace)
                #print(repr(List))
                #print(List)
                #List = util.removeWhiteSpaces(List)
                itemSpaces = question.findAllTagSpacesBetween("<item>", "</item>", List)
                errorIdentified = False
                #print(len(itemSpaces))
                for itemSpace in itemSpaces:
                    item = question.getInnerText(itemSpace, question.getInnerText(listSpace))
                    itemWE = util.removeWhiteSpaces(item) #Item Without Spaces
                    
                    #print("ITEM")
                    #print(item)
                    #print("\n\n")
                    if len(itemWE) > 2 and itemWE[1] == ")":
                        quantity = item.find(")") + 1
                        startIndex = listSpace.getStart() + itemSpace.getStart()
                        question.removeAtIndex(startIndex, quantity, listSpaces)
                        startItemIndex = itemSpace.getStart()
                        for itemSpace2 in itemSpaces:
                            itemSpace2.incrementFrom(-1*quantity, startItemIndex)
                        errorIdentified = True
                if errorIdentified:
                    newComment = "Letras das Alternativas presentes nos items do XML"
                    newCommentXML = "<!-- "+newComment+" -->"
                    summaryAluno.incrementErrorType(newComment)
                    question.addCommentAfterIndex(listSpace.getOuterEnd(), newCommentXML, [], listSpaces)
                    #print(question.name)
                    #print(question.getInnerText(listSpace))

def verifyComments(question, summaryAluno):
    if(summaryAluno.name == "Vinícius Pereira Duarte"):
        commentSpaces = question.findAllTagSpacesBetween("<!--","-->")
        for commentSpace in commentSpaces:
            comment = question.getInnerText(commentSpace)
            corrigido = False
            middleString = "deveria ser"
            deveriaSerIndex = comment.find(middleString)
            if(deveriaSerIndex != -1):
                #print(comment)
                beforeWords = question.findAllBetween("\"","\"",comment[:deveriaSerIndex])
                afterWords = question.findAllBetween("\"","\"",comment[deveriaSerIndex+len(middleString):])
                lb = len(beforeWords)
                la = len(afterWords)
                if lb > 0 and la > 0:
                    beforeWord = beforeWords[lb - 1]
                    afterWord = afterWords[la - 1]

                    replaceIndex = question.text.rfind(beforeWord, 0, commentSpace.getOuterStart())
                    if(replaceIndex != -1):
                        question.removeAtIndex(replaceIndex, len(beforeWord), commentSpaces)
                        question.insertAtIndex(replaceIndex, afterWord, commentSpaces)
                        newComment = "Correção dos comentários com: Deveria ser"
                        summaryAluno.incrementErrorType(newComment)
                        corrigido = True
                        #print(question.text)
                        #print(beforeWord)
                        #print(afterWord)
            else:
                commentLR = util.removeWhiteSpaces(comment.lower())
                if(commentLR.find("itálico") != -1 or commentLR.find("italico") !=-1 ):
                    words = question.findAllBetween("\"","\"", comment)
                    l = len(words)
                    if(l > 0):
                        word = words[l - 1]
                        if(word != "et al" and word != "In"):
                            replaceIndex = question.text.rfind(word, 0, commentSpace.getOuterStart())
                            question.removeAtIndex(replaceIndex, len(word), commentSpaces)
                            newWord = "<italic>"+word+"</italic>"
                            question.insertAtIndex(replaceIndex, newWord, commentSpaces)
                            newComment = "Correção de comentários com: Faltou Itálico em"
                            summaryAluno.incrementErrorType(newComment)
                            corrigido = True
                            #print(comment)
                            #print(word)
                            #print(question.text)
                if(commentLR.find("negrito") != -1):
                    words = question.findAllBetween("\"","\"", comment)
                    l = len(words)
                    if(l > 0):
                        word = words[l - 1]
                        replaceIndex = question.text.rfind(word, 0, commentSpace.getOuterStart())
                        question.removeAtIndex(replaceIndex, len(word), commentSpaces)
                        newWord = "<b>"+word+"</b>"
                        question.insertAtIndex(replaceIndex, newWord, commentSpaces)
                        newComment = "Correção de comentários com: Faltou Negrito em"
                        summaryAluno.incrementErrorType(newComment)
                        corrigido = True
                        #print(comment)
                        #print(word)
                        #print(question.text)
            if not corrigido: pass
                #print(comment)
