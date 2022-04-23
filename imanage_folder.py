# Copyright (c) 2022. K2-Software
# All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.

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

    def subfolder_exists(self, name):
        response = self.session.get_imanage_data('folders/' + self.id + '/subfolders?limit=1000')
        if 'data' not in response:
            return False
        itemData = [item for item in response['data'] if item.name == name]
        if len(itemData) > 0:
            return True
        else:
            return False

    def make_folder(self, name):
        body = {}
        body['name'] = self.name
        body['default_security'] = 'inherit'
        body['database'] = self.database
        body['description'] = 'K2-Lib created folder for ' + self.name
        response = self.session.post_imanage_data('folders/' + self.id + '/subfolders', body)
        if 'data' in response:
            return True
        else:
            return False

    def move_content(self, to_folder):

        return True
