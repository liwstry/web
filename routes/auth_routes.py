from flask import request as rq, render_template

from routes.routes_init import Routes

class AuthRoutes(Routes):
    def run_routes(self):
        @self.app.route("/signin", methods=["get", "post"])
        def signin():
            if rq.method == "POST":
                return self.auth.signin()
            return render_template("signin.html")
        
        @self.app.route("/signup", methods=["get", "post"])
        def signup():
            if rq.method == "POST":
                return self.auth.signup()
            return render_template("signup.html")