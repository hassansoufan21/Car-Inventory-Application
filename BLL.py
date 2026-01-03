from DAL import Database


# ---------------------------
# Business Logic Layer (BLL)
# ---------------------------

def add_car(db: Database, make, model, year, vin, color, status, is_certified, location_id, price):
    """
    Add a new car to the inventory with validation.
    Uses stored procedure AddCar.
    """
    # --- Validation ---
    if not make or not model:
        raise ValueError("Make and model are required")
    if not isinstance(year, int) or year < 1886 or year > 2100:  # first car ~1886
        raise ValueError("Year must be a valid 4-digit number")
    if not vin or len(vin) != 17:
        raise ValueError("VIN must be exactly 17 characters")
    if price <= 0:
        raise ValueError("Price must be greater than 0")
    if status not in ("Available", "Sold", "Under Maintenance"):
        raise ValueError("Invalid status. Must be 'Available', 'Sold', or 'Under Maintenance'")
    if is_certified not in (0, 1, True, False):
        raise ValueError("is_certified must be 0/1 or True/False")

    # --- Business Rule Example: Prevent duplicate VINs ---
    existing_cars = db.get_view("cars") if "cars" in db.database else []
    for car in existing_cars:
        if car.get("vin") == vin:
            raise ValueError("A car with this VIN already exists in the database")

    # --- Call DAL ---
    return db.add_car(make, model, year, vin, color, status, int(is_certified), location_id, price)


def update_car_status(db: Database, car_id, new_status):
    """
    Update a car's status with validation.
    Uses stored procedure UpdateCarStatus.
    """
    if not isinstance(car_id, int) or car_id <= 0:
        raise ValueError("Car ID must be a positive integer")
    if new_status not in ("Available", "Sold", "Under Maintenance"):
        raise ValueError("Invalid status. Must be 'Available', 'Sold', or 'Under Maintenance'")

    return db.update_car_status(car_id, new_status)


def delete_car(db: Database, car_id):
    """
    Delete a car by ID.
    Uses stored procedure DeleteCar.
    Cascades to transactions and maintenance.
    """
    if not isinstance(car_id, int) or car_id <= 0:
        raise ValueError("Car ID must be a positive integer")

    return db.delete_car(car_id)


def get_all_transactions(db: Database):
    """
    Get all transactions.
    Uses stored procedure GetAllTransactions.
    """
    return db.get_all_transactions()


def get_sales_view(db: Database):
    """
    View: total sales by staff.
    """
    return db.get_sales_by_staff()


def get_available_cars_view(db: Database):
    """
    View: available cars by location.
    """
    return db.get_available_cars_by_location()

def get_low_stock(db):
    return db.call_view("Low_Stock")