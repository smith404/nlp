import spacy
import json

from part_of_speech import PartOfSpeech
from named_entity import NamedEntity
from span import Span

from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')

# Add bespoke patters for entity recognition
data = open('patterns.json')
bespoke_patterns = json.load(data)
bespoke_ruler = nlp.add_pipe('entity_ruler', before='ner')
bespoke_ruler.add_patterns(bespoke_patterns)

# Read matcher index
index = open('matchers/index.json')
known_matchers = json.load(index)

class LanguageProcessor:
    def __init__(self, text):
        self._text = text
        self._doc = nlp(text)

    LIST_DELIMITER = ';'        

    @staticmethod
    def tokens_to_string(tokens):
        result = ""
        for token in tokens:
            result = result + token.lemma + " "
        
        return result

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
            results.append(PartOfSpeech(token.text, token.ent_type_, token.lemma_, \
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

    def entities_of_kind(self, kind):
        results = []
        for entity in self._doc.ents:
            if entity.label_ == kind:
                results.append(NamedEntity(entity.text, entity.label_, \
                    entity.start_char, entity.end_char))
        return results

    def sentences(self):
        results = []
        for sentence in self._doc.sents:
            results.append(Span(sentence.text, 'sentence', \
                sentence.start_char, sentence.end_char, sentence.sentiment))
        return results

    def remove_stops(self):
        results = []
        for token in self._doc:
            if (token.is_stop == False):
                results.append(PartOfSpeech(token.text, token.ent_type_, token.lemma_, \
                    token.pos_, token.tag_, token.dep_, \
                    token.shape_, token.is_alpha, token.is_stop))
        return results
        
    def matcher(self, name):
        matcher = Matcher(nlp.vocab)
        json_file = known_matchers[name]
        index = open(json_file)
        match_object = json.load(index)
        # Convert to a simple object list
        patterns = []
        for i in match_object['patterns']:
            patterns.append(i['pattern'])
        matcher.add(match_object['label'], patterns, greedy=match_object['greedy'])
        matches = matcher(self._doc)
        results = []
        for match in matches:
            match_span = self._doc[match[1]:match[2]]
            results.append(Span(match_span.text, match_object['label'], \
                match_span.start_char, match_span.end_char, match_span.sentiment))
        return results
