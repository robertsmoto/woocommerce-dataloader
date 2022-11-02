SETTINGS = {
    # common
    'debugOutput': False,  # normal=False
    'useThreads': True,  # normal=True
    'numberThreads': 10,  # normal=10

    # server locations
    'wdpLoc': 'remote',  # wordpress 'local' or 'remote'
    'wdpDbt': 'mysql',  # type of database
    'cliLoc': 'remote',  # client 'local' or 'remote'
    'cliDbt': 'psql',  # type of database

    # dirs
    'logDirFile': '/dir/to/wcdataloader.log',
    'cliImgDir': '/share/images',
    'wdpImgDir': '/home/user/uploads/staging',
    'csvFileDir': '/dir/to/csv_files',

    # processers
    'deleteCalcMeta': False,  # normal = False

    # other
    'other1': 100,  # normal = 1
    'other2': 'value',  # normal = 'value'
    'other3': True,  # normal = True
}
