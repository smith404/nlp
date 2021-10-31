import fitz

class ActiveDocument:
    def __init__(self, doc):
        self.doc = doc

    def redactToBlack(self, entity):
        for page in self.doc:
            areas = page.searchFor(entity.text)
            [page.add_redact_annot(area, text='[]', fill = (0, 0, 0)) for area in areas]
            page.apply_redactions()

    def redactToLabel(self, entity):
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