from config.config import Config
from config.settings import SETTINGS
from log.log import Log
from connection.connection import Connect
from data.data import ProcessorData
import unittest


class TestProductLoader(unittest.TestCase):

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

    def test_product_validate(self):
        # correct varible data
        sd = ProcessorData()
        data = [{
                'pid': 26948, 
                'sku': 'SKU43509', 
                'stock_quantity': 4,
                'komplexity': 'variable'}]
        sd.product_data = data
        from product.methods import product_validation
        clean_data = []
        for record in data:
            clean_record, _ = product_validation.main(record)
            clean_data.append(clean_record)
        # print("## clean_data", clean_data)
        self.assertEqual(clean_data[0]['image_is_updated'], 0)
        return self

    def test_product_load(self):
        from app.main.qstrs.qstrs import qstr_get_update_products_by_offset
        os = 0
        qstr = qstr_get_update_products_by_offset(offset=os)
        _, records = self.cnx.q_db('tab', qstr)
        print("## records", records)
        return self



if __name__ == '__main__':
    unittest.main()
