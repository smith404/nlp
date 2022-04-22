import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageFolder(IManageObject):
    def __init__(self, body):
        super().__init__(body)

    def get_documents(self, offset = 0):
        response = self.session.get_imanage_data('folders/' + self.id + '/documents?offset=' + str(offset))
        documents = []
        if 'data' not in response:
            return documents
        documentData = response['data']
        for documentObject in documentData:
            document = self.session.create_object(documentObject)
            document.session = self.session
            documents.append(document)
        return documents

    def get_children(self, offset = 0):
        response = self.session.get_imanage_data('folders/' + self.id + '/children?offset=' + str(offset))
        items = []
        if 'data' not in response:
            return items
        itemData = response['data']
        for itemObject in itemData:
            item = self.session.create_object(itemObject)
            item.session = self.session
            items.append(item)
        return items

    def get_folder(self, name):
        response = self.session.get_imanage_data('folders/' + self.id + '/folders/search?name=' + name)
        item = None
        if 'data' not in response:
            return item
        itemData = response['data']
        if len(itemData) > 0:
            item = self.session.create_object(itemData[0])
            item.session = self.session
        return item

    def make_folder(self, name):
        body = {}
        body['database'] = self.database
        body['name'] = self.name
        response = self.session.post_imanage_data('folders/' + self.id + '/children', body)
        item = None
        if 'data' not in response:
            return item
        itemData = response['data']
        if len(itemData) > 0:
            item = self.session.create_object(itemData[0])
            item.session = self.session
        return item

    def move_content(self, to_folder):

        return True
