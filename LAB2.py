import sys

tokenList = []
resultList = []
ifNotes = 0
SymbolStack = []
ExpInputStack = []
registerNum = 0
ExpTable=[[-1,-1,-1,-1,-2,1],[-1,-1,-1,-1,-2,1],[1,1,-2,-2,1,1],[-1,-1,-1,-1,0,-2],[1,1,-2,-2,1,1],[-1,-1,-1,-1,-2]]


def judge_alpha(token):
    global tokenList
    global resultList
    if token == 'int':
        tokenList.append(token)
    elif token == 'main':
        tokenList.append(token)
    elif token == 'return':
        tokenList.append(token)
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
    else:
        if len(token)>=2 and (token[1] == 'x' or token[1] == 'X'):
            token = token[2:]
            for mem in token:
                if (not mem.isdigit()) and not ('a' <= mem.lower() <= 'f'):
                    sys.exit(-1)
            token = str(int(token, base=16))
            tokenList.append(token)
        else:
            for mem in token:
                if not ('0' <= mem <= '7'):
                    sys.exit(-1)
            token = str(int(token, base=8))
            tokenList.append(token)
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
            elif word[index] == ';' or word[index] == '(' or word[index] == ')' or word[index] == '}' or word[index] == '{' or word[index] == '-' or word[index] == '+':
                token = word[index]
                tokenList.append(token)
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
# class Operator_precedence:
#
#     def Operator_precedence_grammar(self):
#         global SymbolStack
#         global registerNum
#         global ExpInputStack
#         if len(ExpInputStack) == 1 and ExpInputStack[0].isdigit():
#             res = ExpInputStack[0]
#             ExpInputStack = []
#             SymbolStack = []
#             return res
#         for symbol in ExpInputStack:
#             top = ExpInputStack[len(ExpInputStack)-1]
#             topIndex = self.getIndex(top)
#             symbolIndex = self.getIndex(symbol)
#             # if ExpTable[topIndex][symbolIndex] == 1:
#
#
#
#     def getIndex(c):
#         if c =='+':
#             return 0
#         elif c =='-':
#             return 1
#         elif c.isdigit():
#             return 2
#         elif c == '(':
#             return 3
#         elif c ==')':
#             return 4
#         elif c =='#':
#             return 5


class syntax_analysis:
    tokenStream = []
    sym = ''
    tokenIndex = 0
    # o_p = Operator_precedence()
    cur_register_content = 0
    cur_register_num = 0

    def __init__(self):
        self.tokenStream = tokenList

    def readSym(self):
        if self.tokenIndex< len(self.tokenStream):
            self.sym = self.tokenStream[self.tokenIndex]
            self.tokenIndex += 1
            while self.sym == '\n' and self.tokenIndex<len(self.tokenStream):
                resultList.append('\n')
                self.sym = self.tokenStream[self.tokenIndex]
                self.tokenIndex += 1
            return True
        else:
            sys.exit(-1)

    def CompUnit(self):
        if self.readSym():
            self.FuncDef()
            return 1
        sys.exit(-1)

    def FuncDef(self):
        self.FuncType()
        self.Ident()
        if self.sym == '(':
            resultList.append('(')
            if self.readSym():
                if self.sym == ')':
                    resultList.append(')')
                    if self.readSym():
                        self.Block()
                        return 1
        sys.exit(-1)


    def FuncType(self):
        if self.sym == 'int':
            resultList.append('define dso_local i32 ')
            if self.readSym():
                return 1
            else:
                sys.exit(-1)
        else:
            sys.exit(-1)

    def Ident(self):
        if self.sym == 'main':
            resultList.append('@main')
            if self.readSym():
                return 1
            else:
                sys.exit(-1)
        else:
            sys.exit(-1)

    def Block(self):
        if self.sym == '{':
            resultList.append('{')
            if self.readSym():
                self.Stmt()
                if self.readSym():
                    if self.sym == '}':
                        resultList.append('}')
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
                self.Exp()
            if self.readSym():
                if self.sym == ';':
                    resultList.append('ret i32 %'+str(self.cur_register_num))
                    return 1
        else:
            sys.exit(-1)

    def Number(self):
        if self.sym.isdigit():
            if self.cur_register_num == 0:
                self.cur_register_content = int(self.sym)
            return 1
        else:
            sys.exit(-1)
    def Exp(self):
        if self.AddExp():
            return 1;
        else:
            sys.exit(-1)

    def AddExp(self):
        if self.MulExp():
            return 1
        else:
            sys.exit(-1)

    def MulExp(self):
        if self.UnaryExp():
            return 1
        else:
            sys.exit(-1)

    def UnaryExp(self):
        if self.sym == '+' :
            if self.UnaryOp():
                if self.readSym():
                    if self.UnaryExp():
                        return 1;
            sys.exit(-1)
        elif self.sym == '-':
            if self.UnaryOp():
                if self.readSym():
                    if self.UnaryExp():
                        if self.cur_register_num == 0:
                            self.cur_register_num = self.cur_register_num + 1
                            resultList.append('%'+str(self.cur_register_num)+' = sub i32 0, '+str(self.cur_register_content)+'\n')
                            self.cur_register_content = 1
                        else:
                            self.cur_register_num = self.cur_register_num + 1
                            resultList.append('%' + str(self.cur_register_num) + ' = sub i32 0, %'+str(self.cur_register_content)+'\n')
                            self.cur_register_content = self.cur_register_content+1
                        return 1
            sys.exit(-1)
        elif self.sym == '(' or self.sym.isdigit():
            if self.PrimaryExp():
                return 1
            sys.exit(-1)
        sys.exit(-1)

    def PrimaryExp(self):
        if self.sym=='(':
            if self.readSym():
                if self.Exp():
                    if self.readSym():
                        if self.sym == ')':
                            return 1
            sys.exit(-1)
        elif self.sym.isdigit():
            if self.Number():
                return 1
            sys.exit(-1)
        sys.exit(-1)


    def UnaryOp(self):
        if self.sym == '+' or self.sym == '-':
            return 1
        sys.exit(-1)


if __name__ == '__main__':
    fileRoute = sys.argv[1]
    file = open(fileRoute)
    # line = file.readline()
    # while line:
    #     lineList = line.split()
    #     lexicalAnalysis(lineList)
    #     line = file.readline()
    # input = sys.argv[1]
    # ir = sys.argv[2]
    # input = 'D:\大三上\编译原理\lab\in.txt'
    # ir = 'D:\大三上\编译原理\lab\out.txt'
    # file = open(input)
    line = file.readline()
    while line:
        if ifNotes and ('*/' not in line):
            line = file.readline()
            continue
        lineList = line.split()
        lexical_analysis(lineList)
        tokenList.append('\n')
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

