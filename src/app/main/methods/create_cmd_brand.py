from flag.methods import finish_flags


def main(self, wdp_id: int, brand: str) -> list:

    cmd_lst = []

    if not wdp_id or not brand:
        return cmd_lst 

    cmd_lst = [
            'wp', 'post', 'term', 'set', f'{str(wdp_id)}',
            'product_brand', f'{brand}'
            ]

    cmd_lst = finish_flags.main(self, cmd_lst, cred=True)

    return cmd_lst
