import spacy
import json

from spacy.matcher import Matcher
from spacy.tokens import Span

from named_entity import NamedEntity

# Opening JSON file
f = open('matcher.json',)

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

print(patterns)

matcher.add(data['label'], patterns)

doc = nlp("barack Obama was definitely the 44th president of the United States")

matches = matcher(doc)
for match_id, start, end in matches:
    span = Span(doc, start, end, label=match_id)
    e = NamedEntity(span.text, span.label_, span.start_char, span.end_char)  
    print(e.toJSON())  	

