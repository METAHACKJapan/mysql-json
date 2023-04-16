from tests.util import BTC

class Test_MySQL_Connection(BTC):
    """Sample test class."""
    def test_connection(self):
        """Checks connectivity between test module and MySQL database."""
        cur = self.get_cursor()
        cur.execute("SELECT DATABASE() AS `db`;")
        assert self.dsn['database'] == cur.fetchone()['db']
