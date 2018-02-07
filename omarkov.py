import random
import sys
import re
import time

# there could be a nicer way to split text into sentences, but this seems to work sufficiently
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

if len(sys.argv) == 2:				# Yeah, the parameter doesn't need to be "usage" for it to work as long as there is only one parameter
	print("Usage: omarkov.py A B C D E <sentence length> <number of sentences> <split by rows : 0, split by sentences : 1> <optional>")
	print("A = file")
	print("B = target length of sentences")
	print("C = number of sentences to generate")
	print("D = split file by rows: 0, split file by sentences: 1")
	print("E = optional, N: remove numbers, A: read file as ANSI")
	print("Example: omarkov.py lotr.txt 8 5 1 NA")
	sys.exit()

if len(sys.argv) != 5 and len(sys.argv) != 6:
	print("Try \"omarkov.py usage\" for help")		
	sys.exit()


file = str(sys.argv[1])
length = int(sys.argv[2])
sentences = int(sys.argv[3])
method = int(sys.argv[4])
removeNumbers = False
fileEncoding = "utf-8"
if len(sys.argv) == 6:
	if "N" in sys.argv[5]:
		removeNumbers = True
	if "A" in sys.argv[5]:
		fileEncoding = "ANSI"


with open(file, "r", encoding=fileEncoding) as f:
	listOfLines = f.readlines()

if removeNumbers:
	print("Removing numbers")
	tempList = []
	temp = ""
	for x in listOfLines:
		temp = "".join(i for i in x if not i.isdigit())
		tempList.append(temp)
	listOfLines = tempList

if method == 1:
	temp = " ".join(listOfLines).rstrip().replace("  ", " ")
	listOfLinesFixed = [temp]
else:
	listOfLinesFixed = listOfLines

listOfLines2 = []
beginningWords = []
endingWords = []
listOfCapitalizedWords = []
listOfUnCapitalizedWords = []
progressCounterMax = int(len(listOfLinesFixed) / 10)
progressCounter = 0

sys.stdout.write("Listing the sentences    ")
sys.stdout.flush()
millis = int(round(time.time() * 1000))
for e in listOfLinesFixed:
	if method == 1:
		vara = split_into_sentences(e)
		progressCounterMax = int(len(vara) / 10)
		progressCounter = 0
		for z in vara:
			progressCounter += 1
			if progressCounter == progressCounterMax:
				sys.stdout.write(".")
				sys.stdout.flush()
				progressCounter = 0
			z2 = [y.strip().replace(".", "").strip("\'").replace("\"", "").replace("(", "").replace(")", "") for y in z.split()]
			z2 = list(filter(None, z2))
			if z2:
				z3 = []
				for t in z2:
					z3.append(t.lower())
				listOfLines2.append(z3)
				beginningWords.append(z2[0].lower())
				endingWords.append(z2[-1].lower())
				for count in range(1, len(z2)):								# makes a list of capitalized words in sentences to find out names etc.
					if z2[count][0].isupper():								# also makes a list of words that appear uncapitalized to finally remove them
						listOfCapitalizedWords.append(z2[count].lower())	# from the list of capitalized words, because writes like to Randomly capitalize
					else:													# words in Middle of sentences in addition to names
						listOfUnCapitalizedWords.append(z2[count].lower())
	else:
		progressCounter += 1
		if progressCounter == progressCounterMax:
			sys.stdout.write(".")
			sys.stdout.flush()
			progressCounter = 0
		z = [y.strip().replace(".", "").strip("\'").replace("\"", "").replace("(", "").replace(")", "") for y in e.split()]
		if z:
			z = list(filter(None, z))
			if z:
				z2 = []
				for t in z:
					z2.append(t.lower())
				listOfLines2.append(z2)
				beginningWords.append(z[0].lower())
				endingWords.append(z[-1].lower())
				for count in range(1, len(z)):
					if z[count][0].isupper():
						listOfCapitalizedWords.append(z[count].lower())

if method == 1:						
	print(" There was " + str(len(vara)) + " sentences and processing them took " + str(int(round(time.time() * 1000)) - millis) + " ms")
else:
	print(" There was " + str(len(listOfLinesFixed)) + " rows and processing them took " + str(int(round(time.time() * 1000)) - millis) + " ms")
	
beginningWords = list(filter(None, list(set(beginningWords))))
endingWords = list(filter(None, list(set(endingWords))))
listOfCapitalizedWords = list(set(listOfCapitalizedWords))
listOfUnCapitalizedWords = list(set(listOfUnCapitalizedWords))
tempList = []
progressCounterMax = int(len(listOfCapitalizedWords) / 10)
progressCounter = 0

sys.stdout.write("Checking capitalization  ")
sys.stdout.flush()
millis = int(round(time.time() * 1000))

listOfCapitalizedWords.sort()
listOfUnCapitalizedWords.sort()
capitalizationCounter = 0
capitalizedAlphabets = {}
unCapitalizedAlphabets = {}
# this could be done simpler, but this is about 15 times faster
for x in listOfCapitalizedWords:
	if x[0] not in capitalizedAlphabets.keys():
		capitalizedAlphabets[x[0]] = []
	capitalizedAlphabets[x[0]].append(x)
for x in listOfUnCapitalizedWords:
	if x[0] not in unCapitalizedAlphabets.keys():
		unCapitalizedAlphabets[x[0]] = []
	unCapitalizedAlphabets[x[0]].append(x)	
	
for x in capitalizedAlphabets.keys():
	for y in capitalizedAlphabets[x]:
		progressCounter += 1
		if progressCounter == progressCounterMax:
			sys.stdout.write(".")
			sys.stdout.flush()
			progressCounter = 0
		if x in unCapitalizedAlphabets.keys():
			if y not in unCapitalizedAlphabets[x]:
				tempList.append(y)
		else:
			tempList.append(y)
listOfCapitalizedWords = tempList
listOfCapitalizedWords.append("i")		# Lone I should always be capitalized, but probably the text file has uncapitalized single i somewhere, so...
print(" There is " + str(len(listOfCapitalizedWords)) + " capitalized words and prosessing them took " + str(int(round(time.time() * 1000)) - millis) + " ms")

mainlist = {}
progressCounterMax = int(len(listOfLines2) / 10)
progressCounter = 0
sys.stdout.write("Making database of words ")
sys.stdout.flush()
millis = int(round(time.time() * 1000))
for e in listOfLines2:
	progressCounter += 1
	if progressCounter == progressCounterMax:
		sys.stdout.write(".")
		sys.stdout.flush()
		progressCounter = 0
	for x in range(len(e)):
		if e[x] not in mainlist.keys():
			mainlist[e[x]] = {}
		if x < len(e) - 1:
			if e[x+1] not in mainlist[e[x]].keys():
				mainlist[e[x]][e[x+1]] = 0
			mainlist[e[x]][e[x+1]] += 1
print(" There is " + str(len(mainlist.keys())) + " words in total and prosessing them took " + str(int(round(time.time() * 1000)) - millis) + " ms")

mainlist2 = {}

for e in mainlist.keys():
	tempSum = 0
	for z in mainlist[e].keys():
		tempSum += mainlist[e][z]
	x = {}
	for z in mainlist[e].keys():
		x[z] = float(mainlist[e][z])/float(tempSum)
	x2 = {}
	tempSum2 = 0
	for z in x:
		tempSum2 += x[z]
		x2[z] = tempSum2
	mainlist2[e] = x2

listOfWordsSentenceCannotEndWith = ["the", "a", "of", "but", "with"]

while sentences > 0:
	output = ""
	word = beginningWords[random.randrange(len(beginningWords))]
	counter = length
	while True:
		counter -= 1
		if word[0] == "-" or word[0] == "!" or word[0] == "?":
			output = output[:-1]
		if word in listOfCapitalizedWords:
			output += word[:1].upper() + word[1:] + " "
		else:
			output += word + " "
		if word not in listOfWordsSentenceCannotEndWith:
			try:
				if (counter < 0 and word in endingWords) or not mainlist2[word].keys():
					break
			except:
				print(mainlist2[word].keys())
				break
		selectWord = random.uniform(0, 1.0)		# random number between 0 and 1 to select a word
		z = {}
		z2 = []
		temp = 0
		for x in mainlist2[word].keys():		# makes a dict of summed weights of words, with weight as the key
			temp += mainlist2[word][x]    
			z[str(temp)] = x
			z2.append(str(temp))
		z2.sort()								# sorting a list of stringified floating numbers
		for x in z2:							# if it's stupid and it works, it isn't stupid
			if float(x) > selectWord:
				word = z[x]
				break

	output = output[:-1]
	if output[-1] == ",":
		output = output[:-1]
	if output[-1] == "!" or output[-1] == "?":
		output += " "
	else:
		output += ". "

	output = output[:1].upper() + output[1:]
	print(output)
	sentences -= 1