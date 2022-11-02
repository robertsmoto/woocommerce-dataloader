from config.config import Config
from config.settings import SETTINGS
from connection.connection import Connect
from log.log import Log
from data.data import ProcessorData

import unittest

class Test_Error(unittest.TestCase):

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
        # this is checking that the error string values are not shared between
        # class instances
        data1 = ProcessorData()
        data1.err = ''
        data2 = ProcessorData()
        data2.err = 'some error'
        data3 = ProcessorData()
        self.assertEqual(data1.err, '')
        self.assertEqual(data2.err, 'some error')
        self.assertEqual(data3.err, '')
        return self

    
if __name__ == '__main__':
    unittest.main()
