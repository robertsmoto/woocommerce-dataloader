import re


def main(self, tables: dict, tablekeys: dict):
    """This function takes the tables supplied and checks that all
    records in wdp exist in tab."""

    for table, columns in tables.items():

        key = tablekeys[table]

        # columns is already a list
        columns_str = self.cnx.str_from_list(columns, 'no')

        # get all records from tab
        qstr_key = """
        SELECT %s
        FROM %s """ % (key, table)

        n_keys, keys = self.cnx.q_db("tab", qstr_key)
        key_list = [k[key] for k in keys]
        key_str = self.cnx.str_from_list(key_list, 'no')

        # find records in wdp that are not in tab
        # check for 'wp_postmeta' exception
        add_str_01 = ""
        add_str_02 = ""
        if table == 'wp_postmeta':
            add_str_01 = "WHERE meta_key = 'wc_sf_regular_invoice_number'"
            add_str_02 = "AND meta_key = 'wc_sf_regular_invoice_number'"

        qstr = """
        SELECT %s
        FROM %s %s""" % (columns_str, table, add_str_01)

        if n_keys > 0:
            qstr = """
            SELECT %s
            FROM %s
            WHERE %s NOT IN (%s) %s""" % (
                    columns_str, table, key, key_str, add_str_02)

        _, records = self.cnx.q_db("wdp", qstr)

        # create the values string
        values_str = ""
        for record in records:
            values_list = [v for _, v in record.items()]
            values_str = self.cnx.str_from_list(values_list, 'yes')
            values_str = re.sub(r"'None'", 'NULL', values_str)

            qstr = """
            INSERT INTO %s (%s)
            VALUES (%s) """ % (table, columns_str, values_str)

            _, _ = self.cnx.q_db("tab", qstr)

    return

