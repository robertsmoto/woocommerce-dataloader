def main(self) -> None:
    """
    Checks for Wdp orphans.
    These products were either entered in Wordpress or deleted at TABAT
    mark the posts as 'draft' and change the sku to a zzzz-random-string
    then only compare records which sku NOT LIKE 'zzzz%%' or 'vapr%%'
    """
    if not self.conf.conf.get('archiveWdpOrphans', False):
        return self
    self.log.info("Checking orphans ...")

    tab_select = """
        SELECT sku
        FROM products """

    _, tabprod = connections.q_db(
            serv='tab', qstr=tab_select, conn=conn)

    tab_sku_str = ", ".join("'%s'" % p['sku'] for p in tabprod)

    wdp_select = """
        SELECT wc.sku, p.post_status
        FROM wp_wc_product_meta_lookup wc
        INNER JOIN wp_posts p ON p.ID=wc.product_id
        WHERE wc.sku NOT IN (%s)
        AND wc.sku NOT LIKE 'vapr-%%'
        AND wc.sku NOT LIKE 'zzzz-%%'
        """ % (tab_sku_str)

    n_orphans, orphans = connections.q_db(
        serv='wdp', qstr=wdp_select, conn=conn)

    for orphan in orphans:
        status = orphan.get('post_status', '')
        if status == 'pending':
            continue
        wdpids_dict = utils.q_wdp_pids(prod=orphan, conn=conn)
        err = utils.remove_wdp_orphans(wdp_ids=wdpids_dict)
        if err:
            utils_log.TogLog().error(f"{err}")

    if orphans:
        utils_log.TogLog().info(f"{n_orphans} wdp orphans w status 'pending'.")

    return


