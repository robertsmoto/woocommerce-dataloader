def main(crud_operation: str, wdp_id: int) -> list:
    cmd_lst = ['wp', 'wc', 'product', f"{crud_operation}"]

    if crud_operation == 'update' and wdp_id == 0:
        return []

    cmd_lst.append(f"{str(wdp_id)}")

    return cmd_lst
