from app.orders.methods import update_order_status


def main(self, orders: list, ALL_STATUS_TYPES: dict):
    """ Checks changed orders and updates the wp_wc_order_stats on
    the correct server. """

    # select wp_wc_order_stats from each serv
    for order in orders:
        """orders list contains tuples (order_id, status).
        This loop compares and updates one record at a time."""

        qstr = """
        SELECT *
        FROM wp_wc_order_stats
        where order_id = %s """ % (order[0])

        _, tab_status = self.cnx.q_db("tab", qstr)
        _, wdp_status = self.cnx.q_db("wdp", qstr)

        tab_status = tab_status[0]
        wdp_status = wdp_status[0]

        # determine which server needs to be updated by comparing the two
        # greater server updates lesser server
        tab_priority = ALL_STATUS_TYPES[tab_status['status']]
        wdp_priority = ALL_STATUS_TYPES[wdp_status['status']]
        if tab_priority > wdp_priority:
            # update wdp with tab_status
            update_order_status.main(self, serv="wdp", order=tab_status)
        else:
            # update tab with wdp status
            update_order_status.main(self, serv="tab", order=wdp_status)
    return

