from log.log import Log
from connection.connection import Connect


def delete_wdp_post_meta(postid_str, conn):

    logging.info(f"Deleting these meta ids {postid_str} ...")

    qstr = """
        DELETE FROM wp_postmeta
        WHERE post_id IN (%s) """ % (postid_str)

    return connections.q_db(serv="wdp", qstr=qstr, conn=conn)


def get_dup_post_meta(sku_str: str, conn: dict):
    logging.info(f"Deleting these meta records {sku_str} ...")

    qstr = """
        SELECT post_id
        FROM wp_postmeta
        WHERE meta_key = '_sku'
        AND meta_value IN (%s) """ % (sku_str)

    return connections.q_db(serv="wdp", qstr=qstr, conn=conn)


def check_dup_post_meta(conn):
    # checks for dupe skus in wordpress post meta

    qstr = """
        SELECT meta_value,
        COUNT(meta_value)
        FROM wp_postmeta
        WHERE meta_key = '_sku'
        GROUP BY meta_value
        HAVING COUNT(meta_value) > 1 and meta_value != ''
        """

    return connections.q_db(serv="wdp", qstr=qstr, conn=conn)


def main(self):
    """ Checks if there are duplicate skus, although there
    *should* not be any """

    if not self.conf.conf.get('deleteDuplicateSkus', False):
        return self
    utils_log.TogLog().info("Checking for duplicate skus ...")

    # checks for dup skus in woocommerce meta
    qstr = """
        SELECT sku,
        COUNT(sku)
        FROM wp_wc_product_meta_lookup
        GROUP BY sku
        HAVING COUNT(sku) > 1 AND sku != ''
        """

    _, skus = connections.q_db(
        serv="wdp", qstr=qstr, conn=conn)

    if not skus:
        return []

    logging.info("Dupliate skus found ...")
    print("Dupliate skus found ...")
    sku_list = [sku['sku'] for sku in skus]

    sku_set = set(sku_list)

    sku_str = ", ".join("'%s'" % sku for sku in sku_set)
    logging.info(f"Removing skus {sku_str} ...")
    print(f"Removing skus {sku_str} ...")

    # delete wordpress records by sku
    _, _ = utils.del_wp_wc_product_meta_lookup_sku(sku_str=sku_str, conn=conn)

    # get wp_posts.ID by sku
    _, wp_ids = utils.get_wp_posts_sku(sku_str=sku_str, conn=conn)

    # delete wp_posts records by sku
    wpid_list = [pid.get('ID', '') for pid in wp_ids]
    wpid_set = set(wpid_list)
    wpid_str = ", ".join("%s" % pid for pid in wpid_set)
    if wpid_set:
        _, _ = utils.del_wp_posts_id(id_str=wpid_str, conn=conn)

    return
