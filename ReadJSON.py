import spacy

from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

import re

import json

# Opening JSON file
f = open('parser.json',)

# returns JSON object as
# a dictionary
data = json.load(f)

# Closing file
f.close()

nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)

patterns = []
for i in data['patterns']:
    patterns.append(i['pattern'])

#print(patterns)

matcher.add(data['label'], patterns)

doc = nlp("Barack Obama was the 44th president of the United States")

matches = matcher(doc)
for match_id, start, end in matches:
    # Create the matched span and assign the match_id as a label
    span = Span(doc, start, end, label=match_id)
    print(span.text, span.label_)

