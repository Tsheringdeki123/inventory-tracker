========================================================================
INVENTORY MANAGEMENT SYSTEM WITH TKINTER & SQLITE
Jigme Namgyel Engineering College - Royal University of Bhutan
========================================================================

1. APPLICATION OVERVIEW
-----------------------
This project is a custom desktop GUI application built in Python using Tkinter 
and SQLite. It allows users to track inventory items, view stock analytics, 
and perform complete CRUD operations.

2. FEATURES IMPLEMENTED
-----------------------
- User Authentication: Secure login modal (Default: admin / admin123).
- SQLite Integration: Relational table storing product data and user credentials.
- Full CRUD Operations:
    * Create: Add new products with validation checks.
    * Read: View products in a Treeview table or open detailed summary modals.
    * Update: Edit existing inventory items.
    * Delete: Remove records with confirmation popups.
- Real-time Search: Filter inventory items dynamically by name or category.
- CSV File Export: Export all database records to a formatted CSV file.
- Visual Analytics: Matplotlib integration showing bar graphs (Stock by Category) 
  and pie charts (Value Distribution).

3. SYSTEM REQUIREMENTS & DEPENDENCIES
--------------------------------------
- Python Version: Python 3.8 or higher
- Required Python Packages:
    * tkinter (Standard Library)
    * sqlite3 (Standard Library)
    * csv (Standard Library)
    * datetime (Standard Library)
    * matplotlib (Install via: pip install matplotlib)

4. HOW TO RUN THE APPLICATION
-----------------------------
1. Ensure Python and matplotlib are installed on your system.
2. Open terminal/command prompt in the project folder.
3. Run command:
     python inventory_tracker.py
4. Enter credentials when prompted:
     Username: admin
     Password: admin123