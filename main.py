import spacy
import json 

class Entity:
    def __init__(self, ent, kind):
        self.ent = ent
        self.kind = kind

    def out(self):
        print(self.ent + " is a " + self.kind)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

nlp = spacy.load("en_core_web_sm")

f = open("input.txt", "r")
doc = nlp(f.read())

#for token in doc:
#    print(token.text, token.pos_, token.dep_)

for ent in doc.ents:
    #print(ent.text, ent.start_char, ent.end_char, ent.label_)
    e = Entity(ent.text, ent.label_)  
    #e.out()
    print(e.toJSON())  