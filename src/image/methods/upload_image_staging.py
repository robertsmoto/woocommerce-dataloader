from . import check_file_exists
from . import secure_copy


def main(self, wdp_path: str, info_by_wdppath: dict):
    """Uploads images to the staging directory
    located at /home/huckfinn/uploads/staging"""

    err = ''
    cli_path = info_by_wdppath[wdp_path].get('cli_path', '')
    wdp_dir = info_by_wdppath[wdp_path].get('wdp_dir', '')

    # this builds the correct scp commands based on the
    # relative location of server making the call
    scp_cmd, _ = secure_copy.main(self,
        fserv='cli', fpath=cli_path, tserv='wdp', tdir=wdp_dir)

    # upload image to staging directory
    _, _ = self.cnx.subprocess('wdp', scp_cmd)

    # check image exist in wdp staging
    exists, err = check_file_exists.main(self, 'wdp', wdp_path)
    if not exists:
        err = f"Failed to upload {wdp_path} to staging."
        self.log.warn(err)

    return
