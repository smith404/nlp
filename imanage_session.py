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
        return None

    @property            
    def state(self): 
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property            
    def token(self): 
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property            
    def baseURL(self): 
        return self._baseURL

    @baseURL.setter
    def baseURL(self, value):
        self._baseURL = value

    def make_header(self):
        return { 'Authorization' : 'Bearer ' + self.token }

    def get_imanage_data(self, url_path):
        url = self.baseURL + url_path
        try:
            response = requests.get(url, headers=self.make_header(), verify=False)
            self.state = response.status_code
            if response.status_code == 200:
                return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def get_imanage_document(self, doc_id):
        text = {}
        text['body'] = ''
        url = self.baseURL + 'documents/' + doc_id + '/download'
        try:
            response = requests.get(url, headers=self.make_header(), verify=False)
            self.state = response.status_code
            if response.status_code == 200:
                text['body'] = response.text
        except:
            traceback.print_exc()
            self.state = 500
        return json.dumps(text)

    def get_workspaces(self, offset = 0):
        response = self.get_imanage_data('workspaces/search?offset=' + str(offset))
        workspaces = []
        if 'data' not in response:
            return workspaces
        workspaceData = response['data']
        for workspaceObject in workspaceData:
            # Create an object with the workspace data
            workspace = IManageSession.create_object(workspaceObject)
            # Add the session that read the workspace to the child object 
            workspace.session = self
            workspaces.append(workspace)
        return workspaces
       

