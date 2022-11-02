from log.log import Log
from config.config import Config
from config.settings import SETTINGS
from connection.connection import Connect
import psycopg2
import psycopg2.extras
import pymysql
import unittest


class TestConnections(unittest.TestCase):

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

    def test_connect(self):
        db = self.cnx.conn['wdp_pool'].connection()
        cur = db.cursor(pymysql.cursors.DictCursor)
        # print("## cursor", cur)
        cur.execute("""SELECT * FROM wp_posts LIMIT 2;""")
        result = cur.fetchone()
        if result:
            self.assertIsInstance(result, dict)
            # number = cur.rowcount
            # print("result", result)
            # print("number", number)
            # print("result ID", result['ID'])
        cur.close()

        db = self.cnx.conn['tab_pool'].connection()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM products LIMIT 2;")
        result = cur.fetchone()
        if result:
            self.assertIsInstance(result, psycopg2.extras.DictRow)
            # print("result", result)
            # print("result pid", result['pid'])
        cur.close()

        self.cnx.conn['wdp_pool'].close()
        self.cnx.conn['tab_pool'].close()
        self.cnx.conn['wdp_ssh'].stop()
        self.cnx.conn['tab_ssh'].stop()

if __name__ == '__main__':
    unittest.main()

