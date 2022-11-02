def main(self) -> None:
    """Reports current config and the number of records to be processed."""

    update_count = """
    SELECT count(*)
    FROM products
    WHERE is_updated = true and img_updated_true = 0;
    """
    with_images_count = """
    SELECT count(*)
    FROM products
    WHERE is_updated = true and img_updated_true = 1;
    """
    updated_count = """
    SELECT count(*)
    FROM products
    WHERE is_updated = false;
    """
    _, update_r = self.d.cnx.q_db(serv='tab', qstr=update_count)
    _, with_image_r = self.d.cnx.q_db(serv='tab', qstr=with_images_count)
    _, updated_r = self.d.cnx.q_db(serv='tab', qstr=updated_count)

    status_str = f"""Currently in the TABAT database:
        {update_r[0]['count']} products to be updated (w/o images),
        {with_image_r[0]['count']} products to be updated (w/ images),
        {updated_r[0]['count']} total products up-to-date"""

    self.d.log.info(f"{status_str}")
    return self
