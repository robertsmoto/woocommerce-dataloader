def main(self) -> None:
    """Main program for finding products without images."""

    if not self.conf.conf.get('findProductsWoImages', False):
        return self
    utils_log.TogLog().info("Checking products w/o images ...")

    # find candidates
    _, candidates = find_noimages_candidates(conn=conn)

    utils_log.TogLog().info(
            f"WDP Products w/o images: {len(candidates)}")

    limit = 100
    for cand in candidates:
        # changed this to simply delete the product
        # rather than setting 'is_updated=True'

        if limit < 1:
            break

        cmd_lst = [
                'wp', 'wc', 'product', 'delete', f'{cand["ID"]}'
                ]

        cmd_lst = flags_utils.finish_flags(
                cmd_list=cmd_lst,
                cred=True,
                porcelain=True,
                force=True)

        _, err = utils_subprocess.run(serv="wdp", cmd=cmd_lst)

        utils_log.TogLog().info(
                f"Delete product w/o images, wc post ID: {cand['ID']}")

        limit -= 1

    return

