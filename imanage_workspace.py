import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageWorkspace(IManageObject):
    def __init__(self, body):
        super().__init__(body)

    def get_children(self, offset = 0):
        response = self.session.get_imanage_data('workspaces/' + self.id + '/children?offset=' + str(offset))
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
        response = self.session.get_imanage_data('workspaces/' + self.id + '/folders/search?name=' + name)
        item = None
        if 'data' not in response:
            return item
        itemData = response['data']
        if len(itemData) > 0:
            item = self.session.create_object(itemData[0])
            item.session = self.session
        return item
