# TODO: Сделать отдельный класс редису

import json
import subprocess as sp
import socket
from redis import Redis
from pathlib import Path

from logs.setup_logs import LogSetup

log = LogSetup(__file__)

class Cache:
    def __init__(self):
        self.redis = Redis(host="127.0.0.1", port=6379)
        self.run_server_redis()
    
    def run_server_redis(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            conn = sock.connect_ex(("127.0.0.1", 6379))
            if not conn == 0:
                sp.Popen(["start", "cmd", "/k", "cache\\redis.cmd"], shell=True)
                log.log("error", "Redis запущен")
        except Exception as e:
            sock.close
            log.log("error", f"Ошибка при проверке состояния или запуска Redis: {str(e)}")
    
    @staticmethod
    def check_path_redis():
        if not Path("C:/Redis").is_dir():
            log.log("error", "Не найден путь к Redis по пути: C:/Redis")
            return False
        return True
    
    @staticmethod
    def key_format(user, *keys):
        return f"{user}:{":".join(str(i) for i in keys)}"
    
    def add_cache(self, user, *keys, data):
        try:
            time=360
            self.redis.setex(self.key_format(user, *keys), time, json.dumps(data))
        except Exception as e:
            log.log("error", f"Ошибка при записи в кэш: {str(e)}")
            print(f"Ошибка при записи в кэш: {str(e)}")
    
    def get_cache(self, user, *keys):
        try:
            return json.loads(self.redis.get(self.key_format(user, *keys)))
        except Exception as e:
            log.log("error", f"Ошибка при чтении из кэша: {str(e)}")
            print(f"Ошибка при чтении из кэша: {str(e)}")
    
    def del_cache(self, user, *keys):
        try:
            self.redis.delete(self.key_format(user, *keys))
        except Exception as e:
            log.log("error", f"Ошибка при удалении из кэша: {str(e)}")
            print(f"Ошибка при удалении из кэша: {str(e)}")



class CacheConst:
    def __init__(self):
        self.filename = "cache/const_cache.json"
        self.cache = {}

    def get_cache(self, key):
        return self.cache.get(key)
    
    def add_cache(self, key, value):
        self.cache[key] = value
    
    def save_cache(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.cache, file, indent=4, ensure_ascii=False)
        except Exception as e:
            log.log("error", f"Ошибка при записи кэша в {self.filename}: {str(e)}")
    
    def load_cache(self):
        if Path(self.filename).is_file():
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.cache = json.load(file)
            except Exception as e:
                log.log("error", f"Ошибка при чтении кэша из {self.filename}: {str(e)}")