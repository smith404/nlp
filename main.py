import spacy

nlp = spacy.load("en_core_web_sm")

f = open("input.txt", "r")
doc = nlp(f.read())

for token in doc:
    print(token.text, token.pos_, token.dep_)