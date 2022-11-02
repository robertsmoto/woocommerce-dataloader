from config.config import Config
from config.settings import SETTINGS
from connection.connection import Connect
from log.log import Log
from checker.checker import NormalChecker
from data.data import CheckerData

import unittest

class TestNormalChecker(unittest.TestCase):

    def setUp(self):
        path = '/var/togsync/config.json'
        self.conf = Config(SETTINGS, path).load()
        self.log = Log(self.conf)
        self.cnx = Connect(self.conf, self.log)

    def tearDown(self):
        if self.conf.conf['tabLoc'] == "remote":
            self.cnx.conn['tab_ssh'].stop()
        if self.conf.conf['wdpLoc'] == "remote":
            self.cnx.conn['wdp_ssh'].stop()
        return self

    def test_get_candaiates(self):
        cd = CheckerData(self.conf, self.cnx, self.log)
        checker = NormalChecker(cd)
        checker.check()
        return self

    
if __name__ == '__main__':
    unittest.main()
