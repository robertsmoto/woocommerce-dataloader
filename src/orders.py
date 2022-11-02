from app.orders.methods import *
from app.app import App
from app.main.methods import *
from config.config import Config
from config.settings import SETTINGS
from connection.connection import Connect
from log.log import Log
import sys

# statuses with priority
ALL_STATUS_TYPES = {
        'wc-authentication-required': 1,
        'wc-pending-payment': 3,
        'wc-pending': 5,
        'wc-processing': 7,
        'wc-export-to-neoship': 8,
        'wc-failed': 9,
        'wc-on-hold': 11,
        'wc-cancelled': 13,
        'wc-completed': 15,
        'wc-refunded': 17,
    }

TABLE_KEYS = {
        'tabat_orders': 'order_id',
        'wp_wc_order_stats': 'order_id',
        'wp_wc_customer_lookup': 'customer_id',
    }

ALL_TABLES = {
        'tabat_orders': [
            'order_id', 'sku', 'vzor', 'city', 'l_name', 'invoice_no',
            'quantity', 'unit_price', 'f_name', 'date_created', 'customer_id'],
        'wp_wc_customer_lookup': [
            'customer_id', 'user_id', 'username', 'first_name', 'last_name',
            'email', 'date_last_active', 'date_registered', 'country',
            'postcode', 'city', 'state'],
        'wp_wc_order_stats': [
            'order_id', 'parent_id', 'date_created', 'date_created_gmt',
            'num_items_sold', 'total_sales', 'tax_total', 'shipping_total',
            'net_total', 'returning_customer', 'status', 'customer_id'],
    }


class LoadOrders(App):
    """The main processor loads data and images from TABAT to wdp."""

    def run(self):
        """ The main orders sync program """
        # check new orders
        self.log.info("Looking over orders ...")
        n_new_orders, _ = check_orders.main(self, check="new")
        if n_new_orders > 0:
            self.log.info(f"{n_new_orders} new order(s) found.")
            sync_order_tables.main(
                    self, tables=ALL_TABLES, tablekeys=TABLE_KEYS)
            self.log.info("Sync'd all orders tables")
        else:
            self.log.info("No new orders found.")

        # sync_orders_tables(
        #         conn=conn, tables=ALL_TABLES, tablekeys=TABLE_KEYS)

        # check if status changed
        self.log.info("Checking if any order status has changed ...")
        n_orders_changed, orders_changed = check_status_changed.main(
                self, table='wp_wc_order_stats', ALL_TABLES=ALL_TABLES)
        if n_orders_changed > 0:
            self.log.info(
                    f"{n_orders_changed} Order(s) have changed status.")
            compare_order_status.main(
                    self, orders=orders_changed, ALL_STATUS_TYPES=ALL_STATUS_TYPES)
            self.log.info("I've updated the status for those orders.")
        else:
            self.log.info("No orders have their status changed.")

        return


if __name__ == '__main__':

    # files can be found in /var/togsync/config.json and ./config/settings.py
    path = '/var/togsync/config.json'
    conf = Config(SETTINGS, path).load()
    log = Log(conf)
    cnx = Connect(conf, log)

    lo = LoadOrders(conf, cnx, log)
    lo.run()

    # disconnect
    if conf.conf.get('tabLoc', '') == "remote":
        cnx.conn['tab_ssh'].stop()

    if conf.conf.get('wdpLoc', '') == "remote":
        cnx.conn['wdp_ssh'].stop()

    log.info("Elvis has left the building ...")
    sys.exit("lights out")
