import spacy
from NamedEntity import NamedEntity
from PartOfSpeech import PartOfSpeech

nlp = spacy.load("en_core_web_sm")

f = open("input.txt", "r")
doc = nlp(f.read())

for token in doc:
    p = PartOfSpeech(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
    print(p.toJSON())  

#for ent in doc.ents:
#    e = NamedEntity(ent.text, ent.label_, ent.start_char, ent.end_char)  
#    print(e.toJSON())  