import sys


def judgeIfIdent(token):
    if token == 'if':
        print('If')
    elif token == 'else':
        print('Else')
    elif token == 'while':
        print('While')
    elif token == 'break':
        print('Break')
    elif token == 'continue':
        print('Continue')
    elif token == 'return':
        print('Return')
    else:
        print('Ident('+token+')')
    token = ''
def judgeUnsigned(token):
    print('Number('+token+')')
    token = ''
def lexicalAnalysis(linelist):
    for word in linelist:
        token = ''
        index = 0
        while( index< len(word)):
            if word[index].isalpha() or word[index]== '_' :
                while(word[index].isalpha() or word[index]== '_' or word[index].isdigit()):
                    token+=word[index]
                    index= index+1
                    if index >= len(word):
                        break
                index -=1
                judgeIfIdent(token)
                token=''
            elif word[index].isdigit():
                while(word[index].isdigit()):
                    token += word[index]
                    index = index + 1
                    if index >= len(word):
                        break
                index -=1
                judgeUnsigned(token)
                token= ''
            elif word[index] == '=':
                if index < len(word)-1:
                    if word[index+1] == '=':
                        print('Eq')
                        index +=1
                        continue
                    else:
                        print('Assign')
                else:
                    print('Assign')
            elif word[index] == ';':
                print('Semicolon')
            elif word[index] == '(':
                print('LPar')
            elif word[index] == ')':
                print('RPar')
            elif word[index] == '{':
                print('LBrace')
            elif word[index] == '}':
                print('RBrace')
            elif word[index] == '+':
                print('Plus')
            elif word[index] == '*':
                print('Mult')
            elif word[index] == '/':
                print('Div')
            elif word[index] == '<':
                print('Lt')
            elif word[index] == '>':
                print('Gt')
            else:
                print('Err')
                sys.exit(0)
            index +=1
if __name__ == '__main__':
    fileRoute = sys.argv[1]
    file = open(fileRoute)
    line = file.readline()
    while line:
        lineList = line.split()
        lexicalAnalysis(lineList)
        line = file.readline()

