import os
from typing import Tuple


def main(self, image_data: list, sku: str) -> Tuple[dict, dict, dict]:
    # print("## image query -->", image_query)


    wdppaths_by_sku = {} # <-- {"sku": ["/path/xx", ....]}
    info_by_wdppath = {} # <-- {"/path/xx": {"wdp_id", .....}}
    featured_image = {}
    # cli_set = set() # client paths
    # wdp_set = set() # staging paths
    for img in image_data:
        picpath = img.get('picpath', '')
        picpath = picpath.replace("\\", "/")
        file_name = os.path.basename(picpath)
        cli_dir = self.conf.conf.get('cliImgDir', '')
        wdp_dir = self.conf.conf.get('wdpImgDir', '')
        cli_path = f"{cli_dir}/{file_name}"
        wdp_path = f"{wdp_dir}/{file_name}"
        skus = img.get('sku', '') # <-- is a list of skus returned by query
        skus.append(sku) # <-- adds in sku from above in case list is empty

        if img.get('hlavny', False):
            featured_image['path'] = wdp_path

        for sku in skus:
            sku_exists = wdppaths_by_sku.get(sku, False)
            if not sku_exists:
                wdppaths_by_sku[sku] = []  # <-- create it
                wdppaths_by_sku[sku].append(wdp_path)

            wdppath_exists = info_by_wdppath.get(wdp_path, '')
            if not wdppath_exists:
                info_by_wdppath[wdp_path] = {}
                info_by_wdppath[wdp_path]['file_name'] = file_name
                info_by_wdppath[wdp_path]['cli_dir'] = cli_dir
                info_by_wdppath[wdp_path]['wdp_dir'] = wdp_dir
                info_by_wdppath[wdp_path]['cli_path'] = cli_path
                info_by_wdppath[wdp_path]['wdp_path'] = wdp_path
                info_by_wdppath[wdp_path]['image'] = img
                # also 'wdp_id' is added in later when image is uploaded to wdp

    return wdppaths_by_sku, info_by_wdppath, featured_image
