from . import append_flag


def main(self, product: dict, cmd_lst: list) -> list:
    """Adds product dimension flags to product flags."""

    l = product.get('length', '')
    w = product.get('width', '')
    h = product.get('height', '')

    conditions = [l, w, h]
    if not all(conditions):
        return cmd_lst

    dimensions = {}
    dimensions['length'] = l
    dimensions['width'] = w
    dimensions['height'] = h
    cmd_lst = append_flag.main(self, cmd_lst, 'dimensions', dimensions)

    return cmd_lst



