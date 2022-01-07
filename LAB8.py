#!/usr/bin/env python
# coding=utf-8
import copy
import sys

tokenList = []
resultList = []
ifNotes = 0
ifDef = 0
ifConst =0
ifInt = 0
ifexp = 0
SymbolStack = []
ExpInputStack = []
registerNum = 0
ExpTable = [[1, -1, -1, -1, 1, 1,1,1,1,-1], [1, 1, -1, -1, 1, 1,1,1,1,-1], [1, 1, -2, -2, 1, 1,1,1,1,1], [-1, -1, -1, -1, 0, -2,1,1,1,-1],
            [1, 1, -2, -2, 1, 1,1,1,1,1], [-1, -1, -1, -1, -2, -2,-1,-1,-1,-1],[-1, -1, -1, -1, 1, 1,1,1,1,-1],[-1, -1, -1, -1, 1, 1,-1,1,1,-1],[-1, -1, -1, -1, 1, 1,-1,-1,1,-1],[1, 1, -1, -1, 1, 1,1,1,1,-1]]
comparator = ['<','>','<=','>=','==','!=']
identifierList = []
constNum = 0
LVarRegister = 0
FuncIdent = ['getint', 'getch', 'putint', 'putch','getarray','putarray']
FuncAppear = []
CondWaitRegister = []
curBlockStart = []
continueBlock = []
waitBreakBlock=[]
varStart=0
curFuncIndex = -1
arrayList = []
FuncList = []


def judge_alpha(token):
    global tokenList
    global resultList
    global identifierList
    global constNum
    global ifDef
    global ifConst
    global ifexp
    global ifInt
    global curFuncIndex
    if token == 'int':
        ifDef =1
        ifInt = 1
        tokenList.append(token)
    elif token == 'void':
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
        # 普通标识符 变量或常量
        if '[' not in token and '(' not in token:
            if ifDef ==1 and not ifexp ==1:
                tmp = identifier()
                tmp.content = token
                identifierList.append(tmp)
                if curFuncIndex>=0:
                    tmpList = copy.deepcopy(FuncList[curFuncIndex].curFuncIdentifierList)
                    tmpList.append(tmp)
                    FuncList[curFuncIndex].curFuncIdentifierList = tmpList
            tokenList.append(token)
        # 函数标识符
        elif '(' in token:
            firstLeft = token.index('(')
            name = token[0:firstLeft]
            if (ifDef == 1 and not ifexp == 1) or findFuncIndexByContent(name) == -1:
                if not name in FuncIdent:
                    tmp = My_Function()
                    tmp.content = name
                    curFuncIndex = len(FuncList)
                    FuncList.append(tmp)
                    tmp = identifier()
                    tmp.content = name
                    tmp.type = 'function'
                    identifierList.append(tmp)
                else:
                    pos = FuncIdent.index(name)
                    FuncAppear[pos] = 1
                    # tokenList.append(token)
            tokenList.append(name)
            tokenList.append('(')
        # 数组标识符
        else:
            firstLeft = token.index('[')
            name = token[0:firstLeft]
            if (ifDef == 1 and not ifexp == 1) or finArrayIndexByContent(name) == -1:
                tmp = My_array()
                tmp.content = name
                tmp.appearFunc = curFuncIndex
                arrayList.append(tmp)
                tmp = identifier()
                tmp.content = name
                tmp.type = 'array'
                identifierList.append(tmp)
                if curFuncIndex >= 0:
                    FuncList[curFuncIndex].curFuncIdentifierList.append(tmp)
            tokenList.append(name)
            tokenList.append('[')
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
    global ifInt
    m = 0
    while m <len(linelist):
        word = linelist[m]
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
                while word[index].isalpha() or word[index].isdigit() or word[index] == '_' or word[index] == '[':
                    token += word[index]
                    index = index + 1
                    if index >= len(word) or (word[index] in ['[','('] and not word[index] in FuncIdent):
                        # 判断是否为数组标识符
                        if index<len(word) and word[index] == '[':
                            token+=word[index]
                            index+=1
                        elif index>=len(word) and m <len(linelist)-1 and linelist[m+1][0] == '[':
                            token +='['
                            index = 1
                            m+=1
                            word = linelist[m]
                        # 判断是否为函数标识符
                        elif index<len(word) and word[index] == '(' and token not in ['while','if']:
                            token+=word[index]
                            index+=1
                        elif index>=len(word) and m <len(linelist)-1 and linelist[m+1][0] == '(' and token not in ['while','if']:
                            token +='('
                            index = 1
                            m+=1
                            word = linelist[m]
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
                            if word[index] == ';':
                                ifInt = 0
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
                    word[index] == '%' or (word[index] == '=' and len(word) == 1) or word[index] == ',' or (word[index] == '!' and not word[index+1]=='=') or word[index] in [']','[']:
                token = word[index]
                tokenList.append(token)
                token = ''
                if word[index] == ';' or word[index] == '{':
                    ifConst = 0
                    ifDef = 0
                    ifexp =0
                    if word[index] == ';':
                        ifInt = 0
                if word[index] == '=':
                    ifexp =1
                if word[index] == ',':
                    ifexp = 0
                    if ifInt == 1:
                        ifDef = 1
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
        m+=1


def findIndexByContent(content,tmpList):
    i = len(tmpList)-1
    while i >=0 :
        if tmpList[i].content == content:
            return i
        i -= 1
    if i ==-1:
        i = 0
        while i<len(identifierList):
            if identifierList[i].content == content and identifierList[i].area == 'global':
                return identifierList[i]
            i+=1
    return -1

def findIndexByContentOrigin(content,tmpList):
    i = len(tmpList)-1
    while i >=0 :
        if tmpList[i].content == content:
            return i
        i -= 1
    return -1

def finArrayIndexByContent(content):
    global arrayList
    i = 0
    while i < len(arrayList) :
        if arrayList[i].content == content:
            return i
        i += 1
    return -1
def findFuncIndexByContent(content):
    global FuncList
    i = 0
    while i < len(FuncList) :
        if FuncList[i].content == content:
            return i
        i += 1
    return -1

def getLocalArrayIndexByContent(content):
    global arrayList
    i = 0
    while i<len(arrayList):
        if arrayList[i].content == content and not arrayList[i].area == 'global':
            return i
        i+=1
    i = 0
    while i<len(arrayList):
        if arrayList[i].content == content:
            return i
        i+=1
    return -1

class Expression:
    isregister = False
    content = ''
    res = 0
    type = ''

class My_array:
    type = ''
    dim = []
    content = ''
    value = []
    hasDefine = False
    register = ''
    defPos = -1
    curElem = []
    appearFunc = ''
    area = 'default'
    def getTotalLength(self):
        res = 1
        for dims in self.dim:
            res*=dims
        return res
    def getCurLength(self,type = 'call'):
        global ExpInputStack
        i = 0
        res= 0
        if type == 'def':
            while i < len(self.dim)-1:
                res+=((self.curElem[i]-1)*self.dim[len(self.dim)-1-i])
                i+=1
            return res + self.curElem[-1]
        else:
            saveStack = copy.deepcopy(ExpInputStack)
            ExpInputStack = []
            while i < len(self.dim)-1:
                # ExpInputStack.append(self.curElem[i]*self.dim[len(self.dim)-1-i])
                if isinstance(self.curElem[i],Expression):
                    ExpInputStack.append(self.curElem[i])
                else:
                    ExpInputStack.append(str(self.curElem[i]))
                ExpInputStack.append('*')
                ExpInputStack.append(str(self.dim[len(self.dim)-1-i]))
                ExpInputStack.append('+')
                i+=1
            if isinstance(self.curElem[-1],Expression):
                ExpInputStack.append(self.curElem[-1])
            else:
                ExpInputStack.append(str(self.curElem[-1]))
            o_p = Operator_precedence()
            res = o_p.Operator_precedence_grammar('LVal')
            ExpInputStack = copy.deepcopy(saveStack)
            return res

class My_Function:
    content = ''
    paramType = []
    register = ''
    curFuncIdentifierList = []
    type = 'function'
    retType = 'void'
    param = []
    paramContent = []


class identifier:
    hasDefine = False
    register = ''
    content = ''
    type = ''
    value = 0
    area = 'default'
    toMyArray = My_array()
    toMyFunction = My_Function()
    hasPointer:False

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
                    if (SymbolStack[-2] == '+' or SymbolStack[-2] == '-' ) and SymbolStack[-3] in ['#','*','/']:
                        if isinstance(SymbolStack[-1], Expression):
                            num = SymbolStack[-1].content
                            if SymbolStack[-1].type == 'i1':
                                num = trans_i1_to_i32(num)
                        else:
                            num = SymbolStack[-1]
                        if SymbolStack[-2] == '-':
                            self.single_operator('-', num)
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
                    self.top += 1
                    if self.top == len(ExpInputStack):
                        self.top-=1
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
                    elif (SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%') and stackTop == -2:
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
                    elif (SymbolStack[stackTop] == '*' or SymbolStack[stackTop] == '/' or SymbolStack[stackTop] == '%') and stackTop == -1 and input_symbol in ['-','+']:
                        SymbolStack.append(ExpInputStack[self.top])
                        self.top += 1
                    elif SymbolStack[stackTop] == '+' or SymbolStack[stackTop] == '-' :
                        if SymbolStack[stackTop - 1] == '+' or SymbolStack[stackTop - 1] == '-' or SymbolStack[
                            stackTop - 1] == '#' or SymbolStack[stackTop - 1] == '(' or SymbolStack[stackTop-1] in ['>=','<=','<','>','==','||','&&','!=','*','/','%']:
                            if isinstance(SymbolStack[-1], Expression):
                                num = SymbolStack[-1].content
                                if SymbolStack[-1].type == 'i1':
                                    num = trans_i1_to_i32(num)
                            else:
                                num = SymbolStack[-1]
                            if SymbolStack[stackTop] == '-':
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
                    if SymbolStack[stackTop] == input_symbol and input_symbol == '#':
                        returnRes = SymbolStack[-1].res
                        ExpInputStack = []
                        SymbolStack = []
                        return returnRes
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
                            if SymbolStack[stackTop] == '-':
                                SymbolStack.pop()
                                SymbolStack.pop()
                                tmp = Expression()
                                tmp.res = 0 - num
                                SymbolStack.append(tmp)
                            elif SymbolStack[-2] == '#' and SymbolStack[-1] == '-':
                                SymbolStack.pop()
                                SymbolStack.pop()
                                tmp = Expression()
                                tmp.res = 0-num
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
    # 一个专门负责读入下一个token的函数
    def readSym(self):
        if self.tokenIndex < len(self.tokenStream):
            self.sym = self.tokenStream[self.tokenIndex]
            self.tokenIndex += 1
            while self.sym == '\n' and self.tokenIndex < len(self.tokenStream):
                self.sym = self.tokenStream[self.tokenIndex]
                self.tokenIndex += 1
            return True
        else:
            return False
    def minusSym(self):
        if self.tokenIndex >=0:
            self.sym = self.tokenStream[self.tokenIndex-2]
            self.tokenIndex -= 1
            while self.sym == '\n' and self.tokenIndex < len(self.tokenStream):
                self.sym = self.tokenStream[self.tokenIndex-2]
                self.tokenIndex -= 1
            return True
        else:
            return False
    def CompUnit(self,type = 'default'):
        global varStart
        global registerNum
        if type == 'origin':
            i = 0
            # while self.readSym() and not tokenList[self.tokenIndex] == 'main':
            #     self.Decl('global')FuncList[curFuncIndex].curFuncIdentifierList
            # 新增两个数组函数
            while i < len(FuncAppear):
                if FuncAppear[i] == 1:
                    if FuncIdent[i] == 'putch' or FuncIdent[i] == 'putint':
                        resultList.append('declare void @' + FuncIdent[i] + '(i32)\n')
                    elif FuncIdent[i] == 'getarray':
                        resultList.append('declare i32 @getarray(i32*)\n')
                    elif FuncIdent[i] == 'putarray':
                        resultList.append('declare void @putarray(i32, i32*)\n')
                    else:
                        resultList.append('declare i32 @' + FuncIdent[i] + '()\n')
                i += 1
            # 如果出现了数组，调用memset
            if len(arrayList)>0:
                resultList.append('declare void @memset(i32*, i32, i32)\n')
            while self.CompUnit():
                if self.tokenIndex+1 == len(tokenList):
                    break
            return 1
        # 针对LAB8做出的新修改
        else:
            self.readSym()
            if tokenList[self.tokenIndex+1] == '(':
                self.FuncDef()
                if 'ret' not in resultList[-2] and not (':' in resultList[-2] and 'ret' in resultList[-4]):
                    resultList[-1] = 'ret void\n'
                    resultList.append('}\n')
                elif ':' in resultList[-2] and 'ret' in resultList[-4]:
                    label = resultList[-2].index(':')
                    labelNum = resultList[-2][0:label]
                    resultList.pop(-1)
                    resultList[-1] = '}\n'
                    # for sen in resultList:
                    #     if ('%'+labelNum) in sen:
                    #         resultList.remove(sen)
                registerNum = 0
                return 1
            else:
                self.Decl('global',identifierList)
                return 1

        sys.exit(-1)

    def FuncDef(self):
        global registerNum
        global varStart
        retType = self.FuncType()
        res = self.Ident('FuncDef')
        res.retType = retType
        self.readSym()
        if self.sym == '(':
            resultList.append('(')
            if self.readSym():
                # 读入参数
                while not self.sym == ')':
                    self.FuncFParams(res.curFuncIdentifierList,res)
                if self.sym == ')':
                    resultList.append(')')
                    self.readSym()
                    if res == 1:
                        registerNum+=1
                        self.Block(1,0)
                        return 1
                    else:
                        self.Block(1,0,res)
                        return 1
        sys.exit(-1)

    def FuncFParams(self,tmpList,Func):
        while not self.sym == ')':
            self.FuncFParam(tmpList,Func)
            self.readSym()
            if not self.sym == ')':
                resultList.append(', ')
                if not self.sym == ',':
                    self.tokenIndex-=1
            else:
                break
            self.readSym()

    def FuncFParam(self,tmplist,Func):
        self.Btype()
        self.readSym()
        self.Ident('FuncDefParam',tmplist,Func)

    def FuncType(self):
        if self.sym == 'int':
            resultList.append('define dso_local i32 ')
            if self.readSym():
                return 'int'
        # 针对lab8做的新修改
        elif self.sym == 'void':
            resultList.append('define dso_local void ')
            if self.readSym():
                return 'void'
        sys.exit(-1)

    def Ident(self, fromRule,fromList='default',Func = 'default'):
        global curBlockStart
        global arrayList
        global curFuncIndex
        global varStart
        global registerNum
        if fromRule == 'FuncDef':
            curFuncIndex = findFuncIndexByContent(self.sym)
            tmp = identifier()
            tmp.type = 'function'
            tmp.content = self.sym
            tmp.toMyFunction = FuncList[findFuncIndexByContent(self.sym)]
            varStart = len(tmp.toMyFunction.curFuncIdentifierList)
            identifierList.append(tmp)
            # fromList.append(tmp)
            resultList.append('@'+self.sym)
            return tmp.toMyFunction
        elif fromRule == 'FuncDefParam':
            tmp = findIndexByContent(self.sym, fromList)
            if tmp == -1 or len(curBlockStart) == 0 or tmp < curBlockStart[len(curBlockStart) - 1]:
                tmp = identifier()
                tmp.type = 'LVal'
                tmp.content = self.sym
                tmp.register = '%' +str(registerNum)
                tmp.hasDefine = True
                if tokenList[self.tokenIndex] == '[':
                    tmp.type = 'array'
                    tmp.toMyArray = arrayList[getLocalArrayIndexByContent(self.sym)]
                    tmp.toMyArray.register = '%'+str(registerNum)
                    tmp.toMyArray.hasDefine = True
                    tmpParam = copy.deepcopy(Func.param)
                    tmpParam.append('i32*')
                    Func.param = tmpParam
                    resultList.append('i32* '+tmp.toMyArray.register)
                    while not self.sym == ']':
                        self.readSym()
                    tmpDimArray = ['']
                    self.readSym()
                    while not (self.sym == ',' or self.sym == ';' or self.sym == '=' or self.sym == ')'):
                        self.readSym()
                        tmpDim = self.ConstExp(fromList)
                        tmpDimArray.append(tmpDim)
                        self.readSym()
                    if self.sym == ')':
                        self.tokenIndex-=1
                    tmp.toMyArray.dim = tmpDimArray
                    tmp.toMyArray.curElem = [0 for i in range(len(tmp.toMyArray.dim))]
                else:
                    tmpParam = copy.deepcopy(Func.param)
                    tmpParam.append('i32')
                    Func.param = tmpParam
                    resultList.append('i32 ' + tmp.register)
                tmpParam = copy.deepcopy(Func.paramContent)
                tmpParam.append(tmp)
                Func.paramContent = tmpParam
                registerNum+=1
                identifierList.append(tmp)
                fromList.append(tmp)
                return tmp
        elif fromRule == 'ConstDef':
            tmp = findIndexByContent(self.sym)
            if tmp == -1 or len(curBlockStart) == 0 or tmp <curBlockStart[len(curBlockStart)-1]:
                tmp = identifier()
                tmp.type = 'const'
                tmp.content = self.sym
                if tokenList[self.tokenIndex] == '[':
                    tmp.type = 'array'
                    tmp.toMyArray = arrayList[finArrayIndexByContent(self.sym)]
                identifierList.append(tmp)
                fromList.append(tmp)
                return tmp
            else:
                sys.exit(-1)
                # identifierList[tmp].type = 'const'
                # return identifierList[tmp]
        elif fromRule == 'VarDef':
            tmp = findIndexByContent(self.sym,fromList)
            if tmp == -1 or len(curBlockStart) == 0 or isinstance(tmp,identifier) or tmp <curBlockStart[len(curBlockStart)-1]:
                tmp = identifier()
                tmp.type = 'LVal'
                tmp.content = self.sym
                if tokenList[self.tokenIndex] == '[':
                    tmp.type = 'array'
                    tmp.toMyArray = arrayList[getLocalArrayIndexByContent(self.sym)]
                identifierList.append(tmp)
                fromList.append(tmp)
                return tmp
            else:
                sys.exit(-1)
        elif fromRule == 'LVal':
            tmp = findIndexByContent(self.sym,fromList)
            if tmp == -1:
                sys.exit(-1)
            else:
                # identifierList[tmp].type = 'LVal'
                if not isinstance(tmp,identifier):
                    return fromList[tmp]
                else:
                    return tmp
        else:
            sys.exit(-1)

    def Block(self,n,pos,Func,fromFunc = 'default'):
        global identifierList
        global registerNum
        global LVarRegister
        global varStart
        global curFuncIndex
        if self.sym == '{':
            if not fromFunc == 'Stmt':
                registerNum+=1
            tmpidentifierList = Func.curFuncIdentifierList
            if n ==1:
                resultList.append('{\n')
                # 给变量分配空间
                i = 1
                if varStart > 0:
                    LVarRegister = varStart +1
                    while i <= varStart+1:
                        resultList.append('%' + str(registerNum) + ' = alloca i32\n')
                        # identifierList[i].register = '%' + str(registerNum)
                        registerNum += 1
                        i += 1
                i=0
                while i<varStart and len(tmpidentifierList)>0:
                    tmpidentifierList.pop(0)
                    i+=1
                i = 0
                while i<len(Func.param):
                    if Func.param[i] == 'i32*':
                        resultList.append('%'+str(registerNum)+' = alloca '+Func.param[i]+'\n')
                        resultList.append('store i32*  '+Func.paramContent[i].register+', i32* * %'+str(registerNum)+'\n')
                        registerNum+=1
                        resultList.append(
                            '%' + str(registerNum) + ' = load i32*, i32* * %' + str(registerNum - 1) + '\n')

                    else:
                        resultList.append('%' + str(registerNum) + ' = alloca ' + Func.param[i] + '\n')
                        resultList.append(
                            'store i32  ' + Func.paramContent[i].register + ', i32* %' + str(registerNum) + '\n')
                        # registerNum+=1
                        # resultList.append('%' + str(registerNum) + ' = load i32, i32* %' + str(registerNum - 1) + '\n')
                    Func.paramContent[i].register = '%' + str(registerNum)
                    Func.curFuncIdentifierList[findIndexByContent(Func.paramContent[i].content,Func.curFuncIdentifierList)].register = '%' + str(registerNum)
                    if Func.paramContent[i].type == 'array':
                        Func.paramContent[i].toMyArray.register = '%' + str(registerNum)
                    registerNum += 1
                    i+=1

            curBlockStart.append(len(tmpidentifierList))
            i = 0
            while i < len(arrayList) and n==1:
                if arrayList[i].appearFunc == curFuncIndex:
                    tmpArray = arrayList[i]
                    pos = findIndexByContentOrigin(tmpArray.content,tmpidentifierList)
                    if pos>=0:
                        anotherVersion = tmpidentifierList[pos]
                        if anotherVersion.hasDefine == True:
                            tmpArray.hasDefine = True
                    if not tmpArray.area == 'global' and not tmpArray.hasDefine:
                        resultList.append('%' + str(registerNum) + ' = alloca ')
                        arrayList[i].register = '%' + str(registerNum)
                        arrayList[i].defPos = len(resultList) - 1
                        tmp = identifier()
                        tmp.toMyArray = arrayList[i]
                        tmp.type = 'array'
                        tmpidentifierList.append(tmp)
                        registerNum += 1
                i += 1
            if self.readSym():
                while not self.sym == '}':
                    self.BlockItem(tmpidentifierList)
                    if self.readSym():
                        continue
                    else:
                        sys.exit(-1)
                i = len(tmpidentifierList)-1
                while i>=curBlockStart[len(curBlockStart)-1]:
                    tmpidentifierList.pop(i)
                    i-=1
                curBlockStart.pop(len(curBlockStart)-1)
                if n ==1:
                    resultList.append('}\n')
                # elif n ==3:
                #     resultList[pos] += (str(registerNum) + '\n')
                return n
        sys.exit(-1)

    def BlockItem(self,fromList):
        if self.sym == 'const' or self.sym == 'int':
            return self.Decl(fromList=fromList)
        else:
            return self.Stmt(0,fromList)

    def Decl(self,fromBlock = 'default',fromList= 'default'):
        if self.sym == 'const':
            return self.ConstDecl(fromBlock)
        elif self.sym == 'int':
            return self.VarDecl(fromBlock,fromList)

    def ConstDecl(self,fromBlock,fromList='default'):
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

    def VarDecl(self,fromBlock,fromList = 'default'):
        global constNum
        self.Btype()
        if self.readSym():
            if fromBlock == 'global':
                constNum+=1
            self.VarDef(fromBlock,fromList)
            while not self.sym == ';':
                if self.sym == ',':
                    if self.readSym():
                        self.VarDef(fromBlock,fromList)
                        continue
                sys.exit(-1)
            if self.sym == ';':
                return 1

    def VarDef(self,fromBlock,fromList='default'):
        global LVarRegister
        global registerNum
        tmp = identifier()
        tmp = self.Ident('VarDef',fromList)
        if fromBlock == 'global':
            tmp.area = 'global'
            if tmp.type == 'array':
                tmp.toMyArray.register = '@'+self.sym
                tmp.toMyArray.area = 'global'
            else:
                tmp.register = '@' +self.sym
        else:
            if not tmp.type == 'array':
                tmp.register = '%' + str(LVarRegister)
                LVarRegister -= 1
        if self.readSym():
            if self.sym == ',' or self.sym == ';':
                if fromBlock == 'global':
                    if not tmp.type == 'array':
                        resultList.append(str(tmp.register)+' = dso_local global i32 0\n')
                return 1
            elif self.sym == '=':
                if self.readSym():
                    if fromBlock == 'global':
                        value = self.ConstInitVal('global')
                        resultList.append(str(tmp.register)+' = dso_local global i32 '+str(value)+'\n')
                    else:
                        storeRegister = self.InitVal(fromList).content
                        resultList.append('store i32 ' + str(storeRegister) + ', i32* ' + tmp.register + '\n')
                    return 1
            elif self.sym == '[':
                tmpArray = tmp.toMyArray
                tmpArray.type = 'LVal'
                tmpDimArray = []
                while not (self.sym == ',' or self.sym == ';' or self.sym == '='):
                    self.readSym()
                    tmpDim = self.ConstExp(fromList)
                    tmpDimArray.append(tmpDim)
                    self.readSym()
                tmpArray.dim = tmpDimArray
                tmpArray.curElem = [0 for i in range(len(tmpArray.dim))]
                tmpArray.value = [0 for i in range(tmpArray.getTotalLength())]
                if not fromBlock == 'global':
                    anotherPos = arrayList[findIndexByContent(tmpArray.content, arrayList)]
                    if tmpArray.defPos < anotherPos.defPos:
                        tmpArray.defPos = anotherPos.defPos
                        tmpArray.register = anotherPos.register
                    resultList.append('%' + str(registerNum) + ' = getelementptr [' + str(
                        tmpArray.getTotalLength()) + ' x i32], [' + str(
                        tmpArray.getTotalLength()) + ' x i32]* ' + str(
                        tmpArray.register) + ', i32 0, i32 0\n')
                    resultList.append('call void @memset(i32* %'+str(registerNum)+', i32 0, i32 '+str(tmpArray.getTotalLength()*4)+')\n')
                    registerNum+=1
                    resultList[tmpArray.defPos]+=('['+str(tmpArray.getTotalLength())+' x i32]\n')
                if self.sym == '=':
                    # self.readSym()
                    tmpArray.curElem =  [0 for i in range(len(tmpArray.dim))]
                    tmpArray.value = [0 for i in range(tmpArray.getTotalLength())]
                    waitRight = 0
                    while not self.sym == ';' and not (waitRight == 0 and self.sym == ','):
                        self.readSym()
                        i = 0
                        while self.sym == '{':
                            waitRight+=1
                            tmpArray.curElem[i] +=1
                            i+=1
                            self.readSym()
                            tmpArray.curElem[-1] = 0

                        #resultList.append('%'+str(registerNum)+' = getelementptr i32, i32* '+tmpArray.register+', i32 '+str(tmpArray.getCurLength('def'))+'\n')
                        if not self.sym == '}':
                            if not fromBlock == 'global':
                                value = self.InitVal()
                                resultList.append('%' + str(registerNum) + ' = getelementptr [' + str(
                                    tmpArray.getTotalLength()) + ' x i32], [' + str(
                                    tmpArray.getTotalLength()) + ' x i32]* ' + str(tmpArray.register) + ', i32 0, i32 ' + str(
                                    tmpArray.getCurLength('def')) + '\n')
                                resultList.append('store i32 '+str(value.content)+', i32* %'+str(registerNum)+'\n')
                                registerNum+=1
                            else:
                                value = self.ConstInitVal('global')
                                tmpArray.value[tmpArray.getCurLength('def')] = value
                        while self.sym == '}':
                            waitRight-=1
                            self.readSym()
                        if self.sym == ',':
                            tmpArray.curElem[len(tmpArray.dim)-1] +=1
                    if fromBlock == 'global':
                        resultList.append(str(tmpArray.register)+' = dso_local global ['+str(tmpArray.getTotalLength())+' x i32] [')
                        i=0
                        while i<len(tmpArray.value):
                            resultList[-1]+=('i32 '+str(tmpArray.value[i]))
                            if not i == len(tmpArray.value)-1:
                                resultList[-1]+=', '
                            i+=1
                        resultList[-1]+=(']')
                        if len(tmpArray.value)<tmpArray.getTotalLength():
                            resultList[-1]+='zeroinitializer'
                        resultList[-1]+='\n'
                    if self.sym == ';':
                        return 1
                    elif self.sym == ',':
                        self.readSym()
                        self.VarDef(fromBlock,fromList)
                        return 1
                elif fromBlock == 'global':
                    tmpArray.curElem = [0 for i in range(len(tmpArray.dim))]
                    tmpArray.value = [0 for i in range(tmpArray.getTotalLength())]
                    resultList.append(str(tmpArray.register)+' = dso_local global ['+str(tmpArray.getTotalLength())+' x i32] zeroinitializer\n')
                    if self.sym == ',':
                        self.readSym()
                        self.VarDef('global',fromList)
                        return 1
                    elif self.sym == ';':
                        return 1
                elif self.sym == ',':
                    self.readSym()
                    self.VarDef(fromList)
                    return 1
                elif self.sym == ';':
                    return 1

        sys.exit(-1)

    def InitVal(self,fromList = 'default'):
        return self.Exp(fromList)

    def Btype(self):
        if self.sym == 'int':
            return 1
        sys.exit(-1)

    def ConstDef(self,fromBlock):
        tmp = identifier()
        tmp = self.Ident('ConstDef')
        tmp.type = 'ConstVal'
        tmp.area = 'global'
        if self.readSym():
            if self.sym == '=':
                if self.readSym():
                    tmp.value = self.ConstInitVal(fromBlock)
                    return 1
            elif self.sym == '[':
                tmp.type = 'array'
                tmpArray = tmp.toMyArray
                tmpArray.type = 'ConstVal'
                tmpDimArray = []
                while not (self.sym == ',' or self.sym == ';' or self.sym == '='):
                    self.readSym()
                    tmpDim = self.ConstExp()
                    tmpDimArray.append(tmpDim)
                    self.readSym()
                tmpArray.dim = tmpDimArray
                tmpArray.value = [0 for i in range(tmpArray.getTotalLength())]
                tmpArray.curElem = [0 for i in range(len(tmpArray.dim))]
                if self.sym == '=':
                    self.readSym()
                    tmpArray.curElem =  [0 for i in range(len(tmpArray.dim))]
                    waitRight = 0
                    while not self.sym == ';' and not (waitRight == 0 and self.sym == ',' and len(tmpArray.dim)>1):
                        self.readSym()
                        i = 0
                        while self.sym == '{':
                            waitRight+=1
                            tmpArray.curElem[i] += 1
                            i += 1
                            self.readSym()
                        while self.sym == '}':
                            waitRight -= 1
                            self.readSym()
                        if self.sym == ';':
                            break
                        value = self.ConstInitVal()
                        tmpArray.value[tmpArray.getCurLength('def')] = value
                        if self.sym == ',':
                            tmpArray.curElem[len(tmpArray.dim) - 1] += 1
                    if fromBlock == 'global':
                        tmpArray.area = 'global'
                        tmpArray.register = '@'+tmpArray.content
                        resultList.append(str(tmpArray.register)+' = dso_local constant ['+str(tmpArray.getTotalLength())+' x i32] [')
                        i = 0
                        while i < len(tmpArray.value):
                            resultList[-1] += ('i32 ' + str(tmpArray.value[i]))
                            if not i == len(tmpArray.value) - 1:
                                resultList[-1] += ', '
                            i += 1
                        resultList[-1]+=(']')
                        if len(tmpArray.value)<tmpArray.getTotalLength():
                            resultList[-1]+=' zeroinitializer'
                        resultList[-1]+=('\n')
                elif fromBlock == 'global':
                    tmpArray.register = '@' + tmpArray.content
                    resultList.append(str(tmpArray.register) + ' = dso_local constant [' + str(
                        tmpArray.getTotalLength()) + ' x i32] zeroinitializer\n')

        return

    def ConstInitVal(self,fromblock = 'default'):
        return self.ConstExp(fromblock)

    def ConstExp(self,tmpList,fromBlock = 'default'):
        global registerNum
        while not self.sym == ';' and not self.sym == ',' and not self.sym == ']' and not self.sym == '}':
            if self.sym[0] == '_' or self.sym[0].isalpha():
                tmp = findIndexByContent(self.sym)
                if tmp == -1:
                    sys.exit(-1)
                else:
                    tmpVal = tmpList[tmp]
                    if tmpVal.type == 'ConstVal':
                        if tmpVal.value<0:
                            ExpInputStack.append('-')
                            ExpInputStack.append(str(0-tmpVal.value))
                        else:
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

    def Stmt(self,curpos,tmpIdentifierlist):
        global registerNum
        if self.sym == 'return':
            if self.readSym():
                if self.sym == ';':
                    resultList.append('ret void\n')
                    return 1
                # while not self.sym == ';':
                #     if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent and not findFuncIndexByContent(self.sym)>=0:
                #         tmp = findIndexByContent(self.sym,tmpIdentifierlist)
                #         if tmp == -1:
                #             sys.exit(-1)
                #         else:
                #             tmpVal = tmpIdentifierlist[tmp]
                #             if tmpVal.type == 'ConstVal':
                #                 ExpInputStack.append(str(tmpVal.value))
                #             else:
                #                 resultList.append(
                #                     '%' + str(registerNum) + ' = load i32, i32* ' + str(tmpVal.register) + '\n')
                #                 tmpExp = Expression()
                #                 tmpExp.type = 'i32'
                #                 tmpExp.isregister = True
                #                 tmpExp.content = '%' + str(registerNum)
                #                 registerNum += 1
                #                 ExpInputStack.append(tmpExp)
                #     elif self.sym in FuncIdent or findFuncIndexByContent(self.sym)>=0:
                #         res = self.Func(tmpIdentifierlist)
                #         self.tokenIndex-=1
                #         tmpExp = Expression()
                #         tmpExp.type = 'i32'
                #         tmpExp.isregister = True
                #         tmpExp.content = '%' + res
                #         registerNum += 1
                #         ExpInputStack.append(tmpExp)
                #     else:
                #         ExpInputStack.append(self.sym)
                #     self.readSym()
                else:
                    res = self.Exp(tmpIdentifierlist)
                    resultList.append('ret i32 ' + str(res.content) + '\n')
                    return 1

        elif (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent and findFuncIndexByContent(self.sym) == -1 and not self.sym == 'if' and not self.sym == 'else' and not self.sym in ['while','continue','break']:
            tmpLVar = self.LVal(tmpIdentifierlist)
            # if not tmpLVar.type == 'LVal' and not :
            #     sys.exit(-1)
            if self.readSym():
                if self.sym == '=':
                    if self.readSym():
                        tmp = self.Exp(tmpIdentifierlist)
                        if self.sym == ';':
                            resultList.append('store i32 ' + str(tmp.content) + ', i32* ' + tmpLVar.register + '\n')
                            return 1
                elif self.sym == '[':
                    tmpArray = tmpLVar.toMyArray
                    i=0
                    while not (self.sym == ',' or self.sym == ';' or self.sym == '='):
                        self.readSym()
                        tmpDim = self.Exp(tmpIdentifierlist)
                        tmpArray.curElem[i] = tmpDim
                        i+=1
                        self.readSym()
                    if self.sym == '=':
                        self.readSym()
                        saveCurElem = copy.deepcopy(tmpArray.curElem)
                        res = self.Exp(tmpIdentifierlist)
                        tmpArray.curElem = saveCurElem
                        pos =tmpArray.getCurLength('call').content
                        if findIndexByContentOrigin(tmpArray.content,FuncList[curFuncIndex].paramContent)==-1:
                            resultList.append('%' + str(registerNum) + ' = getelementptr [' + str(
                                tmpArray.getTotalLength()) + ' x i32], [' + str(
                                tmpArray.getTotalLength()) + ' x i32]* ' + str(
                                tmpArray.register) + ', i32 0, i32 ' + str(pos) + '\n')
                        else:
                            resultList.append('%' + str(registerNum) + ' = getelementptr i32, i32* ' + str(
                            tmpArray.register) +',i32 '+ str(pos) + '\n')
                        # resultList.append('%' + str(registerNum + 1) + ' = load i32, i32* %' + str(registerNum) + '\n')
                        # registerNum += 1
                        resultList.append('store i32 ' + str(res.content) + ', i32* %' + str(registerNum) + '\n')
                        registerNum+=1
        elif self.sym in FuncIdent or findFuncIndexByContent(self.sym)>=0:
            self.Func(tmpIdentifierlist)
        elif self.sym == 'continue':
            flag = self.sym
            self.readSym()
            if self.sym == ';':
                resultList.append('br label %'+str(continueBlock[len(continueBlock)-1])+'\n')
                return 1
            sys.exit(-1)
        elif self.sym == 'break':
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
                    res = self.Cond(tmpIdentifierlist)
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
                        flag = self.Stmt(pos,tmpIdentifierlist)
                        if not 'br' in resultList[-1]:
                            resultList.append('br label %'+str(whilePos)+'\n')
                        resultList[pos] += (', label %' + str(registerNum) + '\n')
                        resultList.append(str(registerNum) + ':\n')
                        i = len(waitBreakBlock) - 1
                        while i>=breakStart:
                            resultList[waitBreakBlock[-1]]+=(str(registerNum)+'\n')
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
                        res = self.Cond(tmpIdentifierlist)
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
                                block_register = self.Stmt(pos,tmpIdentifierlist)
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
                                        self.Stmt(ifPos,tmpIdentifierlist)
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
                                        registerNum+=1
                                        self.Stmt(pos,tmpIdentifierlist)
                                        registerNum-=1
                                        if not ifPos == -1:
                                            resultList[ifPos] += (str(registerNum) + '\n')
                                        registerNum += 1

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
            return self.Block(registerNum,curpos,FuncList[curFuncIndex],'Stmt')
        else:
            while not self.sym == ';':
                self.readSym()
    def Cond(self,fromList):
        return self.LOrExp(fromList)

    def LOrExp(self,fromList):
        return self.CondJudgeIfEnd_exp(fromList)

    def LVal(self,fromList = 'default'):
        return self.Ident('LVal',fromList)

    def Number(self):
        if self.sym.isdigit():
            if self.cur_register_num == 0:
                self.cur_register_content = int(self.sym)
            return 1
        else:
            sys.exit(-1)

    def getArrayElem(self,tmparray):
        i = 0
        while i <len(tmparray.dim):
            self.readSym()
            while not self.sym == ']':
                self.readSym()
                res = self.ConstExp()
                tmparray.curElem[i] = res
            i+=1
        return tmparray.getCurLength('call')

    def Exp(self,tmpIdentifierList):
        # if self.AddExp():
        #     return 1;
        # else:
        #     sys.exit(-1)
        global registerNum
        global ExpInputStack
        while not self.sym == ';' and not self.sym == ',' and not self.sym == ']' and not self.sym == '}':
            if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent and not findFuncIndexByContent(self.sym)>=0:
                tmp = findIndexByContent(self.sym,tmpIdentifierList)
                if tmp == -1:
                    tmp = findFuncIndexByContent(self.sym)
                    if tmp == -1:
                        sys.exit(-1)
                    else:
                        tmpVal = FuncList[tmp]
                else:
                    if not isinstance(tmp,identifier):
                        tmpVal = tmpIdentifierList[tmp]
                    else:
                        tmpVal = tmp
                if tmpVal.type == 'ConstVal':
                    ExpInputStack.append(str(tmpVal.value))
                elif tmpVal.type == 'array':
                    tmpArray = tmpVal.toMyArray
                    if tmpArray.type == 'const':
                        ExpInputStack.append(tmpArray.value[self.getArrayElem(tmpArray)])
                    else:
                        saveExp = ExpInputStack
                        ExpInputStack = []
                        i=0
                        self.readSym()
                        while self.sym == '[':
                            self.readSym()
                            tmpArray.curElem[i] = self.Exp(tmpIdentifierList)
                            i+=1
                            self.readSym()
                        ExpInputStack = saveExp
                        # resultList.append('%' + str(registerNum) + ' = getelementptr i32, i32* ' + str(
                        #     tmpArray.register) + ', i32 ' + str(tmpArray.getCurLength('call')) + '\n')
                        pos = tmpArray.getCurLength('call').content
                        if findIndexByContentOrigin(tmpVal.content,FuncList[curFuncIndex].paramContent)==-1:
                            resultList.append('%' + str(registerNum) + ' = getelementptr [' + str(
                                tmpArray.getTotalLength()) + ' x i32], [' + str(
                                tmpArray.getTotalLength()) + ' x i32]* ' + str(
                                tmpArray.register) + ', i32 0, i32 ' + str(pos) + '\n')
                        else:
                            resultList.append('%' + str(registerNum) + ' = getelementptr i32, i32* ' + str(
                                tmpArray.register) + ',i32 ' + str(pos) + '\n')
                        resultList.append('%'+str(registerNum+1)+' = load i32, i32* %'+str(registerNum)+'\n')
                        registerNum+=1
                        tmpExp = Expression()
                        tmpExp.type = 'i32'
                        tmpExp.isregister = True
                        tmpExp.content = '%' + str(registerNum)
                        registerNum += 1
                        ExpInputStack.append(tmpExp)
                        self.tokenIndex-=1
                elif tmpVal.type == 'function':
                    resultList.append('%' + str(registerNum) + ' = call i32 @' + str(tmpVal.content) + '(')
                    tmpExp = Expression()
                    tmpExp.type = 'i32'
                    tmpExp.isregister = True
                    tmpExp.content = '%' + str(registerNum)
                    registerNum += 1
                    ExpInputStack.append(tmpExp)
                    while not self.sym == ')':
                        self.readSym()
                    resultList.append(')\n')
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
            elif self.sym in FuncIdent or findFuncIndexByContent(self.sym)>=0:
                saveExp = copy.deepcopy(ExpInputStack)
                ExpInputStack=[]
                res = self.Func(tmpIdentifierList)
                ExpInputStack = saveExp
                tmpExp = Expression()
                tmpExp.type = 'i32'
                tmpExp.isregister = True
                tmpExp.content = '%'+ res
                ExpInputStack.append(tmpExp)
                if self.sym == ';':
                    self.tokenIndex-=1
            else:
                ExpInputStack.append(self.sym)
            self.readSym()
        # if self.sym == ';' or self.sym == ',':
        o_p = Operator_precedence()
        return o_p.Operator_precedence_grammar('LVal')

    def Func(self,fromList = 'default'):
        global registerNum
        global resultList
        global ExpInputStack
        if self.sym == 'getint':
            if self.readSym():
                if self.sym == '(':
                    resultList.append('%' + str(registerNum) + ' = call i32 @getint()\n')
                    cur = str(registerNum)
                    registerNum += 1
                    if self.readSym():
                        if self.sym == ')':
                            return cur
        elif self.sym == 'getch':
            if self.readSym():
                if self.sym == '(':
                    resultList.append('%' + str(registerNum) + ' = call i32 @getch()\n')
                    cur = str(registerNum)
                    registerNum += 1
                    if self.readSym():
                        if self.sym == ')':
                            return cur
        elif self.sym == 'putint':
            if self.readSym():
                if self.sym == '(':
                    if self.readSym():
                        res = self.FuncJudgeIfEnd_Exp(fromList)
                        resultList.append('call void @putint(i32 ' + res.content + ')\n')
                        if self.sym == ')':
                            if self.readSym():
                                if self.sym == ';':
                                    return 1
        elif self.sym == 'putch':
            if self.readSym():
                if self.sym == '(':
                    if self.readSym():
                        res = self.FuncJudgeIfEnd_Exp(fromList)
                        resultList.append('call void @putch(i32 ' + res.content + ')\n')
                        if self.sym == ')':
                            if self.readSym():
                                if self.sym == ';':
                                    return 1
        elif self.sym == 'putarray':
            if self.readSym():
                if self.sym == '(':
                    if self.readSym():
                        res1 = self.FuncJudgeIfEnd_Exp(fromList)
                        self.readSym()
                        res2 = self.FuncJudgeIfEnd_Exp(fromList,False)
                        resultList.append('call void @putarray(i32 ' + res1.content)
                        resultList.append(', i32* '+res2.content+')\n')
                        if self.sym == ')':
                            if self.readSym():
                                if self.sym == ';':
                                    return 1
        elif self.sym == 'getarray':
            if self.readSym():
                if self.sym == '(':
                    if self.readSym():
                        res = self.FuncJudgeIfEnd_Exp(fromList,False)
                        resultList.append('%'+str(registerNum)+' = call i32 @getarray(i32* ' + res.content + ')\n')
                        registerNum+=1
                        if self.sym == ')':
                            self.readSym()
                            return str(registerNum-1)
        else:
            name = self.sym
            tmpFunc = FuncList[findFuncIndexByContent(name)]
            if self.readSym():
                if self.sym == '(':
                    tmpParamRegister = []
                    i = 0
                    if len(tmpFunc.param)>0:
                        while self.readSym():
                            if i>= len(tmpFunc.param):
                                while not self.sym in [';',',',')']:
                                    self.minusSym()
                                    self.minusSym()
                                    self.readSym()
                                if self.sym in [';',',',')']:
                                    break
                                sys.exit(-1)
                            if i == len(tmpFunc.param)-1:
                                flag = True
                            else:
                                flag = False
                            if tmpFunc.param[i] == 'i32*':
                                saveExp = copy.deepcopy(ExpInputStack)
                                ExpInputStack = []
                                res = self.FuncJudgeIfEnd_Exp(fromList,False,flag)
                                ExpInputStack = saveExp
                            else:
                                saveExp = copy.deepcopy(ExpInputStack)
                                res = self.FuncJudgeIfEnd_Exp(fromList,ifLast=flag)
                                ExpInputStack = saveExp
                            i+=1
                            tmpParamRegister.append(res.content)
                            if self.sym == ')':
                                break
                            if self.sym in ['+','==','*']:
                                self.tokenIndex-=1
                                break
                    else:
                        self.readSym()
                        self.readSym()
                    if tmpFunc.retType == 'void':
                        resultList.append('call void @'+name +'(')
                        retRes = 1
                    else:
                        resultList.append('%'+str(registerNum)+' = call i32 @'+name+'(')
                        retRes = str(registerNum)
                        registerNum+=1
                    i = 0
                    if len(tmpParamRegister) == len(tmpFunc.param):
                        while i<len(tmpFunc.param):
                            resultList+=(tmpFunc.param[i]+' '+tmpParamRegister[i])
                            if i <len(tmpFunc.param)-1:
                                resultList+=(', ')
                            i+=1
                        resultList+=(')\n')
                    return retRes

    def FuncJudgeIfEnd_Exp(self,tmpIdentifierList,ifNeedLoad = True,ifLast = False):
        global registerNum
        global ExpInputStack
        waitRight = 0
        while not tokenList[self.tokenIndex] == ';' and not self.sym == ',' and not self.sym == ';':
            if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent and not findFuncIndexByContent(self.sym)>=0:
                tmp = findIndexByContent(self.sym, tmpIdentifierList)
                if tmp == -1:
                    tmp = findFuncIndexByContent(self.sym)
                    if tmp == -1:
                        sys.exit(-1)
                    else:
                        tmpVal = FuncList[tmp]
                else:
                    if not  isinstance(tmp,identifier):
                        tmpVal = tmpIdentifierList[tmp]
                    else:
                        tmpVal = tmp
                if tmpVal.type == 'ConstVal':
                    ExpInputStack.append(str(tmpVal.value))
                elif tmpVal.type == 'array':
                    saveExp = ExpInputStack
                    tmp_Array = tmpVal.toMyArray
                    ExpInputStack = saveExp
                    if tmp_Array.type == 'ConstVal':
                        save_Exp = copy.deepcopy(ExpInputStack)
                        ExpInputStack =  []
                        res = tmp_Array.value[self.getArrayElem(tmp_Array)]
                        ExpInputStack = copy.deepcopy(save_Exp)
                        ExpInputStack.append(str(res))
                    else:
                        saveExp = copy.deepcopy(ExpInputStack)
                        i = 0
                        ExpInputStack = []
                        self.readSym()
                        # if not self.sym == '[':
                        #     sys.exit(-1)
                        tmp_Array.curElem = [0 for i in range(len(tmp_Array.dim))]
                        while self.sym == '[':
                            self.readSym()
                            tmp_Array.curElem[i] = self.Exp(tmpIdentifierList)
                            i += 1
                            self.readSym()
                        ExpInputStack = copy.deepcopy(saveExp)
                        # resultList.append('%' + str(registerNum) + ' = getelementptr i32, i32* ' + str(
                        #     tmpArray.register) + ', i32 ' + str(tmpArray.getCurLength('call')) + '\n')
                        pos =tmp_Array.getCurLength('call').content
                        if findIndexByContentOrigin(tmpVal.content,FuncList[curFuncIndex].paramContent)==-1:
                            resultList.append('%' + str(registerNum) + ' = getelementptr [' + str(
                                tmp_Array.getTotalLength()) + ' x i32], [' + str(
                                tmp_Array.getTotalLength()) + ' x i32]* ' + str(
                                tmp_Array.register) + ', i32 0, i32 ' + str(pos) + '\n')
                        else:
                            resultList.append('%' + str(registerNum) + ' = getelementptr i32, i32* ' + str(
                                tmp_Array.register) + ',i32 ' + str(pos) + '\n')
                        if ifNeedLoad:
                            resultList.append(
                            '%' + str(registerNum + 1) + ' = load i32, i32* %' + str(registerNum) + '\n')
                            registerNum += 1
                        tmpExp = Expression()
                        tmpExp.type = 'i32'
                        tmpExp.isregister = True
                        tmpExp.content = '%' + str(registerNum)
                        registerNum += 1
                        ExpInputStack.append(tmpExp)
                        self.tokenIndex -= 1
                elif tmpVal.type == 'function':
                    resultList.append('%' + str(registerNum) + ' = call i32 @' + str(tmpVal.content) + '(')
                    tmpExp = Expression()
                    tmpExp.type = 'i32'
                    tmpExp.isregister = True
                    tmpExp.content = '%' + str(registerNum)
                    registerNum += 1
                    ExpInputStack.append(tmpExp)
                    while not self.sym == ')':
                        self.readSym()
                    resultList.append(')\n')
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
            elif self.sym in FuncIdent or findFuncIndexByContent(self.sym)>=0:
                res = self.Func(identifierList)
                tmpExp = Expression()
                tmpExp.type = 'i32'
                tmpExp.isregister = True
                tmpExp.content = '%'+res
                # registerNum += 1
                ExpInputStack.append(tmpExp)
                self.tokenIndex-=1
            else:
                if self.sym == '(':
                    waitRight+=1
                if self.sym == ')':
                    if waitRight>0:
                        waitRight-=1
                    else:
                        self.readSym()
                        break
                ExpInputStack.append(self.sym)
            self.readSym()
        o_p = Operator_precedence()
        res = o_p.Operator_precedence_grammar('LVal')
        return res

    def CondJudgeIfEnd_exp(self,tmpIdentifierList):
        global registerNum
        global ExpInputStack
        while not tokenList[self.tokenIndex] == '{' and not (self.sym== ')' and findIndexByContent(tokenList[self.tokenIndex],tmpIdentifierList)== -1 and not tokenList[self.tokenIndex] in ['+','-','*','%','/','||','>=','<=','>','<','!','!=','==']):
            if (self.sym[0] == '_' or self.sym[0].isalpha()) and self.sym not in FuncIdent and self.sym not in comparator and not self.sym == '&&' and not self.sym == '||'  and not findFuncIndexByContent(self.sym)>=0:
                tmp = findIndexByContent(self.sym, tmpIdentifierList)
                if tmp == -1:
                    tmp = findFuncIndexByContent(self.sym)
                    if tmp == -1:
                        sys.exit(-1)
                    else:
                        tmpVal = FuncList[tmp]
                else:
                    if not isinstance(tmp, identifier):
                        tmpVal = tmpIdentifierList[tmp]
                    else:
                        tmpVal = tmp
                    if tmpVal.type == 'ConstVal':
                        ExpInputStack.append(str(tmpVal.value))
                    elif tmpVal.type == 'array':
                        saveExp = ExpInputStack
                        tmp_Array = tmpVal.toMyArray
                        ExpInputStack = saveExp
                        if tmp_Array.type == 'ConstVal':
                            save_Exp = copy.deepcopy(ExpInputStack)
                            ExpInputStack =  []
                            res = tmp_Array.value[self.getArrayElem(tmp_Array)]
                            ExpInputStack = copy.deepcopy(save_Exp)
                            ExpInputStack.append(str(res))
                        else:
                            saveExp = copy.deepcopy(ExpInputStack)
                            i = 0
                            ExpInputStack = []
                            self.readSym()
                            while self.sym == '[':
                                self.readSym()
                                tmp_Array.curElem[i] = self.Exp(tmpIdentifierList)
                                i += 1
                                self.readSym()
                            ExpInputStack = copy.deepcopy(saveExp)
                            # resultList.append('%' + str(registerNum) + ' = getelementptr i32, i32* ' + str(
                            #     tmpArray.register) + ', i32 ' + str(tmpArray.getCurLength('call')) + '\n')
                            pos =tmp_Array.getCurLength('call').content
                            if findIndexByContentOrigin(tmpVal.content,FuncList[curFuncIndex].paramContent)==-1:
                                resultList.append('%' + str(registerNum) + ' = getelementptr [' + str(
                                    tmp_Array.getTotalLength()) + ' x i32], [' + str(
                                    tmp_Array.getTotalLength()) + ' x i32]* ' + str(
                                    tmp_Array.register) + ', i32 0, i32 ' + str(pos) + '\n')
                            else:
                                resultList.append('%' + str(registerNum) + ' = getelementptr i32, i32* ' + str(
                                    tmp_Array.register) + ',i32 ' + str(pos) + '\n')
                            resultList.append(
                                '%' + str(registerNum + 1) + ' = load i32, i32* %' + str(registerNum) + '\n')
                            registerNum += 1
                            tmpExp = Expression()
                            tmpExp.type = 'i32'
                            tmpExp.isregister = True
                            tmpExp.content = '%' + str(registerNum)
                            registerNum += 1
                            ExpInputStack.append(tmpExp)
                            self.tokenIndex -= 1
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
                if isinstance(ExpInputStack[-1],Expression):
                    ExpInputStack.append(tokenList[self.tokenIndex-2])
                ExpInputStack.append(self.sym)
            elif self.sym in FuncIdent or findFuncIndexByContent(self.sym)>=0:
                saveExp = copy.deepcopy(ExpInputStack)
                ExpInputStack = []
                res = self.Func(tmpIdentifierList)
                ExpInputStack = saveExp
                tmpExp = Expression()
                tmpExp.isregister = True
                tmpExp.content = '%'+res
                tmpExp.type = 'i32'
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
    # input = sys.argv[1]
    # ir = sys.argv[2]
    input = 'D:\大三上\编译原理\compilingLab\in.txt'
    ir = 'D:\大三上\编译原理\compilingLab\out.txt'
    file = open(input)
    FuncAppear = [0 for i in range(len(FuncIdent))]
    # print(input)
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
    s_a.CompUnit('origin')
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
