from abc import ABC, abstractmethod
from config.config import Config
from connection.connection import Connect
from data.data import ProcessorData
from log.log import Log

class Processor(ABC):

    def __init__(self, conf: Config, cnx: Connect, log: Log):
        self.conf = conf
        self.cnx = cnx
        self.log = log

    @abstractmethod
    def process(self, data: ProcessorData) -> ProcessorData:
        ...
