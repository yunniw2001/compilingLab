import sys

tokenList = []
resultList = []
ifNotes = 0


def judge_alpha(token):
    global tokenList
    global resultList
    if token == 'int':
        tokenList.append(token)
        resultList.append('define dsco_local i32 ')
    elif token == 'main':
        tokenList.append(token)
        resultList.append('@main')
    elif token == 'return':
        tokenList.append(token)
        resultList.append('ret ')
    else:
        sys.exit(-1)
    token = ''


def judge_number(token):
    index = 0
    toInt = 0
    global tokenList
    global resultList
    if token[0] != '0':
        tokenList.append(token)
        resultList.append('i32 ' + token)
    else:
        if len(token)>=2 and (token[1] == 'x' or token[1] == 'X'):
            token = token[2:]
            for mem in token:
                if (not mem.isdigit()) and not ('a' <= mem.lower() <= 'f'):
                    sys.exit(-1)
            token = str(int(token, base=16))
            tokenList.append(token)
            resultList.append('i32 '+token)
        else:
            for mem in token:
                if not ('0' <= mem <= '7'):
                    sys.exit(-1)
            token = str(int(token, base=8))
            tokenList.append(token)
            resultList.append('i32 ' + token)
    token = ''


def lexical_analysis(linelist):
    global tokenList
    global resultList
    global ifNotes
    for word in linelist:
        token = ''
        index = 0
        while index < len(word):
            if ifNotes:
                if word[index] == '*' and index <len(word)-1:
                    index +=1
                    if word[index] == '/':
                        ifNotes = 0
                        index+=1
                        continue
                    else:
                        index+=1
                        continue
                else:
                    index+=1
                    continue
            if word[index].isalpha():
                while word[index].isalpha():
                    token += word[index]
                    index = index + 1
                    if index >= len(word):
                        break
                judge_alpha(token)
                token = ''
                if index < len(word):
                    while word[index] == ';' or word[index] == '(' or word[index] == ')' or word[index] == '}' or word[index] == '{':
                        token = word[index]
                        tokenList.append(token)
                        resultList.append(token)
                        token = ''
                        index += 1
                        if index >=len(word):
                            break
                index-=1
            elif word[index].isdigit():
                while word[index].isdigit() or word[index].isalpha():
                    token += word[index]
                    index = index + 1
                    if index >= len(word):
                        break
                index -= 1
                judge_number(token)
                token = ''
            elif word[index] == ';' or word[index] == '(' or word[index] == ')' or word[index] == '}' or word[index] == '{':
                token = word[index]
                tokenList.append(token)
                resultList.append(token)
                token = ''
            elif word[index] == '/':
                index+=1
                if word[index] == '/':
                    return
                elif word[index] == '*':
                    if ifNotes:
                        sys.exit(-1)
                    else:
                        ifNotes = 1
                else:
                    sys.exit(-1)
            else:
                sys.exit(-1)
            index+=1

class syntax_analysis:
    tokenStream = []
    sym = ''
    tokenIndex = 0

    def __init__(self):
        self.tokenStream = tokenList

    def readSym(self):
        if self.tokenIndex< len(self.tokenStream):
            self.sym = self.tokenStream[self.tokenIndex]
            self.tokenIndex += 1
            return True
        else:
            return False

    def CompUnit(self):
        if self.readSym():
            self.FuncDef()
            return 1
        sys.exit(-1)

    def FuncDef(self):
        self.FuncType()
        self.Ident()
        if self.sym == '(':
            if self.readSym():
                if self.sym == ')':
                    if self.readSym():
                        self.Block()
                        return 1
        sys.exit(-1)


    def FuncType(self):
        if self.sym == 'int':
            if self.readSym():
                return 1
            else:
                sys.exit(-1)
        else:
            sys.exit(-1)

    def Ident(self):
        if self.sym == 'main':
            if self.readSym():
                return 1
            else:
                sys.exit(-1)
        else:
            sys.exit(-1)

    def Block(self):
        if self.sym == '{':
            if self.readSym():
                self.Stmt()
                if self.readSym():
                    if self.sym == '}':
                        return 1
                    else:
                        sys.exit(-1)
                else:sys.exit(-1)
            else:
                sys.exit(-1)
        else:
            sys.exit(-1)

    def Stmt(self):
        if self.sym == 'return':
            if self.readSym():
                self.Number()
                if self.readSym():
                    if self.sym == ';':
                        return 1
                    else:
                        sys.exit(-1)
                else:
                    sys.exit(-1)
            else:
                sys.exit(-1)
        else:
            sys.exit(-1)

    def Number(self):
        if self.sym.isdigit():
            return 1
        else:
            sys.exit(-1)
if __name__ == '__main__':
    # fileRoute = sys.argv[1]
    # file = open(fileRoute)
    # line = file.readline()
    # while line:
    #     lineList = line.split()
    #     lexicalAnalysis(lineList)
    #     line = file.readline()
    input = sys.argv[1]
    ir = sys.argv[2]
    # input = 'D:\大三上\编译原理\lab\in.txt'
    # ir = 'D:\大三上\编译原理\lab\out.txt'
    file = open(input)
    line = file.readline()
    while line:
        if ifNotes and ('*/' not in line):
            line = file.readline()
            continue
        lineList = line.split()
        lexical_analysis(lineList)
        resultList.append('\n')
        line = file.readline()
    if ifNotes:
        sys.exit(-1)
    s_a = syntax_analysis()
    s_a.CompUnit()
    outFile = open(ir,mode='w')
    for sym in resultList:
        outFile.write(sym)
    outFile.close()
    sys.exit(0)

