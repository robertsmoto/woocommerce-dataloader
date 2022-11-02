def main(self, order, serv: str):
    qstr = """
    UPDATE wp_wc_order_stats
    SET status = '%s'
    WHERE order_id = %s """ % (order['status'], order['order_id'])

    _, _ = self.cnx.q_db(serv, qstr)

    # wdp needs an additional table updated with order_status
    if serv == "wdp":
        qstr = """
        UPDATE wp_posts
        SET post_status = '%s'
        WHERE post_type = 'shop_order'
        AND ID = %s """ % (order['status'], order['order_id'])
        _, _ = self.cnx.q_db(serv, qstr)

    return


