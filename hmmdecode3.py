import sys
import codecs
import ast
import math

testing_data = sys.argv[1]
model_file = "hmmmodel.txt"
output_file = "hmmoutput.txt"

items = []
f = open(model_file, encoding="utf8", errors='ignore').read().splitlines()
numeratorT = {}
transitionDenomination = {}
numeratorE = {}
emmitiondenominatior = {}
prior = {}
uniquewords = {}
uniqueTags = {}
for line in f:
    value = line.split("=", 1)
    if value[0] == "numeratorT":
        numeratorT = ast.literal_eval(value[1])
    elif value[0] == "transitionDenomination":
        transitionDenomination = ast.literal_eval(value[1])
    elif value[0] == "numeratorE":
        numeratorE = ast.literal_eval(value[1])
    elif value[0] == "emmitiondenominatior":
        emmitiondenominatior = ast.literal_eval(value[1])
    elif value[0] == "prior":
        prior = ast.literal_eval(value[1])
    elif value[0] == "totalsent":
        totalsent = int(value[1])
    elif value[0] == "uniquewords":
        uniquewords = ast.literal_eval(value[1])
    elif value[0] == "uniqueTags":
        uniqueTags = ast.literal_eval(value[1])
    elif value[0] == "N":
        N = int(value[1])
    else:
        print("Error")

f = open(testing_data, encoding="utf8", errors='ignore').read().splitlines()
for line in f:
    words = line.split()
    cols = len(words)
    rows = N
    ans = [[0 for x in range(cols)] for y in range(rows)]
    parent = [[0 for x in range(cols)] for y in range(rows)]
    for j in range(cols):
        for i in range(rows):
            if j == 0:
                if words[j] not in uniquewords:
                    E = 1
                else:
                    key2 = words[j]+"/"+uniqueTags[i]
                    # print(key2)
                    if key2 not in numeratorE:
                        E = 0
                    else:
                        E = numeratorE[key2] / \
                            emmitiondenominatior[uniqueTags[i]]
                if uniqueTags[i] in prior:
                    ans[i][j] = E*(prior[uniqueTags[i]]/totalsent)
                else:
                    ans[i][j] = 0
            else:
                x = []
                for k, tag in enumerate(uniqueTags):
                    key = tag+"#"+uniqueTags[i]
                    # print(key)
                    if key in numeratorT:
                        if tag in transitionDenomination:
                            T = numeratorT[key] + 1 / \
                                transitionDenomination[tag] + N
                        else:
                            T = numeratorT[key] + 1 / N
                    else:
                        if tag in transitionDenomination:
                            T = 1 / transitionDenomination[tag] + N
                        else:
                            T = 1 / N
                    x.append(ans[k][j-1]*T)
                val = max(x)
                y = x.index(max(x))
                prev = j-1
                parent[i][j] = str(y)+","+str(prev)

                if words[j] not in uniquewords:
                    E = 1
                else:
                    key2 = words[j]+"/"+uniqueTags[i]
                    if key2 not in numeratorE:
                        E = 0
                    else:
                        E = numeratorE[key2] / \
                            emmitiondenominatior[uniqueTags[i]]
                ans[i][j] = E*val
    # for i in range(len(ans)):
    #     ans[i].append(uniqueTags[i])
    #     print(ans[i])
    # for i in range(len(ans)):
    #     parent[i].append(uniqueTags[i])
    #     print(parent[i])
    maxoutput = ans[0][cols-1]
    for i in range(rows):
        if maxoutput < ans[i][cols-1]:
            maxoutput = ans[i][cols-1]
            tag = uniqueTags[i]
            index = i
    finalanswer = []
    finalanswer = [tag]+finalanswer
    indexI = i
    indexJ = cols-1
    while indexJ != 0:
        pos = parent[indexI][indexJ]
        pos = pos.split(",")
        indexI = int(pos[0])
        indexJ = int(pos[1])
        tag = uniqueTags[indexI]
        finalanswer = [tag]+finalanswer

    output = ""
    for i, word in enumerate(words):
        output += word+"/"+finalanswer[i]+" "
    # print(output)

    with codecs.open(output_file, 'a', encoding='utf8') as f:
        f.write(output+"\n")
