from flask_socketio import SocketIO as _SocketIO

from threading import Thread
import time

from logic.pages.admin.server.server import Server

class ServerSocket:
    def __init__(self, socketio: _SocketIO):
        self.socketio = socketio
        self.server = Server()
    
    def run_server_socket(self):
        
        @self.socketio.on("get_server_stats")
        def server_stats():
            self.socketio.emit("server_update", self.server.get_server_info())
    
    def _server_update(self):
        while True:
            self.server.server_update_info()
            self.socketio.emit("server_update", self.server.get_server_info())
            time.sleep(0.4)
    
    def run(self):
        self.run_server_socket()
        self.socketio.start_background_task(self._server_update)