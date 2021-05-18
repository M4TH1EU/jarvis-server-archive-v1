import re

import nltk
from nltk.corpus import stopwords

mytext = "Pourrais-tu m'allumer la lumière ainsi que allumer la tv"
tokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
mytext = re.sub('[\W_]+ ', '', mytext)

# tokens = tokenizer.tokenize(mytext)
# tokens = [t for t in tokens.split()]

tokens = [t for t in mytext.split()]
clean_tokens = tokens[:]

sr = stopwords.words('french')

for token in tokens:
    if token in sr:
        clean_tokens.remove(token)
freq = nltk.FreqDist(clean_tokens)

turn_on_lights = ['m\'allumer', 'allumer', 'lumière']
if turn_on_lights in freq.items():
    print("LIGHTSSS")

for key, val in freq.items():
    print(str(key) + ':' + str(val))