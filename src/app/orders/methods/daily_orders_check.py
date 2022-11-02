def daily_orders_check(self):
    """Daily order check routines."""
    sync_orders_tables(self, tables=ALL_TABLES, tablekeys=TABLE_KEYS)
    return
