from flask import render_template
from flask_login import current_user

from routes.routes_init import Routes

class AdminRoutes(Routes):
    def run_routes(self):
        @self.app.route("/admin")
        def admin():
            return self.admin.open_admin()
        
        @self.app.route("/admin/server")
        def server():
            if current_user.is_authenticated and current_user.is_admin:
                return render_template("admin/server.html")
            return render_template("errors/404.html")
        
        @self.app.route("/admin/users")
        def admin_users():
            return self.admin.open_users_panel()
        
        @self.app.route("/admin/users/admin-add", methods=["POST"])
        def admin_add():
            return self.admin.create_admin()
        
        @self.app.route("/admin/users/admin-remove", methods=["post"])
        def admin_remove():
            return self.admin.del_admin()
        
        @self.app.route("/admin/users/admin-switch", methods=["post"])
        def admin_switch():
            return self.admin.switch_admin()
        
        @self.app.route("/admin/users/user-remove", methods=["post"])
        def user_remove():
            return self.admin.del_user()
        
        @self.app.route("/admin/add_cars", methods=["get", "post"])
        def add_cars():
            return self.add_car.add_car()