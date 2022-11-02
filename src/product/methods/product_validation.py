from typing import Tuple
import math
import re
import unidecode


def strip_bad(attr: str) -> str:
    return attr.replace('"', '').strip("\n ")

def slugify(attr: str):
    slug = unidecode.unidecode(attr).lower()
    slug = re.sub("[^0-9a-zA-Z]+", "-", slug)
    return slug[:20]

def clean_record(self, data: dict) -> Tuple[dict, str]:
    """Validates and cleans product attributes."""
    err = ''
    cd = {}
    # fields needed for futher processing
    cd['pid'] = data.get('pid', 0)
    cd['var_product'] = data.get('var_product', False)
    cd['is_updated'] = data.get('is_updated', False)
    cd['img_updated_true'] = data.get('img_updated_true', 0)
    cd['image_exists'] = data.get('image_exists', '')
    cd['komplexity'] = data.get('komplexity', 'simple')
    cd['size1'] = data.get('size1', '')
    cd['size2'] = data.get('size2', '')
    cd['size3'] = data.get('size3', '')
    cd['color'] = data.get('color', '')
    cd['pattern'] = data.get('pattern', '')
    cd['design'] = data.get('design', '')
    cd['brand'] = data.get('brand', '')
    # these are the basic flag attributes
    cd['name'] = strip_bad(data.get('name', ''))
    cd['status'] = data.get('status', '')
    # a boolean indicates if the product is featured (not featured image)
    cd['featured'] = data.get('featured', '')
    cd['catalog_visibility'] = data.get('catalog_visibility', '')
    cd['description'] = strip_bad(data.get('description', ''))
    cd['short_description'] = strip_bad(
            data.get('short_description', ''))
    cd['regular_price'] = data.get('regular_price', 0)
    cd['sale_price'] = data.get('sale_price', 0)
    dosf = data.get('date_on_sale_from', '')
    if dosf:
        dosf = dosf.split()[0]
    cd['date_on_sale_from'] = dosf
    cd['date_on_sale_to'] = data.get('date_on_sale_to', '')
    cd['tax_status'] = data.get('tax_status', '')
    cd['tax_class'] = data.get('tax_class', '')
    cd['manage_stock'] = data.get('manage_stock', True)
    cd['backorders'] = "no"
    cd['sold_individually'] = data.get('sold_individually', '')
    cd['shipping_class'] = data.get('shipping_class', '')
    cd['reviews_allowed'] = data.get('reviews_allowed', '')

    cd['sku'] = data.get('sku', '')
    cd['slug'] = data.get('sku', '')

    # check for float in flats_utils
    stock_qnty = data.get('stock_quantity', 0)
    cd['stock_quantity_raw'] = stock_qnty # <-- preserves the orig value of stock_qnty
    cd['stock_quantity'] = math.floor(stock_qnty)
    self.log.debug(f"stock quantity {cd['stock_quantity']} {type(cd['stock_quantity'])}")

    cd['in_stock'] = True
    if stock_qnty <= 0:
        stock_qnty = 0
        cd['in_stock'] = False

    # dimensions
    cd['length'] = data.get('length', '')
    cd['width'] = data.get('width', '')
    cd['height'] = data.get('height', '')

    # categories
    # this will need special formatting when flags are built
    # list of dics [{"id": 44}, {"id": 22}]
    categories = data.get('categories', '')
    cat_dict = {}
    cat_dict['id'] = f'{categories}'
    cat_list = []
    cat_list.append(cat_dict)
    cd['categories'] = cat_list if categories else []

    self.log.debug(f"##### categories {cd['categories']}", )
    return cd, err

def main(self, data: list) -> Tuple[list, str]:
    err = ''
    cleaned_list = []
    for record in data:
        cr, err = clean_record(self, record)
        if err:
            return data, err
        cleaned_list.append(cr)
    return cleaned_list, err
