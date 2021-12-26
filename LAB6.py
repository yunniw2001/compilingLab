#!/usr/bin/env python
# coding=utf-8
import sys

tokenList = []
resultList = []
ifNotes = 0
ifDef = 0
ifConst =0
ifexp = 0
SymbolStack = []
ExpInputStack = []
registerNum = 1
ExpTable = [[1, -1, -1, -1, 1, 1,1,1,1,-1], [1, 1, -1, -1, 1, 1,1,1,1,-1], [1, 1, -2, -2, 1, 1,1,1,1,1], [-1, -1, -1, -1, 0, -2,1,1,1,-1],
            [1, 1, -2, -2, 1, 1,1,1,1,1], [-1, -1, -1, -1, -2, -2,-1,-1,-1,-1],[-1, -1, -1, -1, 1, 1,1,1,1,-1],[-1, -1, -1, -1, 1, 1,-1,1,1,-1],[-1, -1, -1, -1, 1, 1,-1,-1,1,-1],[1, 1, -1, -1, 1, 1,1,1,1,-1]]
comparator = ['<','>','<=','>=','==','!=']
identifierList = []
constNum = 0
LVarRegister = 0
FuncIdent = ['getint', 'getch', 'putint', 'putch']
FuncAppear = []
CondWaitRegister = []
curBlockStart = []
continueBlock = []
waitBreakBlock=[]
varStart=0


def judge_alpha(token):
    global tokenList
    global resultList
    global identifierList
    global constNum
    global ifDef
    global ifConst
    global ifexp
    if token == 'int':
        ifDef =1
        tokenList.append(token)
    elif token == 'main':
        tokenList.append(token)
    elif token == 'return':
        tokenList.append(token)
    elif token in ['while','break','continue']:
        tokenList.append(token)
    elif token == 'const':
        constNum += 1
        ifConst =1
        tokenList.append(token)
    elif token == 'if' or token == 'else':
        tokenList.append(token)
    elif token in FuncIdent:
        pos = FuncIdent.index(token)
        FuncAppear[pos] = 1
        tokenList.append(token)
    elif token[0] == '_' or token[0].isalpha():
        if ifDef ==1 and not ifexp ==1:
            tmp = identifier()
            tmp.content = token
            identifierList.append(tmp)
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
    global ifDef
    global ifConst
    global ifexp
    for word in linelist:
        token = ''
        index = 0
        while index < len(word):
            # 判断是否为注释
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
            # 判断是否为标识符
            if word[index].isalpha() or word[index] == '_':
                while word[index].isalpha() or word[index].isdigit() or word[index] == '_':
                    token += word[index]
                    index = index + 1
                    if index >= len(word):
                        break
                judge_alpha(token)
                token = ''
                if index < len(word):
                    while word[index] == ';' or word[index] == '(' or word[index] == ')' or word[index] == '}' or word[
                        index] == '{':
                        if word[index] == ';' or word[index] == '{':
                            ifConst =0
                            ifDef = 0
                            ifexp =0
                        token = word[index]
                        tokenList.append(token)
                        token = ''
                        index += 1
                        if index >= len(word):
                            break
                index -= 1
            # 判断是否为数字
            elif word[index].isdigit():
                while word[index].isdigit() or word[index].isalpha():
                    token += word[index]
                    index = index + 1
                    if index >= len(word):
                        break
                index -= 1
                judge_number(token)
                token = ''
            # 判断是否为符号
            elif word[index] == ';' or word[index] == '(' or word[index] == ')' or word[index] == '}' or word[
                index] == '{' or word[index] == '-' or word[index] == '+' or (word[index] == '/' and (
                    len(word) == 1 or (not word[index + 1] == '/' and not word[index + 1] == '*'))) or word[
                index] == '*' or \
                    word[index] == '%' or (word[index] == '=' and len(word) == 1) or word[index] == ',' or (word[index] == '!' and not word[index+1]=='=') :
                token = word[index]
                tokenList.append(token)
                token = ''
                if word[index] == ';' or word[index] == '{':
                    ifConst = 0
                    ifDef = 0
                    ifexp =0
                if word[index] == '=':
                    ifexp =1
                if word[index] == ',':
                    ifexp = 0
            # 判断是否为逻辑符号
            elif word[index] == '<' or word[index] == '>':
                token = word[index]
                if index+1<len(word) and word[index+1] == '=':
                    index+=1
                    token+=word[index]
                tokenList.append(token)
                token = ''
            elif index+1<len(word) and(word[index] == '=' and word[index+1] == '=') or (word[index] == '&' and word[index+1] == '&') or (word[index] == '|' and word[index+1] == '|') or (word[index] == '!' and word[index+1] == '='):
                token = word[index] +word[index+1]
                tokenList.append(token)
                token = ''
                index+=2
            elif word[index] in comparator:
                token = word[index]
                tokenList.append(token)
                token = ''
                index +=1
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


def findIndexByContent(content):
    global identifierList
    i = len(identifierList)-1
    while i >=0 :
        if identifierList[i].content == content:
            return i
        i -= 1
    return -1


class Expression:
    isregister = False
    content = ''
    res = 0
    type = ''


class identifier:
    hasDefine = False
    register = ''
    content = ''
    type = ''
    value = 0


class Operator_precedence:
    top = 0

    def Operator_precedence_grammar(self, type):
        global SymbolStack
        global registerNum
        global ExpInputStack
        global ExpTable
        if len(ExpInputStack) == 0:
            sys.exit(-1)
        SymbolStack.append('#')
        ExpInputStack.append('#')
        self.top = 0
        if type == 'LVal':
            while self.top < len(ExpInputStack):
                input_symbol = ExpInputStack[self.top]
                if isinstance(input_symbol, Expression):
                    SymbolStack.append(input_symbol)
                    self.top += 1
                    continue
                if isinstance(SymbolStack[-1], Expression):
                    stackTop = -2
                    priority = self.judgePriority(SymbolStack[-2], input_symbol, -2)
                else:
                    stackTop = -1
                    if SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%':
                        if input_symbol == '*' or input_symbol == '/' or input_symbol == '%':
                            sys.exit(-1)
                    priority = self.judgePriority(SymbolStack[-1], input_symbol, -1)
                if SymbolStack[stackTop] == input_symbol and input_symbol == '#':
                    returnRes = SymbolStack[-1]
                    ExpInputStack = []
                    SymbolStack = []
                    return returnRes
                if priority == -2:
                    sys.exit(-1)
                elif priority == 1:
                    if SymbolStack[stackTop].isdigit():
                        tmp = Expression()
                        tmp.content = SymbolStack[stackTop]
                        tmp.type == 'i32'
                        SymbolStack.pop()
                        SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%':
                        try:
                            if isinstance(SymbolStack[-3], Expression):
                                num1 = SymbolStack[-3].content
                                if SymbolStack[-3].type == 'i1':
                                    num1 = trans_i1_to_i32(num1)
                            else:
                                num1 = SymbolStack[-3]
                        except IndexError:
                            sys.exit(-1)
                        if isinstance(SymbolStack[-1], Expression):
                            num2 = SymbolStack[-1].content
                            if SymbolStack[-1].type == 'i1':
                                num2 = trans_i1_to_i32(num2)
                        else:
                            num2 = SymbolStack[-1]
                        self.two_operator(SymbolStack[stackTop], num1, num2)
                        SymbolStack.pop()
                        SymbolStack.pop()
                        SymbolStack.pop()
                        tmp = Expression()
                        tmp.content = '%' + str(registerNum)
                        tmp.type = 'i32'
                        registerNum += 1
                        SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] == '+' or SymbolStack[stackTop] == '-' :
                        if SymbolStack[stackTop - 1] == '+' or SymbolStack[stackTop - 1] == '-' or SymbolStack[
                            stackTop - 1] == '#' or SymbolStack[stackTop - 1] == '(' or SymbolStack[stackTop-1] in ['>=','<=','<','>','==','||','&&','!=']:
                            if isinstance(SymbolStack[-1], Expression):
                                num = SymbolStack[-1].content
                                if SymbolStack[-1].type == 'i1':
                                    num = trans_i1_to_i32(num)
                            else:
                                num = SymbolStack[-1]
                            if SymbolStack[-2] == '-':
                                self.single_operator(SymbolStack[stackTop], num)
                                tmp = Expression()
                                tmp.content = '%' + str(registerNum)
                                if SymbolStack[stackTop] == '!':
                                    tmp.type = 'i1'
                                else:
                                    tmp.type = 'i32'
                                SymbolStack.pop()
                                SymbolStack.pop()
                                registerNum += 1
                                SymbolStack.append(tmp)
                            else:
                                tmp = SymbolStack[-1]
                                SymbolStack.pop()
                                SymbolStack.pop()
                                SymbolStack.append(tmp)
                        else:

                            if isinstance(SymbolStack[-3], Expression):
                                num1 = SymbolStack[-3].content
                                if SymbolStack[-3].type == 'i1':
                                    num1 = trans_i1_to_i32(num1)
                            else:
                                num1 = SymbolStack[-3]
                            if isinstance(SymbolStack[-1], Expression):
                                num2 = SymbolStack[-1].content
                                if SymbolStack[-1].type == 'i1':
                                    num2 = trans_i1_to_i32(num2)
                            else:
                                num2 = SymbolStack[-1]
                            self.two_operator(SymbolStack[stackTop], num1, num2)
                            SymbolStack.pop()
                            SymbolStack.pop()
                            SymbolStack.pop()
                            tmp = Expression()
                            tmp.type = 'i32'
                            tmp.content = '%' + str(registerNum)
                            registerNum += 1
                            SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] == '!':
                        if isinstance(SymbolStack[-1], Expression):
                            num = SymbolStack[-1].content
                            if SymbolStack[-1].type == 'i32':
                                num = trans_i32_to_i1(num)
                        else:
                            num = trans_i32_to_i1(SymbolStack[-1])
                        self.single_operator(SymbolStack[stackTop], num)
                        tmp = Expression()
                        tmp.content = '%' + str(registerNum)
                        tmp.type = 'i1'
                        SymbolStack.pop()
                        SymbolStack.pop()
                        registerNum += 1
                        SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] == ')':
                        SymbolStack.pop()
                        tmp = SymbolStack[-1]
                        SymbolStack.pop()
                        SymbolStack.pop()
                        SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] in comparator :
                        try:
                            if isinstance(SymbolStack[-3], Expression):
                                num1 = SymbolStack[-3].content
                                if SymbolStack[-3].type == 'i1':
                                    num1 = trans_i1_to_i32(num1)
                            else:
                                num1 = SymbolStack[-3]
                        except IndexError:
                            sys.exit(-1)
                        if isinstance(SymbolStack[-1], Expression):
                            num2 = SymbolStack[-1].content
                            if SymbolStack[-1].type == 'i1':
                                num2 = trans_i1_to_i32(num2)
                        else:
                            num2 = SymbolStack[-1]
                        self.two_operator(SymbolStack[stackTop], num1, num2)
                        SymbolStack.pop()
                        SymbolStack.pop()
                        SymbolStack.pop()
                        tmp = Expression()
                        tmp.type ='i1'
                        tmp.content = '%' + str(registerNum)
                        registerNum += 1
                        SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] == '&&' or SymbolStack[stackTop] == '||':
                        try:
                            if isinstance(SymbolStack[-3], Expression):
                                num1 = SymbolStack[-3].content
                                if SymbolStack[-3].type == 'i32':
                                    num1 = trans_i32_to_i1(num1)
                            else:
                                num1 = SymbolStack[-3]
                        except IndexError:
                            sys.exit(-1)
                        if isinstance(SymbolStack[-1], Expression):
                            num2 = SymbolStack[-1].content
                            if SymbolStack[-1].type == 'i32':
                                num2 = trans_i32_to_i1(num2)
                        else:
                            num2 = SymbolStack[-1]
                        self.two_operator(SymbolStack[stackTop], num1, num2)
                        SymbolStack.pop()
                        SymbolStack.pop()
                        SymbolStack.pop()
                        tmp = Expression()
                        tmp.type = 'i1'
                        tmp.content = '%' + str(registerNum)
                        registerNum += 1
                        SymbolStack.append(tmp)
                else:
                    SymbolStack.append(ExpInputStack[self.top])
                    self.top += 1
        elif type == 'ConstExp':
            while self.top < len(ExpInputStack):
                input_symbol = ExpInputStack[self.top]
                if isinstance(input_symbol, Expression):
                    SymbolStack.append(input_symbol)
                    self.top += 1
                    continue
                if isinstance(SymbolStack[-1], Expression):
                    stackTop = -2
                    priority = self.judgePriority(SymbolStack[-2], input_symbol, -2)
                else:
                    stackTop = -1
                    if SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%':
                        if input_symbol == '*' or input_symbol == '/' or input_symbol == '%':
                            sys.exit(-1)
                    priority = self.judgePriority(SymbolStack[-1], input_symbol, -1)
                if SymbolStack[stackTop] == input_symbol and input_symbol == '#':
                    returnRes = SymbolStack[-1].res
                    ExpInputStack = []
                    SymbolStack = []
                    return returnRes
                if priority == -2:
                    sys.exit(-1)
                elif priority == 1:
                    if SymbolStack[stackTop].isdigit():
                        tmp = Expression()
                        tmp.res = int(SymbolStack[stackTop])
                        SymbolStack.pop()
                        SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%':
                        try:
                            if isinstance(SymbolStack[-3], Expression):
                                num1 = SymbolStack[-3].res
                            else:
                                num1 = int(SymbolStack[-3])
                        except IndexError:
                            sys.exit(-1)
                        if isinstance(SymbolStack[-1], Expression):
                            num2 = SymbolStack[-1].res
                        else:
                            num2 = int(SymbolStack[-1])
                        tmp = Expression()
                        if SymbolStack[stackTop] == '*':
                            tmp.res = num1 * num2
                        elif SymbolStack[stackTop] == '/':
                            tmp.res = num1 // num2
                        elif SymbolStack[stackTop] == '%':
                            tmp.res = num1 % num2
                        SymbolStack.pop()
                        SymbolStack.pop()
                        SymbolStack.pop()
                        SymbolStack.append(tmp)
                    elif SymbolStack[stackTop] == '+' or SymbolStack[stackTop] == '-':
                        if SymbolStack[stackTop - 1] == '+' or SymbolStack[stackTop - 1] == '-' or SymbolStack[
                            stackTop - 1] == '#' or SymbolStack[stackTop - 1] == '(':
                            if isinstance(SymbolStack[-1], Expression):
                                num = SymbolStack[-1].res
                            else:
                                num = int(SymbolStack[-1])
                            if SymbolStack[-2] == '-':
                                SymbolStack.pop()
                                SymbolStack.pop()
                                tmp = Expression()
                                tmp.res = 0 - num
                                SymbolStack.append(tmp)
                            else:
                                tmp = SymbolStack[-1]
                                SymbolStack.pop()
                                SymbolStack.pop()
                                SymbolStack.append(tmp)
                        else:

                            if isinstance(SymbolStack[-3], Expression):
                                num1 = SymbolStack[-3].res
                            else:
                                num1 = int(SymbolStack[-3])
                            if isinstance(SymbolStack[-1], Expression):
                                num2 = SymbolStack[-1].res
                            else:
                                num2 = int(SymbolStack[-1])
                            if SymbolStack[stackTop] == '+':
                                tmp = Expression()
                                tmp.res = num1 + num2
                            else:
                                tmp = Expression()
                                tmp.res = num1 - num2
                            SymbolStack.pop()
                            SymbolStack.pop()
                            SymbolStack.pop()
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
        if stack_symbol in comparator:
            resultList.append('%'+str(registerNum)+' = icmp '+self.getComparatorChar(stack_symbol)+' i32 '+str(number1)+', '+str(number2)+'\n')
        elif stack_symbol == '&&':
            resultList.append('%'+str(registerNum)+' = and i1 '+str(number1)+','+str(number2)+'\n')
        elif stack_symbol == '||':
            resultList.append('%'+str(registerNum)+' = or i1 '+str(number1)+','+str(number2)+'\n')
        else:
            resultList.append('%' + str(registerNum) + ' = ' + self.get_operator_char(stack_symbol) + ' i32 ' + str(
            number1) + ', ' + str(number2) + '\n')

    def getComparatorChar(self,c):
        if c == '==':
            return 'eq'
        elif c== '!=':
            return 'ne'
        elif c == '<':
            return 'slt'
        elif c == '>':
            return 'sgt'
        elif c == '<=':
            return 'sle'
        elif c == '>=':
            return 'sge'


    def single_operator(self, stack_symbol, input_symbol):
        if stack_symbol == '!':
            resultList.append('%'+str(registerNum)+' = xor i1 '+str(input_symbol)+', true\n')
        else:
            resultList.append(
            '%' + str(registerNum) + ' = ' + self.get_operator_char(stack_symbol) + ' i32 ' + '0, ' + str(
                input_symbol) + '\n')

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
        elif c in comparator:
            return 6
        elif c == '&&':
            return 7
        elif c == '||':
            return 8
        elif c == '!':
            return 9

    def judgePriority(self, stack_symbol, input, stacktop):
        sy_idx = self.getIndex(stack_symbol)
        in_idx = self.getIndex(input)
        result = ExpTable[sy_idx][in_idx]
        if stacktop == -1:
            if stack_symbol == '+' or stack_symbol == '-':
                if input == '+' or input == '-':
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

def trans_i1_to_i32(oriRegister):
    global registerNum
    resultList.append('%'+str(registerNum)+' = zext i1 '+str(oriRegister)+' to i32\n')
    res = '%'+str(registerNum)
    registerNum+=1
    return res

def trans_i32_to_i1(oriRegister):
    global registerNum
    resultList.append('%'+str(registerNum)+' = icmp ne i32 '+str(oriRegister)+', 0\n')
    res = '%' + str(registerNum)
    registerNum += 1
    return res

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
                self.sym = self.tokenStream[self.tokenIndex]
                self.tokenIndex += 1
            return True
        else:
            sys.exit(-1)

    def CompUnit(self):
        global varStart
        i = 0
        varStart = len(identifierList)
        while self.readSym() and not tokenList[self.tokenIndex] == 'main':
            self.Decl('global')
        while i < len(FuncAppear):
            if FuncAppear[i] == 1:
                if FuncIdent[i] == 'putch' or FuncIdent[i] == 'putint':
                    resultList.append('declare void @' + FuncIdent[i] + '(i32)\n')
                else:
                    resultList.append('declare i32 @' + FuncIdent[i] + '()\n')
            i += 1
        if self.FuncDef():
            return 1
        sys.exit(-1)

    def FuncDef(self):
        self.FuncType()
        self.Ident('FuncDef')
        if self.sym == '(':
            resultList.append('(')
            if self.readSym():
                if self.sym == ')':
                    resultList.append(')')
                    if self.readSym():
                        self.Block(1,0)
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

    def Ident(self, fromRule):
        global curBlockStart
        if fromRule == 'FuncDef':
            if self.sym == 'main':
                resultList.append('@main')
                if self.readSym():
                    return 1
                else:
                    sys.exit(-1)
        elif fromRule == 'ConstDef':
            tmp = findIndexByContent(self.sym)
            if tmp == -1 or len(curBlockStart) == 0 or tmp <curBlockStart[len(curBlockStart)-1]:
                tmp = identifier()
                tmp.type = 'const'
                tmp.content = self.sym
                identifierList.append(tmp)
                return tmp
            else:
                sys.exit(-1)
                # identifierList[tmp].type = 'const'
                # return identifierList[tmp]
        elif fromRule == 'VarDef':
            tmp = findIndexByContent(self.sym)
            if tmp == -1 or len(curBlockStart) == 0 or tmp <curBlockStart[len(curBlockStart)-1]:
                tmp = identifier()
                tmp.type = 'LVal'
                tmp.content = self.sym
                identifierList.append(tmp)
                return tmp
            else:
                sys.exit(-1)
        elif fromRule == 'LVal':
            tmp = findIndexByContent(self.sym)
            if tmp == -1:
                sys.exit(-1)
            else:
                # identifierList[tmp].type = 'LVal'
                return identifierList[tmp]
        else:
            sys.exit(-1)

    def Block(self,n,pos):
        global identifierList
        global registerNum
        global LVarRegister
        if self.sym == '{':

            if n ==1:
                resultList.append('{\n')
                # 给变量分配空间
                i = 1
                LVarRegister = varStart - constNum
                while i <= varStart+1-constNum:
                    resultList.append('%' + str(i) + ' = alloca i32\n')
                    # identifierList[i].register = '%' + str(registerNum)
                    registerNum += 1
                    i += 1
                i=0
                while i<varStart:
                    identifierList.pop(0)
                    i+=1
            curBlockStart.append(len(identifierList))
            if self.readSym():
                while not self.sym == '}':
                    self.BlockItem()
                    if self.readSym():
                        continue
                    else:
                        sys.exit(-1)
                i = len(identifierList)-1
                while i>=curBlockStart[len(curBlockStart)-1]:
                    identifierList.pop(i)
                    i-=1
                curBlockStart.pop(len(curBlockStart)-1)
                if n ==1:
                    resultList.append('}')
                # elif n ==3:
                #     resultList[pos] += (str(registerNum) + '\n')
                return n
        sys.exit(-1)

    def BlockItem(self):
        if self.sym == 'const' or self.sym == 'int':
            return self.Decl()
        else:
            return self.Stmt(0)

    def Decl(self,fromBlock = 'default'):
        if self.sym == 'const':
            return self.ConstDecl(fromBlock)
        elif self.sym == 'int':
            return self.VarDecl(fromBlock)

    def ConstDecl(self,fromBlock):
        if self.sym == 'const':
            if self.readSym():
                self.Btype()
                if self.readSym():
                    self.ConstDef(fromBlock)
                    while not self.sym == ';':
                        if self.sym == ',':
                            if self.readSym():
                                self.ConstDef(fromBlock)
                                continue
                        sys.exit(-1)
                    if self.sym == ';':
                        return 1

    def VarDecl(self,fromBlock):
        global constNum
        self.Btype()
        if self.readSym():
            if fromBlock == 'global':
                constNum+=1
            self.VarDef(fromBlock)
            while not self.sym == ';':
                if self.sym == ',':
                    if self.readSym():
                        self.VarDef(fromBlock)
                        continue
                sys.exit(-1)
            if self.sym == ';':
                return 1

    def VarDef(self,fromBlock):
        global LVarRegister
        tmp = identifier()
        tmp = self.Ident('VarDef')
        if fromBlock == 'global':
            tmp.register = '@' +self.sym
        else:
            tmp.register = '%' + str(LVarRegister)
            LVarRegister -= 1
        if self.readSym():
            if self.sym == ',' or self.sym == ';':
                if fromBlock == 'global':
                    resultList.append(str(tmp.register)+' = dso_local global i32 0\n')
                return 1
            elif self.sym == '=':
                if self.readSym():
                    if fromBlock == 'global':
                        value = self.ConstInitVal('global')
                        resultList.append(str(tmp.register)+' = dso_local global i32 '+str(value)+'\n')
                    else:
                        storeRegister = self.InitVal().content
                        resultList.append('store i32 ' + str(storeRegister) + ', i32* ' + tmp.register + '\n')
                    return 1
        sys.exit(-1)

    def InitVal(self):
        return self.Exp()

    def Btype(self):
        if self.sym == 'int':
            return 1
        sys.exit(-1)

    def ConstDef(self,fromBlock):
        tmp = identifier()
        tmp = self.Ident('ConstDef')
        tmp.type = 'ConstVal'
        if self.readSym():
            if self.sym == '=':
                if self.readSym():
                    tmp.value = self.ConstInitVal(fromBlock)
                    return 1
        return

    def ConstInitVal(self,fromblock = 'default'):
        return self.ConstExp(fromblock)

    def ConstExp(self,fromBlock = 'default'):
        global registerNum
        while not self.sym == ';' and not self.sym == ',':
            if self.sym[0] == '_' or self.sym[0].isalpha():
                tmp = findIndexByContent(self.sym)
                if tmp == -1:
                    sys.exit(-1)
                else:
                    tmpVal = identifierList[tmp]
                    if tmpVal.type == 'ConstVal':
                        ExpInputStack.append(str(tmpVal.value))
                    else:
                        if fromBlock == 'global':
                            sys.exit(-1)
                        resultList.append('%' + str(registerNum) + ' = load i32, i32* ' + str(tmpVal.register) + '\n')
                        tmpExp = Expression()
                        tmpExp.isregister = True
                        tmpExp.type = 'i32'
                        tmpExp.content = '%' + str(registerNum)
                        registerNum += 1
                        ExpInputStack.append(tmpExp)
            else:
                ExpInputStack.append(self.sym)
            self.readSym()
        o_p = Operator_precedence()
        return o_p.Operator_precedence_grammar('ConstExp')

    def Stmt(self,curpos):
        global registerNum
        if self.sym == 'return':
            if self.readSym():
                while not self.sym == ';':
                    if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent:
                        tmp = findIndexByContent(self.sym)
                        if tmp == -1:
                            sys.exit(-1)
                        else:
                            tmpVal = identifierList[tmp]
                            if tmpVal.type == 'ConstVal':
                                ExpInputStack.append(str(tmpVal.value))
                            else:
                                resultList.append(
                                    '%' + str(registerNum) + ' = load i32, i32* ' + str(tmpVal.register) + '\n')
                                tmpExp = Expression()
                                tmpExp.type = 'i32'
                                tmpExp.isregister = True
                                tmpExp.content = '%' + str(registerNum)
                                registerNum += 1
                                ExpInputStack.append(tmpExp)
                    elif self.sym in FuncIdent:
                        self.Func()
                    else:
                        ExpInputStack.append(self.sym)
                    self.readSym()
                if self.sym == ';':
                    o_p = Operator_precedence()
                    res = o_p.Operator_precedence_grammar('LVal')
                    resultList.append('ret i32 ' + str(res.content) + '\n')
                    return 1
        elif (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent and not self.sym == 'if' and not self.sym == 'else' and not self.sym in ['while','continue','break']:
            tmpLVar = self.LVal()
            if not tmpLVar.type == 'LVal':
                sys.exit(-1)
            if self.readSym():
                if self.sym == '=':
                    if self.readSym():
                        tmp = self.Exp()
                        if self.sym == ';':
                            resultList.append('store i32 ' + str(tmp.content) + ', i32* ' + tmpLVar.register + '\n')
                            return 1
        elif self.sym in FuncIdent:
            self.Func()
        elif self.sym == 'continue':
            flag = self.sym
            self.readSym()
            if self.sym == ';':
                resultList.append('br label %'+str(continueBlock[len(continueBlock)-1])+'\n')
                return 1
            sys.exit(-1)
        elif self.sym == 'break:':
            self.readSym()
            if self.sym == ';':
                waitBreakBlock.append(len(resultList))
                resultList.append('br label %')
                return 1
            sys.exit(-1)
        elif self.sym == 'while':
            resultList.append('br label %'+str(registerNum)+'\n'+str(registerNum)+':\n')
            breakStart = len(waitBreakBlock)
            continueBlock.append(registerNum)
            whilePos = registerNum
            registerNum+=1
            if self.readSym():
                if self.sym == '(':
                    self.readSym()
                    res = self.Cond()
                    if res.type == 'i32':
                        res = trans_i32_to_i1(res.content)
                        resultList.append('br i1 ' + res + ',label %' + str(registerNum))
                    else:
                        resultList.append('br i1 ' + res.content + ',label %' + str(registerNum))
                    pos = len(resultList) - 1
                    resultList.append(str(registerNum) + ':\n')
                    registerNum += 1
                    if self.sym == ')':
                        self.readSym()
                        flag = self.Stmt(pos)
                        if not 'br' in resultList[-1]:
                            resultList.append('br label %'+str(whilePos)+'\n')
                        resultList[pos] += (', label %' + str(registerNum) + '\n')
                        resultList.append(str(registerNum) + ':\n')
                        i = len(waitBreakBlock) - 1
                        while i>=breakStart:
                            resultList[waitBreakBlock[-1]].append(str(registerNum)+'\n')
                            waitBreakBlock.pop(-1)
                            i-=1
                        registerNum += 1
                        self.tokenIndex -= 1
                        if len(continueBlock) > 0:
                            continueBlock.pop(len(continueBlock) - 1)
                        if self.sym == '}':
                            self.readSym()
                        return 1


        elif self.sym == 'if':
            if self.readSym():
                if self.sym == '(':
                    if self.readSym():
                        res = self.Cond()
                        if res.type == 'i32':
                            res = trans_i32_to_i1(res.content)
                            resultList.append('br i1 '+res+',label %'+str(registerNum))
                        else:
                            resultList.append('br i1 ' + res.content + ',label %' + str(registerNum))
                        pos = len(resultList)-1
                        resultList.append(str(registerNum)+':\n')
                        registerNum+=1
                        if self.sym == ')':
                            if self.readSym():
                                block_register = self.Stmt(pos)
                                self.readSym()
                                if self.sym == 'else':
                                    self.readSym()
                                    if not self.sym == 'if':
                                        if not 'br' in resultList[-1]:
                                            resultList.append('br label %')
                                            ifPos = len(resultList) - 1
                                        else:
                                            ifPos = -1
                                        resultList[pos]+=(', label %' + str(registerNum) + '\n')
                                        resultList.append(str(registerNum) + ':\n')
                                        registerNum+=1
                                        self.Stmt(ifPos)
                                        if not ifPos == -1:
                                            resultList[ifPos]+=(str(registerNum)+'\n')
                                        if not 'br' in resultList[-1]:
                                            resultList.append('br label %'+str(registerNum) + '\n')
                                        resultList.append(str(registerNum) + ':\n')
                                        registerNum+=1
                                    elif self.sym == 'if':
                                        if not 'br' in resultList[-1]:
                                            resultList.append('br label %')
                                            ifPos = len(resultList) - 1
                                        else:
                                            ifPos = -1
                                        resultList[pos] += (', label %' + str(registerNum) + '\n')
                                        resultList.append(str(registerNum) + ':\n')
                                        if not ifPos == -1:
                                            resultList[ifPos] += (str(registerNum) + '\n')
                                        registerNum+=1
                                        self.Stmt(pos)
                                        # resultList[pos] += (', label %' + str(registerNum) + '\n')
                                        # registerNum+=1
                                        return 1
                                    #resultList[ifPos] += (str(registerNum) + '\n')
                                    return 1

                                else:
                                    resultList[pos]+=(', label %' + str(registerNum) + '\n')
                                    if not 'br' in resultList[-1]:
                                        resultList.append('br label %'+str(registerNum)+'\n')
                                    resultList.append(str(registerNum) + ':\n')
                                    registerNum+=1
                                    self.tokenIndex-=1
                                    return 1
            sys.exit(-1)
        elif self.sym == '{':
            return self.Block(registerNum,curpos)
        else:
            while not self.sym == ';':
                self.readSym()
    def Cond(self):
        return self.LOrExp()

    def LOrExp(self):
        return self.CondJudgeIfEnd_exp()

    def LVal(self):
        return self.Ident('LVal')

    def Number(self):
        if self.sym.isdigit():
            if self.cur_register_num == 0:
                self.cur_register_content = int(self.sym)
            return 1
        else:
            sys.exit(-1)

    def Exp(self):
        # if self.AddExp():
        #     return 1;
        # else:
        #     sys.exit(-1)
        global registerNum
        while not self.sym == ';' and not self.sym == ',':
            if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent:
                tmp = findIndexByContent(self.sym)
                if tmp == -1:
                    sys.exit(-1)
                else:
                    tmpVal = identifierList[tmp]
                    if tmpVal.type == 'ConstVal':
                        ExpInputStack.append(str(tmpVal.value))
                    else:
                        resultList.append('%' + str(registerNum) + ' = load i32, i32* ' + str(tmpVal.register) + '\n')
                        tmpExp = Expression()
                        tmpExp.type = 'i32'
                        tmpExp.isregister = True
                        tmpExp.content = '%' + str(registerNum)
                        registerNum += 1
                        ExpInputStack.append(tmpExp)
            elif self.sym.isdigit():
                ExpInputStack.append(self.sym)
            elif self.sym in FuncIdent:
                res = self.Func()
                tmpExp = Expression()
                tmpExp.type = 'i32'
                tmpExp.isregister = True
                tmpExp.content = res
                ExpInputStack.append(tmpExp)
            else:
                ExpInputStack.append(self.sym)
            self.readSym()
        if self.sym == ';' or self.sym == ',':
            o_p = Operator_precedence()
            return o_p.Operator_precedence_grammar('LVal')

    def Func(self):
        global registerNum
        if self.sym == 'getint':
            if self.readSym():
                if self.sym == '(':
                    resultList.append('%' + str(registerNum) + ' = call i32 @getint()\n')
                    cur = '%' + str(registerNum)
                    registerNum += 1
                    if self.readSym():
                        if self.sym == ')':
                            return cur
        elif self.sym == 'getch':
            if self.readSym():
                if self.sym == '(':
                    resultList.append('%' + str(registerNum) + ' = call i32 @getch()\n')
                    cur = '%' + str(registerNum)
                    registerNum += 1
                    if self.readSym():
                        if self.sym == ')':
                            return cur
        elif self.sym == 'putint':
            if self.readSym():
                if self.sym == '(':
                    if self.readSym():
                        res = self.FuncJudgeIfEnd_Exp()
                        resultList.append('call void @putint(i32 ' + res.content + ')\n')
                        if self.sym == ')':
                            if self.readSym():
                                if self.sym == ';':
                                    return 1
        elif self.sym == 'putch':
            if self.readSym():
                if self.sym == '(':
                    if self.readSym():
                        res = self.FuncJudgeIfEnd_Exp()
                        resultList.append('call void @putch(i32 ' + res.content + ')\n')
                        if self.sym == ')':
                            if self.readSym():
                                if self.sym == ';':
                                    return 1

    def FuncJudgeIfEnd_Exp(self):
        global registerNum
        while not tokenList[self.tokenIndex] == ';':
            if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent:
                tmp = findIndexByContent(self.sym)
                if tmp == -1:
                    sys.exit(-1)
                else:
                    tmpVal = identifierList[tmp]
                    if tmpVal.type == 'ConstVal':
                        ExpInputStack.append(str(tmpVal.value))
                    else:
                        resultList.append(
                            '%' + str(registerNum) + ' = load i32, i32* ' + str(tmpVal.register) + '\n')
                        tmpExp = Expression()
                        tmpExp.type = 'i32'
                        tmpExp.isregister = True
                        tmpExp.content = '%' + str(registerNum)
                        registerNum += 1
                        ExpInputStack.append(tmpExp)
            elif self.sym.isdigit():
                ExpInputStack.append(self.sym)
            elif self.sym in FuncIdent:
                res = self.Func()
                tmpExp = Expression()
                tmpExp.type = 'i32'
                tmpExp.isregister = True
                tmpExp.content = res
                registerNum += 1
                ExpInputStack.append(tmpExp)
            else:
                ExpInputStack.append(self.sym)
            self.readSym()
        o_p = Operator_precedence()
        res = o_p.Operator_precedence_grammar('LVal')
        return res

    def CondJudgeIfEnd_exp(self):
        global registerNum
        while not tokenList[self.tokenIndex] == '{' and not (self.sym== ')' and findIndexByContent(tokenList[self.tokenIndex])== -1 and not tokenList[self.tokenIndex] in ['+','-','*','%','/','||','>=','<=','>','<','!','!=','==']):
            if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent and self.sym not in comparator and not self.sym == '&&' and not self.sym == '||':
                tmp = findIndexByContent(self.sym)
                if tmp == -1:
                    sys.exit(-1)
                else:
                    tmpVal = identifierList[tmp]
                    if tmpVal.type == 'ConstVal':
                        ExpInputStack.append(str(tmpVal.value))
                    else:
                        resultList.append(
                            '%' + str(registerNum) + ' = load i32, i32* ' + str(tmpVal.register) + '\n')
                        tmpExp = Expression()
                        tmpExp.type = 'i32'
                        tmpExp.isregister = True
                        tmpExp.content = '%' + str(registerNum)
                        registerNum += 1
                        ExpInputStack.append(tmpExp)
            elif self.sym.isdigit():
                ExpInputStack.append(self.sym)
            elif self.sym in FuncIdent:
                res = self.Func()
                tmpExp = Expression()
                tmpExp.isregister = True
                tmpExp.content = res
                registerNum += 1
                ExpInputStack.append(tmpExp)
            else:
                ExpInputStack.append(self.sym)
            self.readSym()
        o_p = Operator_precedence()
        res = o_p.Operator_precedence_grammar('LVal')
        return res
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
    FuncAppear = [0 for i in range(len(FuncIdent))]
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
    i = 0
    retRes = []
    i = 0
    ifret = 0
    while i<len(resultList):
        if 'ret' in resultList[i]:
            ifret = 1
            retRes.append(resultList[i])
            i+=1
            continue
        if ifret == 1:
            if 'br' in resultList[i]:
                ifret = 0
                i+=1
                continue
            ifret = 0
            retRes.append(resultList[i])
            i+=1
            continue
        retRes.append(resultList[i])
        i+=1

    for sym in retRes:
        outFile.write(sym)
    outFile.close()
    sys.exit(0)
