from . methods import *
from processor.processor import Processor
from data.data import ProcessorData


class FlagSimple(Processor):
    """This processes both simple and variation products."""

    def process(self, data: ProcessorData) -> ProcessorData:
        if data.err:
            return data

        for product in data.cleaned_data:
            # create base command
            crud_operation = product.get('crud_operation', 'update')
            wdp_id = product.get('wdp_id', 0)
            if crud_operation == 'update' and wdp_id == 0:
                data.err = "FlagSimple, cannot update product without wdp_id"
                continue
            cmd_lst = create_cmd_simple.main(crud_operation, wdp_id)

            # build the base product flags, common for simple and variation
            cmd_lst = create_flags_base.main(self, product, cmd_lst)

            # certain flags need to be added for simple products
            cmd_lst = add_flags_simple.main(self, product, cmd_lst)

            # add dimensions
            cmd_lst = add_product_dimensions.main(self, product, cmd_lst)

            # add the images
            infobypath = data.info_by_wdppath
            fi = data.featured_image
            cmd_lst = add_image_list.main(self, cmd_lst, infobypath, fi)

            # d.attributes_list for product
            crud_operation = product.get('crud_operation', '')

            if crud_operation == 'create':
                attributes = data.attributes_list
                cmd_lst = append_flag.main(self, cmd_lst, 'attributes', attributes)

            # finish the flags
            cmd_lst = finish_flags.main(
                    self,
                    cmd_lst=cmd_lst,
                    ptype='simple',
                    sku=product.get('sku', ''),
                    cred=True
                    )

            data.cmd_lst.append(cmd_lst)

        return data

class FlagVariation(Processor):
    """This processes both simple and variation products."""

    def process(self, data: ProcessorData) -> ProcessorData:
        if data.err:
            return data

        for product in data.cleaned_data:
            sku = product.get('sku', '')
            cmd_lst = []

            # base cmd_lst 
            crud_operation = product.get('crud_operation', 'update')
            wdp_id = product.get('wdp_id', 0)
            vapr_id = data.vapr_id
            if crud_operation == 'update' and wdp_id == 0:
                crud_operation = 'create'
            if vapr_id == 0:
                data.err = "FlagVariation, cannot create or update variation without vapr_id."
            cmd_lst = create_cmd_variation.main(crud_operation, vapr_id, wdp_id)

            # build the base product flags, common for simple and variation
            cmd_lst = create_flags_base.main(self, product, cmd_lst)

            # add dimensions
            cmd_lst = add_product_dimensions.main(self, product, cmd_lst)

            # add image
            wdpbysku = data.wdppaths_by_sku
            infobypath = data.info_by_wdppath
            cmd_lst = add_image_variation.main(self, cmd_lst, sku, wdpbysku, infobypath)

            # attributes, add only if 'create'
            crud_operation = product.get('crud_operation', '')
            if crud_operation == 'create':
                attributes = data.attributes_index[sku]
                cmd_lst = append_flag.main(self, cmd_lst, 'attributes', attributes)

            # finish the flags
            cmd_lst = finish_flags.main(
                    self,
                    cmd_lst=cmd_lst,
                    sku=product.get('sku', ''),
                    cred=True,
                    porcelain=True,
                    )

            # append data.cmd_list
            data.cmd_lst.append(cmd_lst)

        return data

class FlagVariable(Processor):
    """This processes flags for the parent variable product.
    It needs to run before FlagSimpleVariation because the latter
    needs a vapr_id to build variation flags."""

    def process(self, data: ProcessorData) -> ProcessorData:
        if data.err:
            return data

        # create base command
        vapr_id = data.vapr_id
        cmd_lst = create_cmd_variable.main(vapr_id)

        # build the base variable flags from the first product in d.cleaned_data
        first_product = data.cleaned_data[0] if data.cleaned_data else {}
        cmd_lst = create_flags_variable.main(self, first_product, cmd_lst)

        # now add the specifiic vapr attrs to the cmd_lst
        cmd_lst = append_flag.main(self, cmd_lst, 'sku', data.vapr_sku)
        cmd_lst = append_flag.main(self, cmd_lst, 'in_stock', data.vapr_in_stock)
        # cmd_lst = append_flag.main(self, cmd_lst, 'stock_quantity', data.vapr_quantity)
        # cmd_lst = append_flag.main(self, cmd_lst, 'manage_stock', data.vapr_manage_stock)

        # add dimensions to variable, using first product info
        cmd_lst = add_product_dimensions.main(self, first_product, cmd_lst)

        # add the images, if they exist
        infobypath = data.info_by_wdppath
        fi = data.featured_image
        cmd_lst = add_image_list.main(self, cmd_lst, infobypath, fi)

        # add categories
        category = first_product.get('categories', '')
        if category:
            cmd_lst = append_flag.main(self, cmd_lst, 'categories', category)

        # add attributes only on 'create'
        if data.vapr_operation == 'create':
            # d.attributes_list for simple products and variable products
            cmd_lst = append_flag.main(self, cmd_lst, 'attributes', data.attributes_list)

        cmd_lst = finish_flags.main(
            self,
            cmd_lst=cmd_lst,
            ptype=data.komplexity,
            sku=data.vapr_sku,
            cred=True,
            porcelain=True)

        # append cmd_list to vapr_cmd_lst
        data.vapr_cmd_lst.append(cmd_lst)

        return data


class FlagBrand(Processor):
    """Creates and processes brands for given data."""


    def process(self, data: ProcessorData) -> ProcessorData:
        if data.err:
            return data

        # create the brand command
        commands = create_cmd_brand.main(self, data)
        
        # send them
        for cmd in commands:
            self.cnx.subprocess('wdp', cmd)
        
        return data
