oMarkovChainer


Generates sentences with Markov chains from text files.


It tries to format the text and words to have sentences look nicer, have proper capitalization for names, not to have multiple punctuation marks after each other, and remove some non-letter characters.
Options are for how many senteces should be generated, how long they should be, are the "sentences" in text as proper sentences or are they separate lines (for example if you feed it with song lyrics), and should something extra be removed or the text be formatted. Currently the extra options are remove numbers, read file as ANSI (instead of utf-8), have the sentences to have atleast as many words as the length says, to sentences have capital letter only in the beginning, removing commas, trying to make pairs of sentences the same length, and making pairs of sentences rhyme.

About the sentence length. The program tries to end the sentence after the length is achieved, but only ends sentence with a word that has been used to end a sentence in the source text and is not included in the list of words the sentence cannot end with. Like prepositions like "with". With short source material this could be a problem as hitting a word that can end a sentence can take time and the generated sentence just grows and grows. Also, there are some words that appear in the text only at the end of a sentence. If the generated sentence tumbles into one of those, the sentence ends immediately, regardless of its length.

One could also wonder why words that cannot be at the end of a sentence are in the list of ending words. Maybe the source text has them like that or the sentence splitter just fails sometimes. The splitter is ugly and clunky anyway, a better one would be fine improvement.

About the rhyming. First the program tries to make sentences that have the last three letters same, then after 500 tries it settles for two letters to be same and then again after 500 it just accepts if the rhyming words in both sentences are the same word. May be slow with large input texts and quite bad with too short texts.

The parameter S tries to make every second sentence to be 0.8 - 1.2 of the length of the previous sentence. As one can easily speculate, this combined with the rhyming really slows things down.

Usage:
omarkov.py A B C D E
  
A = file

B = target length of sentences

C = number of sentences to generate

D = split file by rows: 0, split file by sentences: 1

E = optional, N: remove numbers, A: read file as ANSI, L: make sentences at least long as length, C: Capital letters only in the beginning of sentence, R: try to make sentences rhyme, ,: remove commas, S: try really to make pairs of sentences the same length


Example: omarkov.py lotr.txt 8 5 1 NRC
