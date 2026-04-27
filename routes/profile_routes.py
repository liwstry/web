from flask import request as rq

from routes.routes_init import Routes

class ProfileRoutes(Routes):
    def run_routes(self):
        @self.app.route("/profile", methods=["get", "post"])
        def profile():
            if rq.method == "POST":
                return self.profile_handler.edit_profile()
            return self.profile_handler.get_data()