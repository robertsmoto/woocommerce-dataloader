def main(vapr_id: int) -> list:

    cmd_lst = ['wp', 'wc', 'product']

    vapr_oper = 'create'
    if vapr_id != 0:
        vapr_oper = 'update'
    cmd_lst.append(vapr_oper)

    if vapr_oper == 'update':
        cmd_lst.append(f'{str(vapr_id)}')

    return cmd_lst




