oMarkovChainer


Generates sentences with Markov chains from text files.


It tries to format the text and words to have sentences look nicer, have proper capitalization for names, not to have multiple punctuation marks after each other, and remove some non-letter characters.
Options are for how many senteces should be generated, how long they should be, are the "sentences" in text as proper sentences or are they separate lines (for example if you feed it with song lyrics), and should something extra be removed or the text be formatted (at the moment extra options are to remove all numbers and/or read text as ANSI instead of utf-8).


Usage:
omarkov.py A B C D E <sentence length> <number of sentences> <split by rows : 0, split by sentences : 1> <optional>
  
A = file

B = target length of sentences

C = number of sentences to generate

D = split file by rows: 0, split file by sentences: 1

E = optional, N: remove numbers, A: read file as ANSI

Example: omarkov.py lotr.txt 8 5 1 NA
