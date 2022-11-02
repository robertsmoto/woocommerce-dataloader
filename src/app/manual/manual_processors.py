import config_env
import connections
import sys
import utils


def find_not_imported_products(conn):
    """Finds all tab products that have not been imported to wdp
    regardless of is_updated."""

    # find all products in wdp
    qstr = """
    SELECT sku
    FROM wp_wc_product_meta_lookup
    WHERE sku NOT LIKE 'vapr%'
    OR sku NOT LIKE 'zzz%' """

    n_wskus, wskus = connections.q_db(conn=conn, serv="wdp", qstr=qstr)
    wskus_list = [x['sku'] for x in wskus]
    wskus_str = utils.str_from_list(data_list=wskus_list, quoted='yes')

    # find products in tab that don't exist in wdp
    qstr = """
    SELECT sku
    FROM products
    WHERE sku NOT IN (%s) """ % (wskus_str)

    n_tskus, tskus = connections.q_db(conn=conn, serv="tab", qstr=qstr)
    tskus_list = [x['sku'] for x in tskus]
    tskus_str = utils.str_from_list(data_list=tskus_list, quoted='yes')

    print("tab skus notin wdp\n", tskus_str)

    return


if __name__ == "__main__":
    """Updates simple products is_updated = true."""

    conn = connections.create_all_connections()

    qstr = """
        UPDATE tblsklad
        SET is_updated = 'true'
        WHERE pid in (
            SELECT pid
            FROM products
            WHERE komplexity = 'variable');"""

    _, _ = connections.q_db(serv="tab", conn=conn, qstr=qstr)

    # close connections and exit the program
    if config_env.tab_loc == "remote":
        conn['tab_ssh'].stop()

    if config_env.wdp_loc == "remote":
        conn['wdp_ssh'].stop()

    sys.exit("Exiting main program ...")
