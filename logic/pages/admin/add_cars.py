from flask import request as rq, redirect, url_for, render_template

from database.setup_db.models.base_instance import db
from database.setup_db.models.cars_ml import Cars

class AddCars:
    def add_car(self):
        if rq.method == "POST":
            data = [
                "country",
                "brand",
                "model",
                "release_year",
                "color",
                "type_body",
                "transmission",
                "engine_volume",
                "engine_power",
                "mileage",
                "price",
                "image"
            ]
            
            get_data = {key: rq.form.get(key) for key in data}
            
            car = Cars(**get_data)
            db.session.add(car)
            db.session.commit()
            return redirect(url_for("add_cars"))
        
        return render_template("admin/add_cars.html")