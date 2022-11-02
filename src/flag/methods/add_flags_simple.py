from . import append_flag


def main(self, product: dict, cmd_lst: list) -> list:
    """Creates base product flags for both simple and variable products."""
    product_attrs = {
        'catalog_visibility',
        'categories',
        'name',
        'reviews_allowed',
        'short_description', 
        'slug',
        'status',
        'type',
        }

    for key in product_attrs:
        value = product.get(key, '')
        if not value:
            continue
        cmd_lst = append_flag.main(self, cmd_lst, key, value)

    return cmd_lst
