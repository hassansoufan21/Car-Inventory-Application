import mysql.connector


class Database:
    """
    Data Access Layer (DAL) for the Car Inventory system.
    Handles all database communication using stored procedures and views only.
    """

    def __init__(self, host="localhost", port=3306, user=None, password=None, database="car_inventory"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    # -------------------------------
    # Connection Management
    # -------------------------------
    def connect(self):
        """Open a connection to the MySQL database."""
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor(dictionary=True)  # results as dicts

    def close(self):
        """Close the DB connection safely."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    # -------------------------------
    # Generic Helpers
    # -------------------------------
    def call_proc(self, proc_name, args=()):
        """
        Call a stored procedure and return results (if any).
        """
        self.cursor.callproc(proc_name, args)
        results = []
        for r in self.cursor.stored_results():
            results.extend(r.fetchall())
        self.conn.commit()
        return results

    def get_view(self, view_name):
        """
        Query a predefined view.
        """
        self.cursor.execute(f"SELECT * FROM {view_name}")
        return self.cursor.fetchall()

    # -------------------------------
    # Stored Procedure Wrappers
    # -------------------------------
    def get_all_transactions(self):
        """Wrapper for GetAllTransactions() stored procedure."""
        return self.call_proc("GetAllTransactions")

    def add_car(self, make, model, year, vin, color, status, is_certified, location_id, price):
        """Wrapper for AddCar() stored procedure."""
        return self.call_proc(
            "AddCar",
            (make, model, year, vin, color, status, is_certified, location_id, price)
        )

    def update_car_status(self, car_id, new_status):
        """Wrapper for UpdateCarStatus() stored procedure."""
        return self.call_proc("UpdateCarStatus", (car_id, new_status))

    def delete_car(self, car_id):
        """Wrapper for DeleteCar() stored procedure."""
        return self.call_proc("DeleteCar", (car_id,))

    # -------------------------------
    # View Wrappers
    # -------------------------------
    def get_sales_by_staff(self):
        """Query total_sales_by_staff view."""
        return self.get_view("total_sales_by_staff")

    def get_available_cars_by_location(self):
        """Query available_cars_by_location view."""
        return self.get_view("available_cars_by_location")
    
    def get_low_stock(db):
        query = "SELECT * FROM low_stock;"
        return db.query(query)