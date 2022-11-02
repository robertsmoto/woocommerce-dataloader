from . import append_flag


def main(self, cmd_lst: list, info_by_wdppath: dict, featured_image: dict) -> list:
    """Adds images flags to variable and simple products. Expects a
    list of dicts for images, will return
    --images='[{"id":"239"},{"id":"240"}]'"""

    img_list = []

    # this puts the featured image in the first position
    featured_path = featured_image.get('path', '')
    featured_id = info_by_wdppath.get(featured_path, {}).get('wdp_id', '')
    if featured_id:
        idict = {'id': featured_id}
        img_list.insert(0, idict)

    for path, info in info_by_wdppath.items():
        if path == featured_path:
            continue
        wdp_id = info.get('wdp_id', '')
        idict = {'id': wdp_id}
        img_list.append(idict)

    cmd_lst = append_flag.main(self, cmd_lst, "images", img_list)

    return cmd_lst
