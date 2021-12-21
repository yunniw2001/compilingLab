import sys

tokenList = []
resultList = []
ifNotes = 0
SymbolStack = []
ExpInputStack = []
registerNum = 1
ExpTable = [[1, -1, -1, -1, 1, 1], [1, 1, -1, -1, 1, 1], [1, 1, -2, -2, 1, 1], [-1, -1, -1, -1, 0, -2],
            [1, 1, -2, -2, 1, 1], [-1, -1, -1, -1, -2, -2]]


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
        if len(token) >= 2 and (token[1] == 'x' or token[1] == 'X'):
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
                if word[index] == '*' and index < len(word) - 1:
                    index += 1
                    if word[index] == '/':
                        ifNotes = 0
                        index += 1
                        continue
                    else:
                        index += 1
                        continue
                else:
                    index += 1
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
                    while word[index] == ';' or word[index] == '(' or word[index] == ')' or word[index] == '}' or word[
                        index] == '{':
                        token = word[index]
                        tokenList.append(token)
                        token = ''
                        index += 1
                        if index >= len(word):
                            break
                index -= 1
            elif word[index].isdigit():
                while word[index].isdigit() or word[index].isalpha():
                    token += word[index]
                    index = index + 1
                    if index >= len(word):
                        break
                index -= 1
                judge_number(token)
                token = ''
            elif word[index] == ';' or word[index] == '(' or word[index] == ')' or word[index] == '}' or word[
                index] == '{' or word[index] == '-' or word[index] == '+' or (word[index] == '/' and (len(word) ==1 or (not word[index+1] =='/' and not word[index+1] == '*'))  ) or word[index] == '*' or \
                    word[index] == '%':
                token = word[index]
                tokenList.append(token)
                token = ''
            elif word[index] == '/':
                index += 1
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
            index += 1

class Expression:
    isregister: False
    content = ''

class Operator_precedence:
    top = 0


    def Operator_precedence_grammar(self):
        global SymbolStack
        global registerNum
        global ExpInputStack
        global ExpTable
        SymbolStack.append('#')
        ExpInputStack.append('#')
        self.top = 0
        while self.top < len(ExpInputStack):
            input_symbol = ExpInputStack[self.top]
            if isinstance(SymbolStack[-1],Expression):
                stackTop = -2
                priority = self.judgePriority(SymbolStack[-2], input_symbol,-2)
            else:
                stackTop = -1
                if SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%':
                    if input_symbol == '*' or input_symbol == '/' or input_symbol == '%':
                        sys.exit(-1)
                priority = self.judgePriority(SymbolStack[-1], input_symbol,-1)
            if SymbolStack[stackTop] == input_symbol and input_symbol == '#':
                return
            if priority == -2:
                sys.exit(-1)
            elif priority == 1:
                if SymbolStack[stackTop].isdigit():
                    tmp = Expression()
                    tmp.content = SymbolStack[stackTop]
                    SymbolStack.pop()
                    SymbolStack.append(tmp)
                elif SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%':
                    try:
                        if isinstance(SymbolStack[-3],Expression): num1 = SymbolStack[-3].content
                        else:
                            num1 = SymbolStack[-3]
                    except IndexError:
                        sys.exit(-1)
                    if isinstance(SymbolStack[-1],Expression): num2 = SymbolStack[-1].content
                    else:
                        num2 = SymbolStack[-1]
                    self.two_operator(SymbolStack[stackTop],num1,num2)
                    SymbolStack.pop()
                    SymbolStack.pop()
                    SymbolStack.pop()
                    tmp = Expression()
                    tmp.content = '%' +str(registerNum)
                    registerNum+=1
                    SymbolStack.append(tmp)
                elif SymbolStack[stackTop] =='+' or SymbolStack[stackTop] == '-':
                    if SymbolStack[stackTop-1] == '+' or SymbolStack[stackTop-1] == '-' or SymbolStack[stackTop-1] == '#' or SymbolStack[stackTop-1] == '(':
                        if isinstance(SymbolStack[-1],Expression):
                            num = SymbolStack[-1].content
                        else:
                            num = SymbolStack[-1]
                        if SymbolStack[-2] == '-':
                            self.single_operator(SymbolStack[stackTop],num)
                            SymbolStack.pop()
                            SymbolStack.pop()
                            tmp = Expression()
                            tmp.content = '%' +str(registerNum)
                            registerNum +=1
                            SymbolStack.append(tmp)
                        else:
                            tmp = SymbolStack[-1]
                            SymbolStack.pop()
                            SymbolStack.pop()
                            SymbolStack.append(tmp)
                    else:

                        if isinstance(SymbolStack[-3], Expression):
                            num1 = SymbolStack[-3].content
                        else:
                            num1 = SymbolStack[-3]
                        if isinstance(SymbolStack[-1], Expression):
                            num2 = SymbolStack[-1].content
                        else:
                            num2 = SymbolStack[-1]
                        self.two_operator(SymbolStack[stackTop], num1, num2)
                        SymbolStack.pop()
                        SymbolStack.pop()
                        SymbolStack.pop()
                        tmp = Expression()
                        tmp.content = '%' + str(registerNum)
                        registerNum += 1
                        SymbolStack.append(tmp)
                elif SymbolStack[stackTop] == ')':
                    SymbolStack.pop()
                    tmp = SymbolStack[-1]
                    SymbolStack.pop()
                    SymbolStack.pop()
                    SymbolStack.append(tmp)
            else:
                SymbolStack.append(ExpInputStack[self.top])
                self.top += 1

    def two_operator(self, stack_symbol, number1, number2):
        resultList.append('%' + str(registerNum) + ' = ' + self.get_operator_char(stack_symbol) + ' i32 ' + str(
            number1) + ', ' + str(number2) + '\n')

    def single_operator(self, stack_symbol, input_symbol):
        resultList.append(
            '%' + str(registerNum) + ' = ' + self.get_operator_char(stack_symbol) + ' i32 ' + '0, ' + str(input_symbol) + '\n')

    def getIndex(self, c):
        if c == '+' or c == '-':
            return 0
        elif c == '*' or c == '/' or c == '%':
            return 1
        elif c.isdigit() or c[0] == '%':
            return 2
        elif c == '(':
            return 3
        elif c == ')':
            return 4
        elif c == '#':
            return 5

    def judgePriority(self, stack_symbol, input,stacktop):
        sy_idx = self.getIndex(stack_symbol)
        in_idx = self.getIndex(input)
        result = ExpTable[sy_idx][in_idx]
        if stacktop == -1:
            if stack_symbol =='+' or stack_symbol == '-':
                if input == '+' or input =='-':
                    return -1
        return result

    def get_operator_char(self, c):
        if c == '+':
            return 'add'
        elif c == '-':
            return 'sub'
        elif c == '*':
            return 'mul'
        elif c == '/':
            return 'sdiv'
        elif c == '%':
            return 'srem'


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
        if self.tokenIndex < len(self.tokenStream):
            self.sym = self.tokenStream[self.tokenIndex]
            self.tokenIndex += 1
            while self.sym == '\n' and self.tokenIndex < len(self.tokenStream):
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
                else:
                    sys.exit(-1)
            else:
                sys.exit(-1)
        else:
            sys.exit(-1)

    def Stmt(self):
        if self.sym == 'return':
            if self.readSym():
                while not self.sym == ';':
                    ExpInputStack.append(self.sym)
                    self.readSym()
                if self.sym == ';':
                    o_p = Operator_precedence()
                    o_p.Operator_precedence_grammar()
                    resultList.append('ret i32 %' + str(registerNum-1))
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
        if self.sym == '+':
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
                            resultList.append('%' + str(self.cur_register_num) + ' = sub i32 0, ' + str(
                                self.cur_register_content) + '\n')
                            self.cur_register_content = 1
                        else:
                            self.cur_register_num = self.cur_register_num + 1
                            resultList.append('%' + str(self.cur_register_num) + ' = sub i32 0, %' + str(
                                self.cur_register_content) + '\n')
                            self.cur_register_content = self.cur_register_content + 1
                        return 1
            sys.exit(-1)
        elif self.sym == '(' or self.sym.isdigit():
            if self.PrimaryExp():
                return 1
            sys.exit(-1)
        sys.exit(-1)

    def PrimaryExp(self):
        if self.sym == '(':
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
    # fileRoute = sys.argv[1]
    # file = open(fileRoute)
    # line = file.readline()
    # while line:
    #     lineList = line.split()
    #     lexicalAnalysis(lineList)
    #     line = file.readline()
    input = sys.argv[1]
    ir = sys.argv[2]
    # input = 'D:\大三上\编译原理\compilingLab\in.txt'
    # ir = 'D:\大三上\编译原理\compilingLab\out.txt'
    file = open(input)
    line = file.readline()
    while line:
        # print(line)
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
    outFile = open(ir, mode='w')
    for sym in resultList:
        outFile.write(sym)
    outFile.close()
    sys.exit(0)
