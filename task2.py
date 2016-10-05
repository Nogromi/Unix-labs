import os
import sys

# pdir = 'd:/4course/unix/lab2'  #use this instead [sys.argw[1]] in case u don't run the cmd

lines = []


def count_em1(valid_path):
    x = 0
    for root, dirs, files in os.walk(valid_path):
        for d in dirs:
            count_em1(os.path.join(valid_path, d))
        for f in files:
            x += 1
        text = "There are " + str(x) + " files in " + valid_path + " directory."
        # print(text)
        lines.append(text)
        return x


answer = input("Enter the file name: ")
count_em1(sys.argw[1])


def sp(line):
    x = int(str(line).split(' ')[2])
    print(x)
    return x


lines.sort(key=sp)
f = open(answer + '.txt', 'w')
for i in lines:
    f.write(i)
    f.write('\n')
