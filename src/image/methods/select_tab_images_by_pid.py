from typing import Tuple
from .. qstrs.qstrs import qstr_select_tab_images_by_pid

def main(self, pid: str) -> Tuple[list, str]:
    err = ''
    qstr = qstr_select_tab_images_by_pid(pid)
    _, records = self.cnx.q_db(serv='cli', qstr=qstr)
    return records, err
