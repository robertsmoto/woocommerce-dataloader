from typing import Tuple

def main(self, fserv: str, fpath: str, tserv: str, tdir: str) -> Tuple[list, str]:
    """Determines whether a local scp or third-party scp should be used."""

    conf = self.conf.conf
    wdphost = f"{conf.get('DOSSH_USER', '')}@{conf.get('DOSSH_IP', '')}"
    clihost = f"{conf.get('SSH_USER', '')}@{conf.get('SSH_IP', '')}"

    fhost = wdphost if fserv == 'wdp' else clihost
    thost = wdphost if tserv == 'wdp' else clihost

    # assumes the fserver (from server) is remote that's why using scp
    # checks if the  tserver (to server) is local or remote
    # and changes the scp command accordingly

    t_loc = self.conf.conf.get('wdpLoc', '') \
            if tserv == 'wdp' else self.conf.conf.get('cliLoc', '')

    def secure_copy_local(fhost=None, fpath=None, tdir=None) -> list:
        """
        Note: the scp syntax is correct.
        There is not a port specified.
        You must have local <config> file at home/user/.ssh/<config>
        """
        command = ['scp', f'{fhost}:{fpath}', f'{tdir}']
        return command

    def secure_copy_thirdparty(
            fhost=None, fpath=None, thost=None, tdir=None) -> list:
        """
        Note: the scp syntax is correct.
        There is not a port secified.
        You must have local <config> file at home/user/.ssh/<config>
        """
        command = ['scp', '-3', f'{fhost}:{fpath}', f'{thost}:{tdir}']
        return command

    command = [] 
    if t_loc == 'remote':
        # is third-party remote to remote
        command = secure_copy_thirdparty(
            fhost=fhost, fpath=fpath, thost=thost, tdir=tdir)
    else:
        # is from local computer
        command = secure_copy_local(fhost=fhost, fpath=fpath, tdir=tdir)

    return command, ''
