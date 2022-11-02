def qstr_get_tab_vapr_qnty(pid: str) -> str:
    return """
        SELECT sum(stock_quantity)
        FROM products
        WHERE pid = '%s';""" % (pid)

def qstr_get_all_products_by_pid(pid: str) -> str:
    return """
        SELECT *
        FROM products
        WHERE pid = '%s';""" % (pid)

def qstr_attributes_by_pid(pid: str) -> str:
    return """
        SELECT tog_id, att_term
        FROM attributes
        WHERE pid = '%s'
        ORDER BY tog_id;""" % (pid)

def qstr_delete_wc_product_by_id(postId: str) -> str:
    """Takes a list of ids and deletes associated wp records."""
    return """
        DELETE
        FROM wp_wc_product_meta_lookup
        WHERE product_id = (%s);""" % (postId)

def qstr_delete_wp_post_by_id(postID: str) -> str:
    """ Takes a post.ID and deletes the wp_posts records."""
    return """
        DELETE FROM wp_posts
        WHERE ID = %s;""" % (postID)

def qstr_delete_wp_postmeta_by_id(postID: str) -> str:
    """ Takes a post.ID and deletes the wp_posts records."""
    return """
        DELETE FROM wp_postmeta
        WHERE post_id = %s;""" % (postID)

def qstr_wdp_products_by_sku(sku: str) -> str:
    """ Takes a single sku and returns wp_wc_product_meta_lookup."""
    return """
        SELECT *
        FROM wp_wc_product_meta_lookup AS wc
        JOIN wp_posts AS p ON p.ID = wc.product_id
        WHERE wc.sku = '%s';""" % (sku)
