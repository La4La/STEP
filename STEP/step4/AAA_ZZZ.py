import re

upperReg = re.compile(r'^[A-Z]+$')
def isupper(s):
    return upperReg.match(s) is not None

count = 0

f = open('pages.txt', encoding='utf-8')
line = f.readline()
while line:
    items = line[:-1].split('\t')
    pageName = items[1]
    if len(pageName) == 3 and isupper(pageName):
        count += 1
        print(pageName)
    line = f.readline()
f.close()

print(count)