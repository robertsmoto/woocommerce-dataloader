def main(self, check):
    """ Checks for new orders in wdp (check='new') or orphaned orders in tab
    (check='orphans')."""

    selectall = "tab"
    compareto = "wdp"
    if check == "orphans":
        selectall = "wdp"
        compareto = "tab"

    qstr = """
    SELECT stats.order_id
    FROM wp_wc_order_stats stats"""

    n_all_orders, all_orders = self.cnx.q_db(selectall, qstr)

    all_orders_list = [x['order_id'] for x in all_orders]
    all_orders_str = self.cnx.str_from_list(all_orders_list, 'no')

    qstr = """
    SELECT order_id
    FROM wp_wc_order_stats """

    if n_all_orders > 0:
        qstr = """
        SELECT order_id
        FROM wp_wc_order_stats
        WHERE order_id NOT IN (%s) """ % (all_orders_str)

    n_notin_orders, notin_orders = self.cnx.q_db(compareto, qstr)

    return n_notin_orders, notin_orders
