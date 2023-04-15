from typing import Any, Dict, Optional
import json

class BTC(object):
    __dsn__: Optional[Dict[str, Any]] = None
    DSN_PATH: Optional[str] = None
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
 
