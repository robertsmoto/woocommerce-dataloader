from config.config import Config
from connection.connection import Connect
from log.log import Log
import unittest
from config.settings import SETTINGS
from data.data import ProcessorData
from product.product import Product

class TestProcessor(unittest.TestCase):

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

    def test_attrs_list(self):
        # # correct varible data
        # data = {
                # 'pid': 26948, 
                # 'sku': 'SKU43509', 
                # 'stock_quantity': 4,
                # 'komplexity': 'variable'}
        # img = {'test': 'data'}
        # proc = ProductProcessor(self.conf, self.cnx, self.log)
        # proc.inspect(data, img) # <-- returns self.inspect_data dict
        # from processor.methods import create_attrs_list
        # attr_list, err = create_attrs_list.main(proc)
        # print("attr_list -->", attr_list)
        # print("err -->", err)
        # proc.validate()
        # # self.assertEqual(proc.inspect_data['vapr_operation'], 'update')
        return self


    def test_load_products_variable(self):
        # # correct varible data
        # data = {
                # 'pid': 26948, 
                # 'sku': 'SKU43509', 
                # 'stock_quantity': 4,
                # 'komplexity': 'variable'}
        # img = {'test': 'data'}
        # proc = ProductProcessor(self.conf, self.cnx, self.log)
        # proc.inspect(data, img) # <-- returns self.inspect_data dict
        # self.assertEqual(proc.inspect_data['vapr_operation'], 'update')
        # # crud operation only set for simple products
        # self.assertEqual(
                # proc.inspect_data.get('crud_operation', 'no value'), 
                # 'no value')
        # # vapr_quantity only set for vapr
        # has_vapr_quantity = proc.inspect_data.get('vapr_quantity', 'no value')
        # self.assertNotEqual(has_vapr_quantity, 'no value')
        # self.assertEqual(
                # math.floor(proc.inspect_data.get('vapr_quantity', 0)), 
                # 112)
        # self.assertEqual(proc.inspect_data.get('vapr_id', 0), 1648749)
        # self.assertEqual(
                # proc.inspect_data.get('vapr_sku', ''), 
                # 'vapr-637514289-YDIM-953628174')
        # prod_by_pid = proc.inspect_data.get('prods_by_pid', [])
        # self.assertEqual(len(prod_by_pid), 12)
        return self

    def test_validate_simple(self):
        products = [{
                'pid': 20328, 
                'sku': 'SKU23193', 
                'stock_quantity': 6,
                'komplexity': 'simple'}]
        img = {'test': 'data'}
        pd = ProcessorData()
        pd.product_data = products
        from product.methods import product_validation
        for product in pd.product_data:
            result, err = product_validation.main(product)
        print("## product -->", pd.product_data)
        from product.methods import inspect_simple_product
        prod = Product(self.conf, self.cnx, self.log, pd)
        for product in pd.product_data:
            err = inspect_simple_product.main(prod, product)
        print("## product -->", pd.product_data)
        # self.assertEqual(proc.inspect_data.get('crud_operation', ''), 'create')
        # self.assertEqual(proc.inspect_data.get('vapr_quantity'), False)
        return self

    
if __name__ == '__main__':
    unittest.main()
