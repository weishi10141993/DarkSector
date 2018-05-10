import sys

with open("Wei.dat") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

sys.stdout = open('list_cff.py','w')

for a in range(0, len(content)):
    if "315/188" in content[a]:
        if a==0:
           print "inputFileNames=['%s',"%(content[a])
        if a!=0:
           print "'%s',"%(content[a])
print "]"
