#!/usr/bin/python
# coding: UTF-8

import itertools

# make a dictionary
f = open('/usr/share/dict/words')
file = f.read()
f.close()
words = file.split('\n')

dict = {}

for word in words:
    if len(word) >= 3 and len(word) <= 16:
        sorted_word = list(word)
        sorted_word.sort()
        sorted_word = ''.join(sorted_word)
        if sorted_word not in dict:
            dict[sorted_word] = [word]
        else:
            dict[sorted_word].append(word)
point = {'a':1, 'b':1, 'd':1, 'e':1, 'g':1, 'i':1,
         'n':1, 'o':1, 'r':1, 's':1, 't':1, 'u':1,
         'c':2, 'f':2, 'h':2, 'l':2, 'm':2, 'p':2,
         'v':2, 'w':2, 'y':2, 'j':3, 'k':3, 'q':3,
         'x':3, 'z':3}
print('dict prepared')


def find(l, n):
    candidate = list(itertools.combinations(l, n))
    for i in range(len(candidate)):
        c = sorted(list(candidate[i]))
        c = ''.join(c)
        if c in dict:
            print(dict[c])
            return True
    return False



# in dictionary or not
while True:
    input = list(raw_input('alphabets:'))

    score = []
    for i in range(len(input)):
        score.append((input[i], point[input[i]]))
    score = sorted(score, key=lambda x: x[1], reverse=True)
    #print(score)
    alphabets = [x[0] for x in score]
    #print(alphabets)

    for i in range(len(alphabets)):
        f = find(alphabets, len(alphabets)-i)
        if f == True:
            break





