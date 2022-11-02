from product.qstrs.qstrs import qstr_get_tab_vapr_qnty
from product.qstrs.qstrs import qstr_wdp_products_by_sku
from data.data import ProcessorData
from typing import Tuple


def main(self, data: ProcessorData) -> Tuple[ProcessorData, str]:
    """Inspects a variable product and adds some operational information
    to the dataclass."""

    err = ''
    first_product = data.cleaned_data[0] if data.cleaned_data else {}
    if not first_product:
        err = "Can't find the first product."
        return data, err

    sku = first_product.get('sku', '')
    sku = f'VAR-{sku}'
    data.vapr_sku = sku
    pid = first_product.get('pid', '')

    # check if wdp product exists and then set 'update' or 'create'
    wdp_products = []
    if sku:
        qstr = qstr_wdp_products_by_sku(sku)
        _, wdp_products = self.cnx.q_db(serv="wdp", qstr=qstr)

    data.vapr_operation = 'create'
    if wdp_products:
        product_id = wdp_products[0].get('product_id', 0)
        if product_id > 0:
            data.vapr_operation = 'update'
            data.vapr_id = product_id


    # if vapr is 'create', need to update each image
    # so update the records
    for rec in data.cleaned_data:
        rec['img_updated_true'] = 1

    # calculate d.vapr_quantity
    qstr = qstr_get_tab_vapr_qnty(pid)
    _, records = self.cnx.q_db('cli', qstr)
    self.log.debug(f"########### get sum here --> {records}")

    sum_qnty = 0
    if records:
        sum_qnty = records[0].get('sum', 0)
        data.vapr_quantity = sum_qnty
        self.log.debug(f"## vapr_quantity {data.vapr_quantity}")

    in_stock = True
    if sum_qnty <= 0:
        in_stock = False
    data.vapr_in_stock = in_stock

    return data, err
