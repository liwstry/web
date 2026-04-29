import psutil as ps

class Server:
    def __init__(self):
        self.server = {
        "cpu": 0,
        "ram": 0,
        "disk_percent": 0,
        "disk_used": 0,
        "disk_total": 0,
        "time_work": 0,
        "bytes_sent": 0,
        "bytes_recv": 0
    }

    def server_update_info(self):
        self.server["cpu"] = ps.cpu_percent(interval=1)
        self.server["ram"] = ps.virtual_memory().percent
        self.server["disk_percent"] = ps.disk_usage("C:/").percent
        self.server["disk_used"] =round(ps.disk_usage("C:/").used / (1024 ** 3), 2)
        self.server["disk_total"] = round(ps.disk_usage("C:/").total / (1024 ** 3), 2)
        self.server["time_work"] = round((ps.cpu_times().user / 60) / 60, 2)
        self.server["bytes_sent"] = ps.net_io_counters().bytes_sent
        self.server["bytes_recv"] = ps.net_io_counters().bytes_recv
    
    def get_server_info(self):
        return self.server