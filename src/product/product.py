from . methods import *
from processor.processor import Processor
from data.data import ProcessorData


class Product(Processor):
    """Validates, inspects and creates attributes for all product types."""

    def process(self, data: ProcessorData) -> ProcessorData:
        if data.err != '':
            return data

        # validate data
        cleaned_list, err = product_validation.main(self, data.product_data)
        data.cleaned_data = cleaned_list
        data.err = err if err else ''
        self.log.debug("###### clean_data {data}")


        first_product = data.cleaned_data[0] if data.cleaned_data else {}
        data.komplexity = first_product.get('komplexity', 'simple')
        data.err = err if err else ''

        self.log.debug(f"komplexity {data.komplexity}")
        # inspect variable product
        # this adds the data vapr_ information
        if data.komplexity == 'variable':
            data, err = inspect_variable_product.main(self, data)
            data.err = err if err else ''

        # inspect each product in cleaned_data
        # checks wdp, adds 'wdp_id' and 'crud_operation' to each record
        # self.log.debug(f"cleaned_data {data.cleaned_data}")
        data, err = inspect_simple_product.main(self, data)
        data.err = err if err else ''

        # creates d.attributes_list and d.attributes_index used for all product types
        data, err = create_product_attributes.main(self, data)
        data.err = err if err else ''

        return data
