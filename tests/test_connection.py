import pymysql
from tests.util import BTC

class Test_MySQL_Connection(BTC):
    """Sample test class."""
    DSN_PATH: str = "dsn.json"

    def test_connection(self):
        """Checks connectivity between test module and MySQL database."""
        con: pymysql.Connection = pymysql.connect(**self.dsn)
        cur: pymysql.cursors.DictCursor = con.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT DATABASE() AS `db`;")
        con.close()
        assert self.dsn['database'] == cur.fetchone()['db']
