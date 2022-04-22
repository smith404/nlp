import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageWorkspace(IManageObject):
    def __init__(self, body):
        super().__init__(body)

    def get_children(self, offset = 0):
        response = self.get_imanage_data('workspaces/' + self.id + '/children?offset=' + str(offset))
        items = []
        if 'data' not in response:
            return items
        itemData = response['data']
        for itemObject in itemData:
            # Create an object with the workspace data
            item = self.session.create_object(itemObject)
            # Add the session that read the workspace to the child object 
            item.session = self.session
            items.append(item)
        return items

    def get_folder(self, name):
        response = self.get_imanage_data('workspaces/' + self.id + '/folders/search?name=' + name)
        item = {}
        if 'data' not in response:
            return item
        itemData = response['data']
        if len(itemData) > 0:
            return itemData[0]
        return item
