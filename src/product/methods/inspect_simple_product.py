from product.qstrs.qstrs import qstr_wdp_products_by_sku
from product.qstrs.qstrs import qstr_delete_wc_product_by_id
from product.qstrs.qstrs import qstr_delete_wp_post_by_id
from product.qstrs.qstrs import qstr_delete_wp_postmeta_by_id
from typing import Tuple
from data.data import ProcessorData


def main(self, data: ProcessorData) -> Tuple[ProcessorData, str]:
    """Checks a simple product and adds these keys to the product dict
        'crud_operation': "create | update"
        'wdp_id' = <id>."""

    err = ''
    for product in data.cleaned_data:

        sku = product.get('sku', '')
        data.cli_pid_group = product.get('pid', 0)
        data.brand = product.get('brand', '')

        # first query wp_wc_product_meta_lookup
        qstr = qstr_wdp_products_by_sku(sku)
        _, wc_products = self.cnx.q_db('wdp', qstr)

        first_product = wc_products[0] if wc_products else {}

        product['crud_operation'] = 'update'
        product['wdp_id'] =  ''
        product['img_updated_true'] = 0

        # update condition
        if not first_product:
            product['crud_operation'] = 'create'
            product['img_updated_true'] = 1
            return data, err

        # for current variation
        wdp_id = first_product.get('product_id', 0)
        product['wdp_id'] = wdp_id
        wdp_parent_id = wc_products[0].get('post_parent', 0)
        product['wdp_parent_id'] = wdp_parent_id

        # ##########################################################
        # # are conditions correct ??
        # print("############ crud_operation simple product inspection -->", product['crud_operation'])
        # print("############ variation wdp_id -->", product['wdp_id'])
        # print("############ variation parent id -->", product['wdp_parent_id'])
        # print("############ vapr id -->", vapr_id)
        # ##########################################################

        if wdp_parent_id != data.vapr_id:
            self.log.error(f"Variation parent_id {wdp_parent_id} != vapr_id {data.vapr_id}")
            self.log.warn("Attempting to fix the problem.")
            # leave the new vapr and delete the old variable and variation
            wdpids = [wdp_id, wdp_parent_id]
            qstr_list = []
            for wid in wdpids:
                qstr_list.append(qstr_delete_wc_product_by_id(wid))
                qstr_list.append(qstr_delete_wp_post_by_id(wid))
                qstr_list.append(qstr_delete_wp_postmeta_by_id(wid))

            for qstr in qstr_list:
                _, _ = self.cnx.q_db('wdp', qstr)

            # then set the product information corrently for create with vapr
            product['crud_operation'] = 'create'
            product['wdp_id'] = 0
            product['wdp_parent_id'] = data.vapr_id
            # since we have deleted the product, will need to also relaod images
            product['img_updated_true'] = 1

        self.log.info(f"{product.get('crud_operation', '')} {product.get('sku', '')} ...")

    return data, err
