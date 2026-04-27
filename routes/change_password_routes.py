from routes.routes_init import Routes

class ChangePasswordRoutes(Routes):
    def run_routes(self):
        @self.app.route("/change-password", methods=["post"])
        def change_password_link():
            return self.change_password.gen_url_token()
        
        @self.app.route("/change-password/<token>", methods=["get", "post"])
        def change_password(token):
            return self.change_password.change_password(token)