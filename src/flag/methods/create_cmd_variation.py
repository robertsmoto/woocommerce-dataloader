def main(crud_operation: str, vapr_id: int, wdp_id: int) -> list:
    """Creates or updates the variation."""
    cmd_lst =  ['wp', 'wc', 'product_variation']

    cmd_lst.append(f"{crud_operation}")
    cmd_lst.append(f'{str(vapr_id)}')
    if wdp_id != 0:
        cmd_lst.append(f'{str(wdp_id)}')

    return cmd_lst
