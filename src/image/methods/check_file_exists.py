from typing import Tuple
import os


def main(self, serv: str, file_path: str) -> Tuple[bool, str]:
    """Checks if file exists on either 'local' or 'remote' server."""

    wdp_loc = self.conf.conf.get('wdpLoc', '')
    cli_loc = self.conf.conf.get('cliLoc', '')

    serv_index = {
            'wdp': wdp_loc,
            'cli': cli_loc,
            }

    serv_loc = serv_index.get(serv, '')

    def check_file_exists_local(path="") -> Tuple[bool, str]:
        """ checks that file exist on local computer """
        exists = os.path.isfile(path)
        return exists, ''

    def check_file_exists_remote(path="") -> Tuple[bool, str]:
        """ checks that file exist on remote computer """
        cmd = [
                '[[', '-f', f'{path}', ']]', '&&', 'echo', 'File exists',
                '||', 'echo', 'File does not exist', ';'
            ]

        output, err = self.cnx.subprocess(serv, cmd)
        self.log.debug(f"Check file remote output {output} type {type(output)}, err {err}")
        exists = True
        if output != 'File exists':
            exists = False
        return exists, err

    if serv_loc == 'local':
        self.log.debug(f"Check file local: {file_path}")
        return check_file_exists_local(path=file_path)

    if serv_loc == 'remote':
        self.log.debug(f"Check file remote: {file_path}")
        return check_file_exists_remote(path=file_path)

    return False, f"Unable to run filecheck {file_path}."
