from config.config import Config
from config.settings import SETTINGS
import unittest


class TestEnvVariables(unittest.TestCase):

    def setUp(self):
        path = '/var/togsync/config.json'
        self.conf = Config(SETTINGS, path).load()
        return self

    def test_load_env(self):
        ssh_port = self.conf.conf.get('SSH_PORT', '')
        self.assertEqual(ssh_port, '2023')
        dossh_devs = bool(self.conf.conf.get('DOSSH_DEVS', 'false'))
        self.assertEqual(dossh_devs, True)
        dossh_port = int(self.conf.conf.get('DOSSH_PORT', '1000'))
        self.assertEqual(dossh_port, 22)

    def test_app_settings(self):
        self.assertEqual(self.conf.conf['wdpLoc'], 'remote') 

if __name__ == '__main__':
    unittest.main()
