def qstr_get_update_products_by_offset(offset: int = 0) -> str:
    return """
        SELECT *
        FROM products
        WHERE pid IN (
            SELECT DISTINCT pid 
            FROM products 
            WHERE is_updated = 'true' 
            ORDER BY pid ASC
            OFFSET %s LIMIT 1
        );""" % (offset)
