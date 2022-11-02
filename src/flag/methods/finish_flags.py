from . import append_flag


def main(self, cmd_lst: list, **kwargs) -> list:
    """Pass in flag_name=value and it will add these attributes to the flags.
    Such as: type="simple" and it will add --type="simple" to the flags."""

    cmd_lst = [] if not cmd_lst else cmd_lst

    for k, v in kwargs.items():

        k = 'type' if k == 'ptype' else k

        if k == 'porcelain':
            cmd_lst.append('--porcelain')
            continue

        if k == 'cred':
            cmd_lst = append_flag.main(self, cmd_lst, 'path', '/var/www/html')
            cmd_lst = append_flag.main(self, cmd_lst, 'user', 'robertsmoto')
            continue

        cmd_lst = append_flag.main(self, cmd_lst, k, v)

    return cmd_lst
