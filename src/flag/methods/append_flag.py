from typing import Any
import json


def main(self, cmd_lst: list, k: str, v: Any) -> list:
    """Appends a flag to the cmd_lst."""

    if isinstance(v, dict) or isinstance(v, list):
        if self.conf.conf.get('wdpLoc', 'remote') == 'local':

            # keeping image and atttrs out of command for now
            cmd_lst.append(f'--{k}={json.dumps(v)}'.replace(' ', ''))
            return cmd_lst
        else:
            cmd_lst.append(f"--{k}='{json.dumps(v)}'")
            return cmd_lst

    # double quote conditions
    double_quote_conditions = [
            k.startswith('name'),
            k.startswith('short'),
            k.startswith('description'),
            ]

    if any(double_quote_conditions):
        cmd_lst.append(f'--{k}="{str(v)}"')
        return cmd_lst

    cmd_lst.append(f'--{k}={str(v)}')

    return cmd_lst
