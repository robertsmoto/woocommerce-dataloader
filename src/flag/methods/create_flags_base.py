from . import append_flag


def main(self, product: dict, cmd_lst: list) -> list:
    """Creates base product flags for both simple and variable products."""

    product_attrs = {
        'backorders',
        'date_on_sale_from',
        'date_on_sale_to',
        'description',
        'featured', 
        'in_stock',
        'manage_stock',
        'regular_price',
        'sale_price', 
        'shipping_class',
        'sku',
        'sold_individually',
        'stock_quantity',
        'tax_class',
        'tax_status',
        }

    for key in product_attrs:
        value = product.get(key, '')
        if key == 'stock_quantity':
            self.log.debug(f"## stock quantity --> {value}")
        if not value:
            continue
        cmd_lst = append_flag.main(self, cmd_lst, key, value)

    return cmd_lst
