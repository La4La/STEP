def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readMultiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readRight(line, index):
    token = {'type': 'RIGHT'}
    return token, index + 1

def readLeft(line, index):
    token = {'type': 'LEFT'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*' or line[index] == '×':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/' or line[index] == '÷':
            (token, index) = readDivide(line, index)
        elif line[index] == '(' or line[index] == '[' or line[index] == '{':
            (token, index) = readRight(line, index)
        elif line[index] == ')' or line[index] == ']' or line[index] == '}':
            (token, index) = readLeft(line, index)
        else:
            print ('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    tokens.insert(0, {'type': 'RIGHT'}) # Insert a dummy '(' token at the beginning
    tokens.append({'type': 'LEFT'}) # Insert a dummy ')' token at the end

    # keep evaluating until the length of tokens reduces to 1
    while len(tokens) > 1:

        # find the inner parentheses
        for i in range(len(tokens)):
            if tokens[i]['type'] == 'RIGHT':
                right = i
            if tokens[i]['type'] == 'LEFT':
                left = i
                break

        # evaluation of multiply and divide between the parentheses
        index = right + 1
        while index < left - 1:
            if tokens[index + 1]['type'] == 'MULTIPLY':
                tokens[index]['number'] *= tokens[index + 2]['number']
                del tokens[index + 1]
                del tokens[index + 1] # del '*' and the number after '*'
                left -= 2
            elif tokens[index + 1]['type'] == 'DIVIDE':
                tokens[index]['number'] /= tokens[index + 2]['number']
                del tokens[index + 1]
                del tokens[index + 1] # del '/' and the number after '/'
                left -= 2
            else:
                index += 1

        # evaluation of plus and minus between the parentheses
        index = right + 1
        while index < left - 1:
            if tokens[index + 1]['type'] == 'PLUS':
                tokens[index]['number'] += tokens[index + 2]['number']
                del tokens[index + 1]
                del tokens[index + 1]  # del '+' and the number after '+'
                left -= 2
            elif tokens[index + 1]['type'] == 'MINUS':
                tokens[index]['number'] -= tokens[index + 2]['number']
                del tokens[index + 1]
                del tokens[index + 1]  # del '-' and the number after '-'
                left -= 2
            else:
                index += 1

        # del the '(' and ')'
        del tokens[left]
        del tokens[right]

    answer = tokens[0]['number']
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print ("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print ("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print ("==== Test started! ====")
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("10-30/2*3.4-10/2+3", -43)
    test("(3.0+4×(2-1))÷5", 1.4)
    test("{2-[1.2-3*(2/2-1+3)+1]}*2/5", 3.52)
    print ("==== Test finished! ====\n")

runTest()

while True:
    print ('> ',)
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print ("answer = %f\n" % answer)