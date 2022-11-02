from data.data import ProcessorData


def prod_isupdated_bool(self, pid):

    qstr = """
        UPDATE tblsklad
        SET is_updated = 'false'
        WHERE pid IN ('%s');""" % (pid)

    try:
        self.cnx.q_db('tab', qstr)
    except Exception as e:
        self.log.error(f"utils.change_is_updated failed {e}")

    return

def img_isupdated_bools(self, pid):
    """ changes image bools to false for all images, by pid."""
    pic_update_str = """
        UPDATE tblpic
        SET is_updated = 'false'
        WHERE productid IN ('%s');""" % (pid)
    pick_update_str = """
        UPDATE tblpic_komplex
        SET is_updated = 'false'
        WHERE pid IN ('%s');""" % (pid)

    try:
        self.cnx.q_db('tab', pic_update_str)
    except Exception as e:
        self.log.error(f"utils.esi_image_update failed {e}")

    try:
        self.cnx.q_db('tab', pick_update_str)
    except Exception as e:
        self.log.error(f"utils.esi_image_update failed {e}")

    return

def main(self, data: ProcessorData):
    self.log.info(f"Update syncbools ...")
    pid = data.tab_pid_group
    img_isupdated_bools(self, pid)
    prod_isupdated_bool(self, pid)
    self.log.info(f"Success, updated tab pid {pid}")
    return

