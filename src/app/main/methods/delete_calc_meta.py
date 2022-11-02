from typing import Tuple

def main(self, sku: str) -> Tuple[str, str]:
    """Checks if calc plugin keys exists on the main parent product, and if
    they keys exist, then they are deleted. The create_calculator_meta func
    will re-create these keys on the next update."""

    qstr = """
    DELETE FROM wp_postmeta
    WHERE (
        meta_key = '_area' OR
        meta_key = '_volume' OR
        meta_key = '_wc_measurement_price_calculator_min_price' OR
        meta_key = '_wc_price_calculator'
        )
    AND post_id IN (
        SELECT ID
        FROM wp_posts
        WHERE
            ID IN (
                SELECT product_id
                FROM wp_wc_product_meta_lookup
                WHERE sku = '%s'
            )
            OR post_parent IN (
                SELECT product_id
                FROM wp_wc_product_meta_lookup
                WHERE sku = '%s'
            )
    )
    """ % (sku, sku)
    _, _ = self.cnx.q_db(serv="wdp", qstr=qstr)
    return _, _
