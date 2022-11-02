from . import append_flag


def main(self, product: dict, cmd_lst: list) -> list:
    """Creates base product flags for both simple and variable products."""

    product_attrs = {
        'backorders',
        'catalog_visibility',
        'categories',
        'date_on_sale_from',
        'date_on_sale_to',
        'description',
        'featured', 
        'name',
        'regular_price',
        'reviews_allowed',
        'sale_price', 
        'shipping_class',
        'short_description', 
        'slug',
        'sold_individually',
        'status',
        'tax_class',
        'tax_status',
        'type',
        }

    for key in product_attrs:
        value = product.get(key, '')
        if not value:
            continue
        cmd_lst = append_flag.main(self, cmd_lst, key, value)

    return cmd_lst
