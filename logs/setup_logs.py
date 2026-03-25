import logging as log
from pathlib import Path
from datetime import datetime, timezone, timedelta

class LogSetup():
    def __init__(self, module_name):
        """
        Args:
            module_name: __file__
        """
        self.module_name = module_name
        
        self._type_log = None
        
    def log(self, type_log, msg):
        msg = f"[{Path(self.module_name).resolve().relative_to(Path.cwd())}] - {msg}"
        
        if type_log == "info":
            self._type_log = "INFO"
            self._setup_log(log.INFO).info(msg)
        
        elif type_log == "error":
            self._type_log = "ERROR"
            self._setup_log(log.ERROR).error(msg)
        
        elif type_log == "debug":
            self._type_log = "DEBUG"
            self._setup_log(log.DEBUG).debug(msg)
        
        elif type_log == "critical":
            self._type_log = "CRITICAL"
            self._setup_log(log.CRITICAL).critical(msg)
    
    @staticmethod
    def get_msc_time():
        utc_time = datetime.now(timezone.utc)
        msc_time = utc_time + timedelta(hours=3)
        return msc_time.strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_current_folder(self):
        return Path(self.module_name).parent.name
    
    def _setup_log(self, level):
        logger = log.getLogger(self._get_current_folder())
        logger.setLevel(level)
        logger.handlers.clear()
        
        foldername = f"logs/{self._get_current_folder()}-logs"
        folder = Path(foldername)
        folder.mkdir(parents=True, exist_ok=True)
        
        filename = f"{foldername}/{self._type_log}.log"
        general_file = "logs/GENERAL.log"
        
        file_handler = log.FileHandler(filename, encoding="utf-8")
        general_file_handler = log.FileHandler(general_file, encoding="utf-8")
        
        formatter = log.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt=self.get_msc_time())
        
        file_handler.setFormatter(formatter)
        general_file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(general_file_handler)
        return logger