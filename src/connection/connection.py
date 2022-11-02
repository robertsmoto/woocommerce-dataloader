from config.config import Config
from dbutils.pooled_db import PooledDB
from log.log import Log
from sshtunnel import SSHTunnelForwarder
from typing import Tuple
import psycopg2
import psycopg2.extras
import pymysql
import subprocess


class Connect:
    """Starts the SSH server and dacliase thread pools.
    mysql connections are not threadsafe which means:
    Threads may not share connections. Each thread should
    create its own connection, but can share the module."""
    def __init__(self, conf: Config, log: Log):
        self.conf = conf
        self.WDPDB_USER = conf.conf.get('WDPDB_USER', '')
        self.WDPDB_PASS = conf.conf.get('WDPDB_PASS', '')
        self.WDPDB_HOST = conf.conf.get('WDPDB_HOST', '')
        self.WDPDB_DNAM = conf.conf.get('WDPDB_DNAM', '')
        self.DB_USER = conf.conf.get('DB_USER', '')
        self.DB_PASS = conf.conf.get('DB_PASS', '')
        self.DB_HOST = conf.conf.get('DB_HOST', '')
        self.DB_DNAM = conf.conf.get('DB_DNAM', '')
        self.DOSSH_IP = conf.conf.get('DOSSH_IP', '')
        self.DOSSH_PORT = int(conf.conf.get('DOSSH_PORT', ''))
        self.DOSSH_USER = conf.conf.get('DOSSH_USER', '')
        self.DOSSH_PKEY = conf.conf.get('DOSSH_PKEY', '')
        self.DOSSH_R_BIND_P = int(conf.conf.get('DOSSH_R_BIND_P', ''))
        self.SSH_IP = conf.conf.get('SSH_IP', '')
        self.SSH_PORT = int(conf.conf.get('SSH_PORT', ''))
        self.SSH_USER = conf.conf.get('SSH_USER', '')
        self.SSH_PKEY = conf.conf.get('SSH_PKEY', '')
        self.SSH_R_BIND_P = int(conf.conf.get('SSH_R_BIND_P', ''))
        self.conn = self.create_all_connections()
        self.log = log

    def _create_ssh_conn(self, cred: dict):
        try:
            ssh_server = SSHTunnelForwarder(
                (cred['ssh_host'], cred['ssh_port']),
                ssh_username=cred['ssh_user'],
                ssh_pkey=cred['ssh_pkey'],
                remote_bind_address=('localhost', cred['ssh_r_bind_p']),
                set_keepalive=1.5,
                threaded=True
            )
            ssh_server.start()
            bp = ssh_server.local_bind_port
        except Exception as e:
            print('ssh connection failed ...', e)
            ssh_server = None
            bp = 0
        return ssh_server, bp


    def _create_db_conn_pool(self, cred: dict, bp: int):
        conn_pool = PooledDB(
            creator=cred['db_module'],
            mincached=10,  # cached connections on creation
            maxcached=20,  # 0 is unlimited
            maxshared=20,  # 0 all connections are dedicated
            maxconnections=20,  # 0 unlimited reuse of a connection
            blocking=False,
            maxusage=None,
            setsession=[],
            ping=1,  # 1 is default, 7 ping always
            reset=True,  # rollback failed transactions
            host=cred['db_host'],
            port=bp,
            user=cred['db_user'],
            password=cred['db_pass'],
            dacliase=cred['db_dnam'],
            # charset='utf8'
        )
        return conn_pool

    def _get_credentials(self, serv: str):
        cred = {}
        cred['db_user'] = (
            self.WDPDB_USER if serv == "wdp" else self.DB_USER)
        cred['db_pass'] = (
            self.WDPDB_PASS if serv == "wdp" else self.DB_PASS)
        cred['db_host'] = (
            self.WDPDB_HOST if serv == "wdp" else self.DB_HOST)
        cred['db_dnam'] = (
            self.WDPDB_DNAM if serv == "wdp" else self.DB_DNAM)
        cred['db_module'] = pymysql if serv == "wdp" else psycopg2
        cred['ssh_host'] = (
            self.DOSSH_IP if serv == "wdp" else self.SSH_IP)
        cred['ssh_port'] = (
            self.DOSSH_PORT if serv == "wdp" else self.SSH_PORT)
        cred['ssh_user'] = (
            self.DOSSH_USER if serv == "wdp" else self.SSH_USER)
        cred['ssh_pkey'] = (
            self.DOSSH_PKEY if serv == "wdp" else self.SSH_PKEY)
        cred['ssh_r_bind_p'] = (
            self.DOSSH_R_BIND_P if serv == "wdp" else self.SSH_R_BIND_P)
        return cred

    def create_all_connections(self):
        conn = {}
        # make wdp connection
        wdp_cred = self._get_credentials(serv="wdp")
        conn['wdp_bp'] = 3306
        if self.conf.conf['wdpLoc'] == "remote":
            conn['wdp_ssh'], conn['wdp_bp'] = self._create_ssh_conn(cred=wdp_cred)
        conn['wdp_pool'] = self._create_db_conn_pool(cred=wdp_cred, bp=conn['wdp_bp'])
        # make cli connection
        cli_cred = self._get_credentials(serv="cli")
        conn['cli_bp'] = 5432
        if self.conf.conf['cliLoc'] == "remote":
            conn['cli_ssh'], conn['cli_bp'] = self._create_ssh_conn(cred=cli_cred)
        conn['cli_pool'] = self._create_db_conn_pool(cred=cli_cred, bp=conn['cli_bp'])
        return conn


    def _mysql_db(self, qstr: str):
        n_records = 0
        records = []
        dbconn = self.conn['wdp_pool'].connection()
        select = qstr.find("SELECT")
        cur = dbconn.cursor(pymysql.cursors.DictCursor)
        cur.execute(qstr)
        dbconn.commit()

        if select == 0:
            records = cur.fetchall()
            n_records = cur.rowcount

        dbconn.close()  # returns connection to the pool
        return n_records, records

    def _psql_db(self, qstr: str):
        n_records = 0
        records = []
        dbconn = self.conn['cli_pool'].connection()
        select = qstr.find("SELECT")
        cur = dbconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(qstr)
        dbconn.commit()

        if select == 0:
            n_records = cur.rowcount
            records = cur.fetchall()

        dbconn.close()  # returns connection to the pool
        return n_records, records

    def str_from_list(self, data_list: list, quoted: str):
        """ Takes a list of items and returns a comma-delimited data_string
        of items. The resulting string may contain unquoted or quoted elements
        "a, b, c" or "'a', 'b', 'c'" using quoted='no' or quoted='yes'"""

        data_string = ", ".join(f"'{d}'" for d in data_list)
        if quoted == 'no':
            data_string = ", ".join(f"{d}" for d in data_list)

        return data_string

    def q_db(self, serv: str, qstr: str) -> Tuple[int, list]:
        n_records = 0
        records = []

        qstr = qstr.replace('\n', ' ').replace('    ', '').strip()

        if serv == "wdp":
            n_records, records = self._mysql_db(qstr=qstr)
        if serv == "cli":
            n_records, records = self._psql_db(qstr=qstr)

        return n_records, records


    def __make_subprocess_command(self, serv: str, cmd: list) -> list:
        if 'scp' in cmd:
            return cmd
        cli_loc = self.conf.conf.get('cliLoc', '')
        wdp_loc = self.conf.conf.get('wdpLoc', '')
        ssh_index = {
                'cli': f"{self.conf.conf.get('SSH_USER', '')}@{self.conf.conf.get('SSH_IP', '')}",
                'wdp': f"{self.conf.conf.get('DOSSH_USER', '')}@{self.conf.conf.get('DOSSH_IP', '')}",
                }
        ssh_needed_conditions = [
                (serv == 'cli' and cli_loc == 'remote') or
                (serv == 'wdp' and wdp_loc == 'remote'),
                'scp' not in cmd,
                ]
        self.log.debug(f"subprocess cmd {cmd}")
        if all(ssh_needed_conditions):
            cmd.insert(0, ssh_index[serv])
            cmd.insert(0, 'ssh')
        return cmd

    def subprocess(self, serv: str, cmd: list) -> Tuple[str, str]:
        """The skip_replace attr will turn off the [] "[]" replacement for
        lists."""

        TO = 30

        if not cmd:
            out = ""
            err_msg = ""
            return out, err_msg

        # determines if ssh is needed, and modifies command
        cmd = self.__make_subprocess_command(serv, cmd)
        cmd = [str(x) for x in cmd if x]

        # if wdp is local, invoke the shell
        cwd = None
        if self.conf.conf.get('wdpLoc', 'remote') == 'local':
            cwd = '/usr/bin'

        # subpr = subprocess.run(cmd, capture_output=True, timeout=TO)
        subpr = subprocess.run(cmd, capture_output=True, timeout=TO, cwd=cwd)

        stdout = subpr.stdout.decode('utf-8').strip()
        stderr = subpr.stderr.decode('utf-8').strip()

        self.log.debug("###########################")
        self.log.debug(f"## stdout: {stdout}")
        self.log.debug(f"## stderr: {stderr}")
        self.log.debug(f"## cmd: {cmd}")

        return stdout, stderr
