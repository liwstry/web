from flask import render_template

from routes.routes_init import Routes

class AdminRoutes(Routes):
    def run_routes(self):
        @self.app.route("/admin")
        def admin():
            return self.admin.open_admin()
        
        @self.app.route("/admin/server")
        def server():
            return render_template("admin/server.html")
        
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