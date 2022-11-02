def qstr_select_tab_images_by_pid(pids: str) -> str:
    """ Select all tabat images by pid."""
    return """
        SELECT *
        FROM images
        WHERE pid IN (%s)
        ORDER BY picpath ASC;""" % (pids)
