from . import append_flag


def main(self, cmd_lst: list, sku: str, wdppaths_by_sku: dict, info_by_wdppath: dict) -> list:
    """Adds images flags to product flags. Expects a
    list of dicts for images, will return
    --image='{"id":"239"}'"""

    wdp_paths = wdppaths_by_sku.get(sku, '')
    path = wdp_paths[0] if wdp_paths else ''
    if not path:
        return cmd_lst
    wdp_id = info_by_wdppath.get(path, {}).get('wdp_id', '')
    img_dict = {'id': wdp_id}
    # for variation --image={'id': wdp_id}
    cmd_lst = append_flag.main(self, cmd_lst, 'image', img_dict)
    return cmd_lst
