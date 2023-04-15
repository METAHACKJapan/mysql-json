import os
from typing import Any, Dict, Optional, List
import json
import subprocess
import pymysql

class BTC(object):
    __dsn__: Optional[Dict[str, Any]] = None
    __con__: Optional[pymysql.Connection] = None
    DSN_PATH: Optional[str] = "dsn.json"
    @classmethod
    @property
    def dsn_path(cls)-> str:
        return cls.DSN_PATH

    @classmethod
    def __load_dsn__(cls, path: str = None)-> None:
        cls.__dsn__ = json.load(open(path or cls.DSN_PATH, "r", encoding = "utf8"))

    @classmethod
    def set_dsn(cls, path: str)-> None:
        cls.DSN_PATH = path
        cls.__load_dsn__()
    
    @property
    def dsn(self)-> Dict[str, Any]:
        if not self.__dsn__:
            self.__load_dsn__()
        return self.__dsn__
 
    @property
    def dbcon(self)-> pymysql.Connection:
        if not self.__con__:
            self.__con__ = pymysql.connect(**self.dsn)
        return self.__con__
    
    def get_cursor(self)-> pymysql.cursors.DictCursor:
        return self.dbcon.cursor(pymysql.cursors.DictCursor)

def execute_sql_file(path: str)-> str:
    dsn: Dict[str, Any] = json.load(open(BTC.dsn_path, "r", encoding = "utf8"))
    args: str = f"mysql -h{dsn['host']} -P{dsn['port']} -u{dsn['user']} -p{dsn['password']} {dsn['database']} < {path}"
    subprocess.call(args = args, shell = True)
    return args
