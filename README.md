# CMSC127-PROJECT
## KRIMSTIX (ST-4L)
## CASTRO, GREGORIO, REYES

## Program Specs
- A simple Terminal-based DBMS on food reviews on food establishments and their food
- Implements a simple sign-in system
- Sign up as admin/regular

### Admin Access
- Admin has access to data on the regular userbase, they can also delete regular users
- Admin can delete any food review made by the regular
- Admin can CRUD food items and food establishments (as well search)
- Admin can access the general reports

### Regular Access
- Regular has no access to the userbase
- Regular can CRUD food and establishment reviews, (can only delete and update their own reviews)
- Regular can only browse the available food establishments and food items
- Regular can access the general reports

### Features
1. Add, update, and delete a food review (on a food establishment or a food item)
2. Add, delete, search, and update a food establishment (ADD, SEARCH, DELETE Admin Access)
3. Add, delete, search, and update a food item. (ADD, SEARCH, DELETE Admin Access)
4. View, delete Regular user (Admin Access)

### Reports to be generated
1. View all food establishments;
2. View all food reviews for an establishment or a food item
3. View all food items from an establishment
4. View all food items from an establishment that belong to a food type
5. View all reviews made within a month for an establishment or a food item
6. View all establishments with a high average rating (>=4)
7. View all food items from an establishment arranged according to price
8. Search food items from any establishment based on a given price range and/or food type

### Necessary Applications
- Python (version 3 or higher) 
- MariaDB

### Instructions
- set the proper mariaDB server in sql connector (in "db = mysql.connector.connect" line 4 and 14)
    - set host, user, and password of your system's mariaDB server
    - the program will automatically create a database and then is used afterwards

#### TO RUN
- simply type this command on your terminal, "python .\KRIMSTIX.py"
