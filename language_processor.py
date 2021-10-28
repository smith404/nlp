import spacy

from part_of_speech import PartOfSpeech
from named_entity import NamedEntity

nlp = spacy.load("en_core_web_trf")

class LanguageProcessor:
    def __init__(self, text):
        self._text = text
        self._doc = nlp(text)
        
    @property            
    def text(self): 
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @text.deleter
    def text(self):
        del self._text

    def pos(self):
        results = []
        for token in self._doc:
            results.append(PartOfSpeech(token.text, token.lemma_, \
                token.pos_, token.tag_, token.dep_, \
                token.shape_, token.is_alpha, token.is_stop))
        return results

    def pos_of_type(self, tag):
        results = []
        for token in self._doc:
            if token.tag_ == tag:
                results.append(PartOfSpeech(token.text, token.lemma_, \
                    token.pos_, token.tag_, token.dep_, \
                    token.shape_, token.is_alpha, token.is_stop))
        return results

    def entities(self):
        results = []
        for entity in self._doc.ents:
            results.append(NamedEntity(entity.text, entity.label_, \
                entity.start_char, entity.end_char))
        return results

    def entities_of_lind(self, kind):
        results = []
        for entity in self._doc.ents:
            if entity.label_ == kind:
                results.append(NamedEntity(entity.text, entity.label_, \
                    entity.start_char, entity.end_char))
        return results
