import tika
from tika import parser

from imanage_folder import IManageFolder
from imanage_session import IManageSession

folder = IManageSession.create_object({ "id": "EMEA!12345", "wstype": "folder" })

folder.info()

parsed = parser.from_file('/braindump.docx')
print(parsed["metadata"])
print(parsed["content"])
