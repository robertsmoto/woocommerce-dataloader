def main(self) -> None:
    """Checks if any variable products exist without variations and
    dfeletes them."""

    if not self.conf.conf.get('archiveVariationOrphans', False):
        return self
    self.log.info("Checking for variation orphans ...")

    select_str = """
    SELECT p.ID, wc.sku
    FROM wp_posts p
    JOIN wp_wc_product_meta_lookup wc
    ON p.ID=wc.product_id
    WHERE p.ID NOT IN
        (SELECT post_parent
        FROM wp_posts
        WHERE post_type='product_variation')
    AND wc.sku like 'vapr-%%'
    """

    _, orphans = connections.q_db(
        serv="wdp", qstr=select_str, conn=conn)

    err = ""
    for orphan in orphans:
        cmd_lst = ['wp', 'wc', 'product', 'delete', f'{orphan["ID"]}']
        cmd_lst = flags_utils.finish_flags(
                cmd_list=cmd_lst,
                cred=True,
                porcelain=True,
                force=True)
        _, err = utils_subprocess.run(serv="wdp", cmd=cmd_lst)
        utils_log.TogLog().info(
                f"Delete orphaned product wc post ID: {orphan['ID']}")

    if err:
        utils_log.TogLog().error(
                f"Failed to check variable product orphans: {err}")

    return orphans


