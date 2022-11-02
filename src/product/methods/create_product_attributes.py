from typing import List, Tuple
from product.qstrs.qstrs import qstr_attributes_by_pid
from data.data import ProcessorData


def variation_dict(vid, pos, vis, var, options):
    """Returns a formatted dict."""
    return {
            "id": vid,
            "position": pos,
            "visible": vis,
            "variation": var,
            "options": options
            }


def create_variation_attributes(self, data: ProcessorData) -> Tuple[list, dict, int]:
    """Builds all product attributes both for variations and
    visible attributes."""

    # main attributes
    # build all the main attributes here in list of dicts format
    """
    [{
        'id':'6',
        'position':'0',
        'visible':true,
        'variation':true,
        'options':['38','39','40']
    }]
    """
    var_index = {
            'size1': '99',
            'size2': '100',
            'size3': '101',
            'color': '2',
            'pattern': '3',
            'design': '102'
            }

    attributes_list = [] # <-- master list for vapr
    attributes_index = {} # <-- by sku for each product
    position = 0

    # make variations index
    for key, value in var_index.items():
        options_list = []
        for prod in data.cleaned_data:
            if not prod:
                continue
            if prod[key] and prod[key] not in options_list:
                options_list.append(prod[key])
            # make index by sku like this
            # {'sku': [{'options': 'xx'}, {'options': 'yy'}]
            sku = prod.get('sku', '')
            if sku not in attributes_index:
                attributes_index[sku] = []

            if prod[key]:
                attributes_index[sku].append({
                        'id': value,
                        'option': prod[key]
                        })

        is_variation = "true"
        if data.komplexity == 'simple':
            is_variation = "false"

        if options_list:
            var_dict = variation_dict(
                    vid=var_index[key],
                    pos=position,
                    vis="true",
                    var=is_variation,
                    options=options_list)

            attributes_list.append(var_dict)
            position += 1

    return attributes_list, attributes_index, position


def create_non_variation_attrs(records: List[dict], position: int) -> list:

    attributes_list = []
    for r in records:
        # make options list from att_term
        # for some reason these strings are decoded, so encode them
        options_list = [x.strip() for x in r['att_term'].split(',')]
        var_dict = variation_dict(
                vid=r['tog_id'],
                pos=position,
                vis="true",
                var="false",
                options=options_list)
        attributes_list.append(var_dict)
        position += 1

    return attributes_list


def main(self, data: ProcessorData) -> Tuple[ProcessorData, str]:
    """Buids all the attributes for each variation and the master attrs
    for the variable product."""

    err = ''
    # returns: tog_id, att_term

    # this is for attributes that *are* product variations
    # return 'attributes' key for each record,
    # and d.vapr_attributes for the master list
    # also return a position that can be used below
    attributes_list, attributes_index, position = create_variation_attributes(self, data)

    # this is for visible attributes that are *not* variations
    # requires postion from function above
    pid = data.cli_pid_group
    qstr = qstr_attributes_by_pid(str(pid))
    _, records = self.cnx.q_db('cli', qstr)
    non_variation_attrs = create_non_variation_attrs(records, position)

    attributes_list.append(non_variation_attrs)

    data.attributes_list = attributes_list
    data.attributes_index = attributes_index
    data.err = err

    return data, err
