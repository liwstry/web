import logging as log
from pathlib import Path
from datetime import datetime, timezone, timedelta

class LoggerSetup():
    @staticmethod
    def get_current_folder():
        file_path = Path(__file__)
        return file_path.parent.name
    
    @staticmethod
    def get_msc_time():
        utc_time = datetime.now(timezone.utc)
        msc_time = utc_time + timedelta(hours=3)
        return msc_time.strftime("%Y-%m-%d %H:%M:%S")
    
    def setup_log(self, filename=f"logs/{get_current_folder()}.log", level=log.INFO):
        logger = log.getLogger()
        logger.setLevel(level)
        logger.handlers.clear()
        
        formatter = log.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt=self.get_msc_time())
        
        file_handler = log.FileHandler(filename)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        return logger

logger = LoggerSetup()

log_info = logger.setup_log()
log_error = logger.setup_log(level=log.ERROR)
log_debug = logger.setup_log(level=log.DEBUG)

log_error.error("Error log")
log_info.info("Info log")
log_debug.debug("Debug log")