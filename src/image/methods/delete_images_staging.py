import os

def main(self, info_by_wdppath: dict):
    """Deletes all images in the self.staging_list."""

    # this needs to operate either on local or remote
    staging_set = set()
    for wdp_path, _ in info_by_wdppath.items():
        staging_set.add(wdp_path)

    if not staging_set:
        return self

    if self.conf.conf.get('wdpLoc', '') == 'local':
        for f_path in staging_set:
            if os.path.exists(f_path):
                os.remove(f_path)
    else:
        rmstr = ' '.join([f_path for f_path in staging_set])
        cmd = ['rm', rmstr]
        self.cnx.subprocess('wdp', cmd)
    return self
