from abc import ABC, abstractmethod
from config.config import Config
from connection.connection import Connect
from log.log import Log

class App(ABC):

    def __init__(self, conf: Config, cnx: Connect, log: Log, indx: int = 0):
        self.conf = conf
        self.cnx = cnx
        self.log = log
        self.indx = indx

    @abstractmethod
    def run(self):
        ...
