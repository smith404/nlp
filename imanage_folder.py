import json
import html
import requests
import re

from imanage_object import IManageObject
from imanage_session import IManageSession

class IManageFolder(IManageObject):
    def __init__(self, body):
        super().__init__(body)

    def get_documents(self, offset = 0):
        response = self.get_imamage_data('folders/' + self.id + '/documents?offset=' + offset)
        documents = []
        documentData = response['data']
        for documentObject in documentData:
            # Create an object with the workspace data
            document = IManageSession.create_object(documentObject)
            # Add the session that read the workspace to the child object 
            document.session = self.session
            documents.append(document)
        return documents

    def get_children(self, offset = 0):
        response = self.get_imamage_data('folders/' + self.id + '/children?offset=' + offset)
        items = []
        itemData = response['data']
        for itemObject in itemData:
            # Create an object with the workspace data
            item = IManageSession.create_object(itemObject)
            # Add the session that read the workspace to the child object 
            item.session = self.session
            items.append(item)
        return items

