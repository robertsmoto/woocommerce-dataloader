def main(self, table, ALL_TABLES: dict):
    """ Selects all orders in wdp and returns all orders in tab where
    wdp.status != tab.status """

    columns = ALL_TABLES[table]
    columns_str = self.cnx.str_from_list(columns, 'no')

    qstr = """
    SELECT %s
    FROM %s """ % (columns_str, table)

    _, wdp_ords = self.cnx.q_db("wdp", qstr)
    wdp_id_status = [(x['order_id'], x['status']) for x in wdp_ords]

    _, tab_ords = self.cnx.q_db("tab", qstr)
    tab_id_status = [(x['order_id'], x['status']) for x in tab_ords]

    update_list = []
    for woid, wstatus in wdp_id_status:
        if not any(
                woid == toid and wstatus == tstatus
                for (toid, tstatus) in tab_id_status):
            update_list.append((woid, wstatus))

    n_updates = len(update_list)

    return n_updates, update_list

