TO_BLACK='ToBlack'
TO_LABEL='ToLabel'
TO_HIGHLIGHT='ToHighlight'

class TxtDocument:
    def __init__(self, doc, include, action_type):
        self.doc = doc
        self.include = include
        self.action_type = action_type

    def redact(self, entities):
        for entity in entities:
            self.do_redact(entity)

    def do_redact(self, entity):
        if self.action_type == TO_BLACK:
            self.redact_to_black(entity)
        elif self.action_type == TO_LABEL:
            self.redact_to_label(entity)
        elif self.action_type == TO_HIGHLIGHT:
            self.highlight(entity)

    def replace_name_with_redacted(self, token):
        if token.ent_iob != 0 and token.ent_type in self.include:
            self.doc = self.doc.replace(token.text,'[REDACTED]')

    def replace_name_with_label(self, token):
        if token.ent_iob != 0 and token.ent_type in self.include:
            self.doc = self.doc.replace(token.text,'[REDACTED ' + token.ent_type_ + ']')

    def replace_name_with_marker(self, token):
        if token.ent_iob != 0 and token.ent_type in self.include:
            self.doc = self.doc.replace(token.text,'[[' + token.text + ']]')

    def get_bytes(self):
        return self.doc

    def save_as(self, name):
        return self.doc.save(name)