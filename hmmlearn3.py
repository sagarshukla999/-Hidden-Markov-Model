from collections import Counter
import codecs
import sys
from collections import defaultdict

totaltags = []
uniqueTags = []
transitionTotaltags = []
numeratorE = []
numeratorT = []
prior = []
uniquewords = []

f = open(sys.argv[1], encoding="utf8", errors='ignore').read().splitlines()
for line in f:
    words = line.split()
    numeratorE += words
    t = words[0].rsplit('/', 1)
    prior.append(t[1])
    for i, tags in enumerate(words):
        arr = tags.rsplit('/', 1)
        totaltags.append(arr[1])
        uniquewords.append(arr[0])
        if tags != words[-1]:
            transitionTotaltags.append(arr[1])
            nextTag = words[i+1].rsplit('/', 1)
            numeratorT.append(arr[1]+"#"+nextTag[1])
uniqueTags = list(set(totaltags))
numeratorE = Counter(numeratorE)
uniquewords = list(set(uniquewords))
emmitiondenominatior = Counter(totaltags)
numeratorT = Counter(numeratorT)
transitionDenomination = Counter(transitionTotaltags)
prior = Counter(prior)
totalsent = len(f)


with codecs.open("hmmmodel.txt", 'w', encoding='utf8') as f:
    f.write("numeratorT="+str(dict(numeratorT))+"\n")
    f.write("transitionDenomination="+str(dict(transitionDenomination))+"\n")
    f.write("numeratorE="+str(dict(numeratorE))+"\n")
    f.write("emmitiondenominatior="+str(dict(emmitiondenominatior))+"\n")
    f.write("prior="+str(dict(prior))+"\n")
    f.write("totalsent="+str(totalsent)+"\n")
    f.write("uniquewords="+str(uniquewords)+"\n")
    f.write("uniqueTags="+str(uniqueTags)+"\n")
    f.write("N="+str(len(uniqueTags))+"\n")
