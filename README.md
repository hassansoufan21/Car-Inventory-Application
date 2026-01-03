# Car-Inventory-Application
A mock-car inventory app created using Python, MySQL, and HTML. 
--------------------------------
Car Inventory Management System by Hassan Soufan
--------------------------------

A 3-tier application built with Flask (GUI), Python (Business Logic Layer & Data Access Layer),
and MySQL (Database), and HTML (Website UI) for managing a car dealership’s inventory, transactions, staff, and reports.

-------------------------------------------------
Project Structure
-------------------------------------------------
car_inventory_app/
    app.py              -> Flask GUI (View Layer)
    business_logic.py   -> Business Logic Layer (BLL)
    data_access.py      -> Data Access Layer (DAL)
    templates/          -> HTML Templates for Flask
        login.html
        dashboard.html
        add_car.html
        update_car.html
        delete_car.html
        transactions.html
        views.html
    car_inventory.sql   -> SQL schema, sample data, stored procedures, and views

-------------------------------------------------
Requirements
-------------------------------------------------
- Python 3.8 or higher
- MySQL Server
- Required Python packages:
    pip install flask mysql-connector-python

-------------------------------------------------
How to Run
-------------------------------------------------
1. Setup Database
   - Make sure that MySQL is running
   - Import SQL schema and sample data:
        mysql -u root -p < car_inventory.sql

2. Run Flask App
   Navigate to project folder:
        cd "X:\Database Principles\car_inventory_app"
        python app.py

   Flask will start at:
        http://127.0.0.1:5000/

-------------------------------------------------
Login Information
-------------------------------------------------
- Host: localhost
- Port: 3306
- User: your MySQL username (example: root)
- Password: your MySQL password (Use Persona2001!, if it doesn't log you in)
- Database is automatically set to: car_inventory

-------------------------------------------------
Features
-------------------------------------------------
- Login Screen (connect to DB before accessing system)
- Dashboard with navigation
- Add Car (insert into inventory)
- Update Car (change status: Available, Sold, Maintenance)
- Delete Car (cascade deletes transactions/maintenance)
- Transactions (view all via stored procedure)
- Reports (database views):
    * Total Sales by Staff (aggregated revenue)
    * Available Cars by Location

-------------------------------------------------
Testing Checklist
-------------------------------------------------
1. Login with MySQL credentials -> Dashboard loads
2. Add Car -> Reflected in DB and views
3. Update Car -> Status changes, views update
4. Delete Car -> Rows removed, cascades applied
5. Transactions -> All records visible
6. Reports -> Aggregated views display correctly
7. Low Stock -> Checks inventory and reports whether car is low in availability

P.S. To return to the previous screen, press the back button on your browser to return to the Dashboard.
