from data.data import ProcessorData

def update_quantity(self, sku: str, stock_quantity: float) -> None:
    """ Update the wdp database with they original stock_quantity. """

    qstr = """
        UPDATE wp_wc_product_meta_lookup
        SET stock_quantity = %s
        WHERE sku = '%s';""" % (stock_quantity, sku)

    _, _ = self.cnx.q_db("wdp", qstr)

    qstr = """
        UPDATE wp_postmeta
        SET meta_value = %s
        WHERE meta_key = '_stock'
        AND post_id IN (
            SELECT product_id
            FROM wp_wc_product_meta_lookup
            WHERE sku = '%s');""" % (stock_quantity, sku)

    _, _ = self.cnx.q_db("wdp", qstr)

    return self

def main(self, processor_data: ProcessorData) -> None:
    for product in processor_data.cleaned_data:
        sku = product.get('sku', '')
        stock_quantity = product.get('stock_quantity_raw', 0.0)
        if not sku and stock_quantity:
            continue
        update_quantity(self, sku, stock_quantity)
        self.log.debug(f"Updated decimal values sku: {sku}, qnty: {stock_quantity}")

    return self
