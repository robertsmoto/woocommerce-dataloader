import logging
import sys
from typing import Tuple


"""The clean images program attempts to find old images (of the same name)
that were previously associated with a product and delete them. To use the
program, delete the records in wordpress.aaa_cleaners and then run this
page python images_clean.py. There are record limits and a bool that needs to
be set to True in the config_env.py settings.

Because of the boundaries given, this is a pretty safe delete pattern and
shouldn't interfere with plugins or other functionality that uses
wp_posts attachments.

This is not a complete image cleaner, and only handles orphaned images from
existing products."""


def select_candidates(self) -> Tuple[list, str]:
    """Finds candidates to be image cleaned."""

    # fist find all ID's already cleaned
    qstr = """
    SELECT post_id
    FROM aaa_cleaners;"""

    n_clean_ids, clean_ids = self.cnx.q_db(qstr=qstr, serv="wdp")

    print("types number and results", type(n_clean_ids), type(clean_ids))

    clean_ids_list = [x['post_id'] for x in clean_ids]
    clean_ids_str = str_from_list(data_list=clean_ids_list, quoted='no')

    # find all unclean candidates
    qstr = """
    SELECT ID
    FROM wp_posts
    WHERE post_type = 'product'
    LIMIT %s """ % (STGS['cleanImagesLimit'])

    if n_clean_ids > 0:
        qstr = """
        SELECT ID
        FROM wp_posts
        WHERE post_type = 'product'
        AND ID NOT IN (%s)
        LIMIT %s """ % (clean_ids_str, STGS['cleanImagesLimit'])

    _, cands = self.cnx.q_db(qstr=qstr, serv="wdp")

    cands_list = [x['ID'] for x in cands]
    cands_str = str_from_list(data_list=cands_list, quoted='no')
    return cands_list, cands_str


def find_images_in_use(self, candidates: str) -> Tuple[list, str]:
    """Finds all images currentl in use by candidates."""

    qstr = """
    SELECT meta_value
    FROM wp_postmeta
    WHERE post_id IN (%s)
    AND (meta_key = '_thumbnail_id' OR meta_key = '_product_image_gallery')
    """ % (candidates)
    n_imgids, imgids = self.cnx.q_db(qstr=qstr, serv="wdp")

    imgids_list = []
    imgids_str = ""
    if n_imgids > 0:
        for x in imgids:
            new_list = x['meta_value'].split(",")
            imgids_list = imgids_list + new_list
        imgids_str = str_from_list(data_list=imgids_list, quoted='no')

    return imgids_list, imgids_str


def find_img_post_titles(self, image_ids: str) -> Tuple[list, str]:
    """Makes a list of image post_titles."""

    qstr = """
    SELECT post_title
    FROM wp_posts WHERE ID IN (%s) """ % (image_ids)
    n_ptitles, ptitles = self.cnx.q_db(conn=conn, qstr=qstr, serv="wdp")

    ptitles_list = []
    ptitles_str = ""
    if n_ptitles > 0:
        ptitles_list = [x['post_title'] for x in ptitles]
        ptitles_str = str_from_list(data_list=ptitles_list, quoted='yes')

    return ptitles_list, ptitles_str


def delete_unused_images(self, post_titles: str, image_ids: str) -> None:
    """Finds all unused images."""
    qstr = """
    DELETE
    FROM wp_posts
    WHERE post_title IN (%s)
    AND post_type = 'attachment'
    AND post_mime_type = 'image/jpeg'
    AND ID NOT IN (%s) """ % (post_titles, image_ids)
    _, _ = self.cnx.q_db(conn=conn, qstr=qstr, serv="wdp")
    return


def insert_records(self, post_ids: list):
    """Records the transaction to aaa_cleaners."""

    post_ids_str = ",".join("(%s)" % (x) for x in post_ids)

    qstr = """
    INSERT INTO aaa_cleaners (post_id)
    VALUES %s """ % (post_ids_str)
    _, _ = self.cnx.q_db(conn=conn, qstr=qstr, serv="wdp")
    return


def get_skus_by_id(self, post_ids: str) -> Tuple[list, str]:
    """Outputs the product skus involved."""

    qstr = """
    SELECT sku
    FROM wp_wc_product_meta_lookup
    WHERE product_id IN (%s) """ % (post_ids)

    n_skus, skus = self.cnx.q_db(conn=conn, qstr=qstr, serv="wdp")

    skus_list = []
    skus_str = ""
    if n_skus > 0:
        skus_list = [x['sku'] for x in skus]
        skus_str = str_from_list(data_list=skus_list, quoted='no')

    return skus_list, skus_str


def main(self):
    """Main program to clean unused images from wp_posts / wc_products."""

    if not self.conf.stgs.get('cleanUnusedImages', False):
        return self

    print("Looking for unused images to clean ...")
    logging.info("Looking for unused images to clean ...")

    """
    # Checks for duplicate, unused product images and deletes them.
    if conf.stgs['cleanUnusedImages']:
        log.info("Cleaning duplicate, unused prod images ...")
        app.image_cleaner()
    """

    # select the candidates
    cands_list, cands_str = select_candidates(conn=conn)

    # return if there aren't any candidates
    if len(cands_list) < 1:
        return self

    print(f"Looking for unused images associated with ids: {cands_str}")
    logging.info("Looking for unused images assoc with ids: %s", cands_str)

    # find images currently in use
    imgids_list, imgids_str = find_images_in_use(
            conn=conn, candidates=cands_str)

    # return if there aren't any images in use
    if len(imgids_list) < 1:
        return

    # get the titles of the images in use
    post_titles_list, post_titles_str = find_img_post_titles(
            conn=conn, image_ids=imgids_str)

    # delete all unused images related to these products
    delete_unused_images(
            conn=conn, post_titles=post_titles_str, image_ids=imgids_str)

    # record the ids insert into aaa_cleaners
    insert_records(conn=conn, post_ids=cands_list)

    # output information to the log
    skus_list, skus_str = get_skus_by_id(conn=conn, post_ids=cands_str)

    print(f"Ceaned unused images for these skus: {skus_str}")
    logging.info("Ceaned unused images for these skus: %s", skus_str)

    return self


if __name__ == "__main__":

    if config_env.clean_unused_images:
        # make the connections
        conn = connections.create_all_connections()
        print("conn type", type(conn))
        # run the main program
        main_images_cleaner(conn=conn)

        # close the connections
        if config_env.tab_loc == "remote":
            conn['tab_ssh'].stop()

        if config_env.wdp_loc == "remote":
            conn['wdp_ssh'].stop()

        sys.exit("Finished cleaning unused images ...")
