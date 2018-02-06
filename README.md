oMarkovChainer


Generates sentences with Markov chains from text files.


It tries to format the text and words to have sentences look nicer, have proper capitalization for names, not to have multiple punctuation marks after each other, and remove some non-letter characters.
Options are for how many senteces should be generated, how long they should be, are the "sentences" in text as proper sentences or are they separate lines (for example if you feed it with song lyrics), and should something extra be removed or the text be formatted (at the moment extra options are to remove all numbers and/or read text as ANSI instead of utf-8).

About the sentence length. The program tries to end the sentence after the length is achieved, but only ends sentence with a word that has been used to end a sentence in the source text and is not included in the list of words the sentence cannot end with. Like prepositions like "with". With short source material this could be a problem as hitting a word that can end a sentence can take time and the generated sentence just grows and grows. Also, there are some words that appear in the text only at the end of a sentence. If the generated sentence tumbles into one of those, the sentence ends immediately, regardless of its length.

One could also wonder why words that cannot be at the end of a sentence are in the list of ending words. Maybe the source text has them like that or the sentence splitter just fails sometimes. The splitter is ugly and clunky anyway, a better one would be fine improvement.


Usage:
omarkov.py A B C D E
  
A = file

B = target length of sentences

C = number of sentences to generate

D = split file by rows: 0, split file by sentences: 1

E = optional, N: remove numbers, A: read file as ANSI

Example: omarkov.py lotr.txt 8 5 1 NA
