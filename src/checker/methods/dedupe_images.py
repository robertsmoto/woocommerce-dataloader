def delete_detail(conn: dict, ids: str) -> None:
    """Deletes the duplicated record."""

    qstr = """
        DELETE FROM wp_as3cf_items
        WHERE id IN (%s);""" % (ids)

    _, _ = connections.q_db(conn=conn, serv='wdp', qstr=qstr)

    # print('deleted ids: ', ids)
    return


def check_each_duplicate(conn: dict, records: list) -> None:
    """Processes each record in dupicate query."""

    detail_ids = set()

    for record in records:
        pocet = record['cnt'] - 1
        qstr = """
            SELECT id
            FROM wp_as3cf_items
            WHERE original_path LIKE '%%%s%%'
            ORDER BY id ASC LIMIT %s;""" % (record['col'], pocet)

        _, details = connections.q_db(conn=conn, serv='wdp', qstr=qstr)

        for detail in details:
            detail_ids.add(detail['id'])

    detail_ids_str = ", ".join("'%s'" % d for d in detail_ids)
    delete_detail(conn=conn, ids=detail_ids_str)

    return


def get_duplicates(conn: dict) -> list:
    """Retrieve potential duplicates."""

    qstr = """
        SELECT col,cnt
        FROM temp_duplicate_count
        LIMIT 17000"""

    _, records = connections.q_db(conn=conn, serv='wdp', qstr=qstr)

    return records

def main(self) -> None:
    """Runs BJ's utils to dedupe images."""

    if not self.conf.conf.get('dedupImages', False):
        return self
    self.log.info("Deduping images ...")

    records = get_duplicates(self)
    check_each_duplicate(self, records=records)
    return self
