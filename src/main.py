from app.app import App
from app.main.methods import *
from app.main.qstrs.qstrs import qstr_get_update_products_by_offset
from checker.checker import NormalChecker
from config.config import Config
from config.settings import SETTINGS
from connection.connection import Connect
from data.data import CheckerData, ProcessorData
from flag.flag import FlagSimple, FlagVariation, FlagVariable, FlagBrand
from image.image import Image
from itertools import repeat
from log.log import Log
from product.product import Product
import concurrent.futures
import sys
import time
import random


class Main(App):
    """The main processor loads data and images from TABAT to wdp."""

    def run(self):

        data = ProcessorData()

        # load records, by offset (self.indx)
        qstr = qstr_get_update_products_by_offset(self.indx)
        _, records = self.cnx.q_db(serv="tab", qstr=qstr)

        # check that records exists
        data.err = "No data to process." if not records else ''
        data.product_data = records

        # run preprocessing methods that rely on ProcessorData
        if self.conf.conf.get('deleteCalcMeta', False):
            for record in data.product_data:
                _, _ = delete_calc_meta.main(self, record.get('sku', ''))

        # add any other pre-processors here
    
        # validate, inspect and create product attributes
        self.log.debug('Product processing ...')
        prod = Product(self.conf, self.cnx, self.log)
        data = prod.process(data)
        del(prod) # <- prod processor no longer needed

        # products need image ids, so we'll process images first
        self.log.debug('Image processing ...')
        img = Image(self.conf, self.cnx, self.log)
        data = img.process(data)
        # self.log.debug(f"image data {data.image_data}")
        # self.log.debug(f"featured image {data.featured_image}")
        # self.log.debug(f"info_by_wdppath {data.info_by_wdppath}")
        # self.log.debug(f"wdppaths_by_sku {data.wdppaths_by_sku}")
        del(img) # <- image processor no longer needed

        # vapr_id is needed by variations, so we'll process the variable prod next
        if data.komplexity == 'variable':
            self.log.debug('Flag Variable processing ...')
            # build variable command and run subprocess
            varf = FlagVariable(self.conf, self.cnx, self.log)
            data = varf.process(data)
            del(varf) # <- variable flag processor no longer needed

        if data.err:
            self.log.error(data.err)

        # process vapr_cmd (only one cmd_lst)
        for cmd in data.vapr_cmd_lst:
            vapr_id, _ = self.cnx.subprocess('wdp', cmd)
            vapr_id = "0" if not vapr_id else vapr_id 
            data.vapr_id = int(vapr_id)
            # add ids for future brand use
            data.wdp_ids.append(vapr_id) 

        # process simple products flags
        if data.komplexity == 'simple':
            self.log.debug('Flag Simple processing ...')
            sf = FlagSimple(self.conf, self.cnx, self.log)
            data = sf.process(data)
            del(sf) # <- simple/variation flag processor no longer needed

        # or process variation products flags
        if data.komplexity == 'variable':
            self.log.debug('Flag Variation processing ...')
            vf = FlagVariation(self.conf, self.cnx, self.log)
            data = vf.process(data)
            del(vf) # <- simple/variation flag processor no longer needed

        if data.err:
            self.log.error(data.err)

        # process commands (multiple commands in data.cmd_lst)
        for cmd in data.variation_cmd_lst:
            wdp_id, err = self.cnx.subprocess('wdp', cmd)
            data.err = err if err else ''

        # process simple_cmd (multiple commands in data.cmd_lst)
        for cmd in data.simple_cmd_lst:
            wdp_id, err = self.cnx.subprocess('wdp', cmd)
            data.wdp_ids.append(wdp_id)
            data.err = err if err else ''

        # ##################################################
        # process brands
        # note only set terms for Variable and Simple products, not variations
        self.log.debug('Brands processing ...')
        br = FlagBrand(conf, cnx, log)
        data = br.process(data)
        del(br)
        # ##################################################

        fabric_cats = {340, 341, 342, 343, 345, 346, 347, 348, 349, 351, 
                352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 1967, 
                1968, 1969, 1970, 1971, 1972, 1973, 1974, 2008}

        first_product = data.cleaned_data[0] if data.cleaned_data else {}
        category = first_product.get('categories', [])[0].get('id', 0)
        if int(category) in fabric_cats:
            update_wdp_stock_quantity.main(self, data)

        if data.err:
            log.error(f"Processing error: {data.err}")

        update_syncbools.main(self, data)
        return self


if __name__ == '__main__':
    # files can be found in /var/togsync/config.json and ./config/settings.py
    path = '/var/togsync/config.json'
    conf = Config(SETTINGS, path).load()
    log = Log(conf)
    cnx = Connect(conf, log)

    # for indx in range(conf.conf.get('numberThreads', 2)):

    # can add checkers here, run independently from processors
    cd = CheckerData(conf, cnx, log)
    c = NormalChecker(cd) # <-- currently only running status update
    c.check()
    if cd.err:
        log.warn(f"Checker error {cd.err}")
    del(cd)
    del(c)


    def thread(conf: Config, cnx: Connect, log: Log, indx: int):
        app = Main(conf, cnx, log, indx)
        time.sleep(random.uniform(0.3, 0.5))
        app.run()
        return

    if conf.conf.get('useThreads', False):
        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(
                    thread,
                    repeat(conf),
                    repeat(cnx),
                    repeat(log),
                    [x for x in range(conf.conf.get('numberThreads', 0))]
                    )
    else:
        for indx in range(conf.conf.get('numberThreads', 1)):
            thread(conf, cnx, log, indx)

    # disconnect
    if conf.conf.get('tabLoc', '') == "remote":
        cnx.conn['tab_ssh'].stop()

    if conf.conf.get('wdpLoc', '') == "remote":
        cnx.conn['wdp_ssh'].stop()

    log.info("Elvis has left the building ...")
    sys.exit("lights out")
