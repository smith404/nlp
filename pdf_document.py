import fitz

TO_BLACK='ToBlack'
TO_LABEL='ToLabel'
TO_HIGHLIGHT='ToHighlight'

class PdfDocument:
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

    def redact_to_black(self, entity):
        for page in self.doc:
            areas = page.searchFor(entity.text)
            [page.add_redact_annot(area, text='[]', fill = (0, 0, 0)) for area in areas]
            page.apply_redactions()

    def redact_to_label(self, entity):
        for page in self.doc:
            areas = page.searchFor(entity.text)
            [page.add_redact_annot(area, text='[REDACTED' + entity.type + ']', fill = (0, 0, 0)) for area in areas]
            page.apply_redactions()

    def highlight(self, entity):
        for page in self.doc:
            areas = page.searchFor(entity.text)
            [page.add_highlight_annot(area) for area in areas]

    def get_bytes(self):
        return self.doc.convert_to_pdf()

    def save_as(self, name):
        return self.doc.save(name)