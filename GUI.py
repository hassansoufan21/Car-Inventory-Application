from flask import Flask, render_template, request, redirect, url_for, session, flash
from DAL import Database
import BLL as bl

app = Flask(__name__)
app.secret_key = "supersecret"   # required for session storage

# -------------------------------
# Helper: Get DB object from session
# -------------------------------
def get_db():
    db_info = session.get("db_info")
    if not db_info:
        raise RuntimeError("Not logged in")
    db = Database(**db_info)
    db.connect()
    return db


# -------------------------------
# Routes
# -------------------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            session["db_info"] = {
                "host": request.form["host"] or "localhost",
                "port": int(request.form["port"] or 3306),
                "user": request.form["user"],
                "password": request.form["password"],
                "database": "car_inventory"
            }

            db = get_db()
            db.close()
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Login failed: {e}", "danger")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -------------------------------
# CRUD: Add Car
# -------------------------------
@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        try:
            db = get_db()
            bl.add_car(
                db,
                request.form["make"],
                request.form["model"],
                int(request.form["year"]),
                request.form["vin"],
                request.form["color"],
                request.form["status"],
                int(request.form.get("is_certified", 0)),
                int(request.form["location_id"]),
                float(request.form["price"])
            )
            db.close()
            flash("Car added successfully!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Error adding car: {e}", "danger")

    return render_template("add_car.html")


# -------------------------------
# CRUD: Update Car Status
# -------------------------------
@app.route("/update_car", methods=["GET", "POST"])
def update_car():
    if request.method == "POST":
        try:
            db = get_db()
            bl.update_car_status(db, int(request.form["car_id"]), request.form["status"])
            db.close()
            flash("Car status updated!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Error updating car: {e}", "danger")

    return render_template("update_car.html")


# -------------------------------
# CRUD: Delete Car
# -------------------------------
@app.route("/delete_car", methods=["GET", "POST"])
def delete_car():
    if request.method == "POST":
        try:
            db = get_db()
            bl.delete_car(db, int(request.form["car_id"]))
            db.close()
            flash("Car deleted!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Error deleting car: {e}", "danger")

    return render_template("delete_car.html")


# -------------------------------
# View Transactions
# -------------------------------
@app.route("/transactions")
def transactions():
    try:
        db = get_db()
        rows = bl.get_all_transactions(db)
        db.close()
        return render_template("transactions.html", rows=rows)
    except Exception as e:
        flash(f"Error loading transactions: {e}", "danger")
        return redirect(url_for("dashboard"))


# -------------------------------
# View Reports (Views from DB)
# -------------------------------
@app.route("/views")
def views():
    try:
        db = get_db()
        sales = bl.get_sales_view(db)
        cars = bl.get_available_cars_view(db)
        db.close()
        return render_template("views.html", sales=sales, cars=cars)
    except Exception as e:
        flash(f"Error loading views: {e}", "danger")
        return redirect(url_for("dashboard"))


# -------------------------------
# Run Flask
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)