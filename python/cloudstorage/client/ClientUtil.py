from abc import ABC, abstractmethod


class CloudUtils(ABC):
    '''
    Abstract Class to connect and do the operation on different storage utls
    '''

    def getallfiles(self):
        pass

    def getmetadata(self):
        pass

    def connecttostorage(self):
        pass


