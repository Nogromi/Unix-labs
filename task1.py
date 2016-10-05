import os

pdir = 'd:/4course/unix/lab2'  #use this instead [sys.argw[1]] in case u don't run the cmd

contdir = []

def search(name):
    for d, dirs, files in os.walk(pdir):
        for f in files:
            if f.startswith(name):
                contdir.append((f, os.path.getsize(os.path.join(d,f))))
    contdir.sort(key=lambda x:x[1])
    print(contdir)

def write(answer):
    f = open(answer+'.txt' ,'w')
    for i in contdir:
        f.write('%s\t%d' % (i[0], i[1]))
        f.write('\n')

name=input("Enter the start of filename: ")
search(name)
answer=input("Enter the file for answer: ")
write(answer)