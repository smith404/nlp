from enum import Enum

class ObjectType(Enum):
    UNKNOWN = 0
    DOCUMENT = 1
    FOLDER = 2
    WORKSPACE = 3
    EMAIL = 4
    DOCUMENT_SHORTCUT = 5
    FOLDER_SHORTCUT = 6
    WORKSPACE_SHORTCUT = 7
    LIBRARY = 8

    @staticmethod
    def value(wstype):
        if wstype.casefold() == 'document':
            return ObjectType.DOCUMENT
        if wstype.casefold() == 'folder':
            return ObjectType.FOLDER
        if wstype.casefold() == 'workspace':
            return ObjectType.WORKSPACE
        if wstype.casefold() == 'email':
            return ObjectType.EMAIL
        if wstype.casefold() == 'document_shortcut':
            return ObjectType.DOCUMENT_SHORTCUT
        if wstype.casefold() == 'folder_shortcut':
            return ObjectType.FOLDER_SHORTCUT
        if wstype.casefold() == 'workspace_shortcut':
            return ObjectType.WORKSPACE_SHORTCUT
        if wstype.casefold() == 'library':
            return ObjectType.LIBRARY
        return ObjectType.UNKNOWN


