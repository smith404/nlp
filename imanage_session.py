# Copyright (c) 2022. K2-Software
# All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.

import json
import traceback
import requests

from object_type import ObjectType
from imanage_object import IManageObject
from imanage_workspace import IManageWorkspace
from imanage_folder import IManageFolder
from imanage_document import IManageDocument
from imanage_email import IManageEmail

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# We are ignoring certificate warnings so we don't want wanrnings all the time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class IManageSession:
    def __init__(self, baseURL, token):
        self._baseURL = baseURL
        self._token = token
        self._state = 200

    @staticmethod
    def create_object(body):
        type = ObjectType.UNKNOWN
        if 'wstype' in body:
            type = ObjectType.value(body['wstype'])
        if type == ObjectType.DOCUMENT:
            return IManageDocument(body)
        if type == ObjectType.FOLDER:
            return IManageFolder(body)
        if type == ObjectType.EMAIL:
            return IManageEmail(body)
        if type == ObjectType.WORKSPACE:
            return IManageWorkspace(body)
        return IManageObject(body)

    @property            
    def state(self): 
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property            
    def baseURL(self): 
        return self._baseURL

    @baseURL.setter
    def baseURL(self, value):
        self._baseURL = value

    @property            
    def token(self): 
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def make_authenticated_header(self):
        return { 'Authorization' : 'Bearer ' + self.token }

    def make_header_with_content_type(self, type):
        header = {}
        header['Authorization'] = 'Bearer ' + self.token
        header['Content-Type'] = type
        return header

    def get_object_with_id(self, id, domain):
            domain_str = domain
            if isinstance(domain, (ObjectType)):
                domain_str = ObjectType.domain(domain)
            url = domain_str + '/' + id
            body = self.get_imanage_data(url)
            item = self.create_object(body['data'])
            item.session = self
            return item
            
    def get_imanage_data(self, url_path):
        url = self.baseURL + url_path
        try:
            response = requests.get(url, headers=self.make_authenticated_header(), verify=False)
            self.state = response.status_code
            return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def patch_imanage_data(self, url_path, body):
        url = self.baseURL + url_path
        try:
            response = requests.patch(url, headers=self.make_header_with_content_type('application/json'), data = json.dumps(body), verify=False)
            self.state = response.status_code
            return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def post_imanage_data(self, url_path, body):
        url = self.baseURL + url_path
        try:
            response = requests.post(url, headers=self.make_header_with_content_type('application/json'), data = json.dumps(body), verify=False)
            self.state = response.status_code
            return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def put_imanage_data(self, url_path, body):
        url = self.baseURL + url_path
        try:
            response = requests.put(url, headers=self.make_header_with_content_type('application/json'), data = json.dumps(body), verify=False)
            self.state = response.status_code
            return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def delete_imanage_data(self, url_path, body):
        url = self.baseURL + url_path
        try:
            response = requests.delete(url, headers=self.make_header_with_content_type('application/json'), data = json.dumps(body), verify=False)
            self.state = response.status_code
            return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def get_imanage_document(self, document):
        url = self.baseURL + 'documents/' + document.id + '/download'
        try:
            response = requests.get(url, headers=self.make_authenticated_header(), verify=False)
            self.state = response.status_code
            if response.status_code == 200:
                document._data = response.content
                return True
            else:
                document._data = None
                return False
        except:
            traceback.print_exc()
            self.state = 500
            document._data = None
        return False

    def upload_imanage_data(self, url_path, data):
        url = self.baseURL + url_path
        try:
            response = requests.delete(url, headers=self.make_header_with_content_type('application/json'), data = json.dumps(data), verify=False)
            self.state = response.status_code
            return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def get_objects(self, domain, offset = 0):
        domain_str = domain
        if isinstance(domain, (ObjectType)):
            domain_str = ObjectType.domain(domain)
        response = self.get_imanage_data(domain_str + '/search?offset=' + str(offset))
        items = []
        if 'data' not in response:
            return items
        itemData = response['data']
        for itemObject in itemData:
            item = self.create_object(itemObject)
            item.session = self
            items.append(item)
        return items

    def get_recent_objects(self, domain, offset = 0):
        domain_str = domain
        if isinstance(domain, (ObjectType)):
            domain_str = ObjectType.domain(domain)
        response = self.get_imanage_data(domain_str + '/recent?offset=' + str(offset))
        items = []
        if 'data' not in response:
            return items
        itemData = response['data']
        for itemObject in itemData:
            item = self.create_object(itemObject)
            item.session = self
            items.append(item)
        return items

    def get_object(self, domain, name):
        domain_str = domain
        if isinstance(domain, (ObjectType)):
            domain_str = ObjectType.domain(domain)
        response = self.get_imanage_data(domain_str + '/search?name=' + name)
        item = None
        if 'data' not in response:
            return item
        itemData = [item for item in response['data'] if item['name'] == name]
        if len(itemData) > 0:
            item = self.create_object(itemData[0])
            item.session = self
        return item
