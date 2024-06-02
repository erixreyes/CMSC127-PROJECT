import mysql.connector
from mysql.connector import Error

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "bbcaleb13",
    database = "KRIMSTIX",
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS KRIMSTIX")
mycursor.execute("USE KRIMSTIX")

UserTable = "CREATE TABLE IF NOT EXISTS user (user_id INT(5) PRIMARY KEY AUTO_INCREMENT, real_name VARCHAR(70), username VARCHAR(20), password VARCHAR(15), isAdmin BOOLEAN, isRegular BOOLEAN)"
#user TABLE
FoodEstabTable = "CREATE TABLE IF NOT EXISTS food_establishment (establishment_id INT(5) PRIMARY KEY AUTO_INCREMENT, establishment_name VARCHAR(50), location VARCHAR(100), average_rating DECIMAL(3,1))"
#food_establishment TABLE
FoodItemTable = "CREATE TABLE IF NOT EXISTS food_item (food_id INT(5) PRIMARY KEY AUTO_INCREMENT, food_name VARCHAR(50), price DECIMAL(5,2) NOT NULL, establishment_id INT(5), FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#food_item TABLE
FoodType = "CREATE TABLE IF NOT EXISTS food_item_food_type (food_type VARCHAR(15), food_id INT(5), PRIMARY KEY (food_type, food_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id))"
#food_item_food_type TABLE
FoodReview = "CREATE TABLE IF NOT EXISTS food_review (review_id INT(5) PRIMARY KEY AUTO_INCREMENT, Date DATE DEFAULT CURRENT_DATE, Rating INT(1), Review VARCHAR(100), user_id INT(5), food_id INT(5), establishment_id INT(5), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id),FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#food_review TABLE
EstabReview = "CREATE TABLE IF NOT EXISTS establishment_review (review_id INT(5) PRIMARY KEY AUTO_INCREMENT, Date DATE DEFAULT CURRENT_DATE, Rating INT(1), Review VARCHAR(100), User_id INT(5), establishment_id INT(5), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#establishment_review TABLE
IsManagedByTable = "CREATE TABLE IF NOT EXISTS is_managed_by (review_id INT(5), user_id INT(5), FOREIGN KEY (review_id) REFERENCES food_review(review_id), FOREIGN KEY (user_id) REFERENCES user(user_id))"
#is_authorized_food TABLE
IsAuthorizedFoodTable = "CREATE TABLE IF NOT EXISTS is_authorized_food (user_id INT(5), food_id INT(5), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id))"
#is_authorized_establishment TABLE
IsAuthorizedEstabTable = "CREATE TABLE IF NOT EXISTS is_authorized_establishment (food_id INT(5), user_id INT(5), FOREIGN KEY (food_id) REFERENCES food_item(food_id), FOREIGN KEY (user_id) REFERENCES user(user_id))"

tables = [UserTable, FoodEstabTable, FoodItemTable, FoodType, FoodReview, EstabReview, IsManagedByTable, IsAuthorizedFoodTable, IsAuthorizedEstabTable]
for table in tables:
    mycursor.execute(table)

def sign_up():
    try:
        real_name = input("Enter your real name: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        insert_query = "INSERT INTO user (real_name, username, password) VALUES (%s, %s, %s)"
        mycursor.execute(insert_query, (real_name, username, password))
        db.commit()

        print("Sign up successful! You can now log in with your username and password.")
    except Error as e:
        print(f"An error occurred: {e}")
        db.rollback()

def login():
    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        mycursor.execute("SELECT user_id, real_name FROM user WHERE username = %s AND password = %s", (username, password))
        user = mycursor.fetchone()

        if user:
            print(f"Welcome back, {user[1]}!")
            return user[0]
        else:
            print("Invalid username or password. Please try again.")
            return None
    except Error as e:
        print(f"An error occurred: {e}")
        return None
    
def select_establishment_and_food():
    try:
        # Display available establishments
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        establishments = mycursor.fetchall()
        if not establishments:
            print("No establishments found.")
            return None, None

        print("Available Establishments:")
        for est_id, name in establishments:
            print(f"ID: {est_id}, Name: {name}")

        # User selects an establishment
        establishment_id = input("Enter the ID of the establishment: ")

        # Display available food items in the selected establishment
        mycursor.execute("SELECT food_id, food_name FROM food_item WHERE establishment_id = %s", (establishment_id,))
        food_items = mycursor.fetchall()
        if not food_items:
            print("No food items found in this establishment.")
            return None, None

        print("Available Food Items in the Establishment:")
        for food_id, food_name in food_items:
            print(f"ID: {food_id}, Name: {food_name}")

        # User selects a food item
        food_id = input("Enter the ID of the food item: ")

        return establishment_id, food_id

    except Exception as e:
        print("An error occurred while selecting establishment and food item:", e)
        return None, None
    
def update_average_rating(establishment_id):
    update_query = """
    UPDATE food_establishment 
    SET average_rating = (SELECT AVG(Rating) FROM food_review WHERE establishment_id = %s)
    WHERE establishment_id = %s
    """
    mycursor.execute(update_query, (establishment_id, establishment_id))
    db.commit()


def add_food_review(user_id):
    establishment_id, food_id = select_establishment_and_food()
    if not establishment_id or not food_id:
        return

    try:
        # User inputs for the review
        rating = int(input("Enter your rating (1-5): "))
        review = input("Enter your review (up to 100 characters): ")

        # Insert the new review
        insert_query = """
        INSERT INTO food_review (Rating, Review, user_id, food_id, establishment_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        mycursor.execute(insert_query, (rating, review, user_id, food_id, establishment_id))
        db.commit()

        update_average_rating(establishment_id)

        print("New review added successfully!")

    except Exception as e:
        print("An error occurred while adding the review:", e)
        db.rollback()


def update_food_review(user_id):
    establishment_id, food_id = select_establishment_and_food()
    if not establishment_id or not food_id:
        return

    try:
        # Display existing reviews for the selected food item
        mycursor.execute("SELECT review_id, Review, Rating FROM food_review WHERE food_id = %s AND establishment_id = %s AND user_id = %s", (food_id, establishment_id, user_id))
        reviews = mycursor.fetchall()
        if not reviews:
            print("No reviews found for this food item in this establishment.")
            return

        print("Existing Reviews for the Food Item:")
        for review_id, review, rating in reviews:
            print(f"Review ID: {review_id}, Review: {review}, Rating: {rating}")

        # User selects the review to update
        review_id = input("Enter the Review ID you want to update: ")

        # User inputs for updating the review
        new_review = input("Enter your new review (up to 100 characters): ")
        new_rating = int(input("Enter your new rating (1-5): "))

        # Update the review details
        update_query = """
        UPDATE food_review
        SET Review = %s, Rating = %s
        WHERE review_id = %s
        """
        mycursor.execute(update_query, (new_review, new_rating, review_id))
        db.commit()

        update_average_rating(establishment_id)

        print("Review updated successfully!")

    except Exception as e:
        print("An error occurred while updating the review:", e)
        db.rollback()


def delete_food_review(user_id):
    establishment_id, food_id = select_establishment_and_food()
    if not establishment_id or not food_id:
        return

    try:
        # Display existing reviews for the selected food item
        mycursor.execute("SELECT review_id, Review, Rating FROM food_review WHERE food_id = %s AND establishment_id = %s AND user_id = %s", (food_id, establishment_id, user_id))
        reviews = mycursor.fetchall()
        if not reviews:
            print("No reviews found for this food item in this establishment.")
            return

        print("Existing Reviews for the Food Item:")
        for review_id, review, rating in reviews:
            print(f"Review ID: {review_id}, Review: {review}, Rating: {rating}")

        # User selects the review to delete
        review_id = input("Enter the Review ID you want to delete: ")

        # Delete the review
        delete_query = "DELETE FROM food_review WHERE review_id = %s"
        mycursor.execute(delete_query, (review_id,))
        db.commit()

        if mycursor.rowcount == 0:
            print("No review found with that ID.")
        else:
            update_average_rating(establishment_id)
            print("Review deleted successfully!")

    except Exception as e:
        print("An error occurred while deleting the review:", e)
        db.rollback()


def add_food_establishment():
    try:
        # User inputs for the new establishment
        establishment_name = input("Enter the establishment name: ")
        location = input("Enter the location: ")

        # SQL command to insert the new establishment without average rating
        insert_query = """
        INSERT INTO food_establishment (establishment_name, location)
        VALUES (%s, %s)
        """
        mycursor.execute(insert_query, (establishment_name, location))
        db.commit()

        # Get the auto-incremented establishment_id of the newly inserted row
        new_establishment_id = mycursor.lastrowid

        # Update the new establishment with the average rating from food_review
        update_query = """
        UPDATE food_establishment 
        SET average_rating = (SELECT AVG(Rating) FROM food_review WHERE establishment_id = %s)
        WHERE establishment_id = %s
        """
        mycursor.execute(update_query, (new_establishment_id, new_establishment_id))
        db.commit()

        print("New establishment added")

    except Error as e:
        print(f"An error occurred: {e}")
        db.rollback()


def delete_food_establishment():
    try:
        # User inputs the ID of the establishment to delete
        establishment_id = input("Enter the ID of the establishment to delete: ")

        # Delete the establishment
        delete_query = "DELETE FROM food_establishment WHERE establishment_id = %s"
        mycursor.execute(delete_query, (establishment_id,))
        db.commit()

        if mycursor.rowcount == 0:
            print("No establishment found with that ID.")
        else:
            print("Establishment deleted successfully!")

    except Exception as e:
        print("An error occurred:", e)
        db.rollback()


def search_food_establishment():
    try:
        # Fetch and display existing establishments
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        results = mycursor.fetchall()
        if results:
            print("Existing Establishments:")
            for est_id, name in results:
                print(f"ID: {est_id}, Name: {name}")
        else:
            print("No establishments found.")
            return
        
    except Exception as e:
        print("An error occurred:", e)
        db.rollback()


def update_food_establishment():
    try:
        # Fetch and display existing establishments
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        results = mycursor.fetchall()
        if results:
            print("Existing Establishments:")
            for est_id, name in results:
                print(f"ID: {est_id}, Name: {name}")
        else:
            print("No establishments found.")
            return

        # User selects which establishment to update
        establishment_id = input("Enter the ID of the establishment to update: ")
        
        # New details for the establishment
        new_name = input("Enter the new name of the establishment: ")
        new_location = input("Enter the new location: ")
        new_rating = float(input("Enter the new average rating (0.0 - 5.0): "))

        # Update the establishment details
        update_query = """
        UPDATE food_establishment
        SET establishment_name = %s, location = %s, average_rating = %s
        WHERE establishment_id = %s
        """
        mycursor.execute(update_query, (new_name, new_location, new_rating, establishment_id))
        db.commit()

        print("Establishment updated successfully!")

    except Exception as e:
        print("An error occurred:", e)
        db.rollback()

def add_food_item():
    try:
        # Ask for the establishment ID first
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        results = mycursor.fetchall()
        if results:
            print("Existing Establishments:")
            for est_id, name in results:
                print(f"ID: {est_id}, Name: {name}")
        else:
            print("No establishments found.")
            return
        
        establishment_id = int(input("Enter the establishment ID: "))

        # User inputs for the new food item
        food_name = input("Enter the food item name: ")
        price = float(input("Enter the price of the food item: "))
        foodtype = input("Enter the food type of food item: ")

        # Insert the new food item
        insert_query = """
        INSERT INTO food_item (food_name, price, establishment_id)
        VALUES (%s, %s, %s)
        """
        mycursor.execute(insert_query, (food_name, price, establishment_id))
        db.commit()

        new_food_id = mycursor.lastrowid

        insert_query2 = """
        INSERT INTO food_item_food_type (food_type, food_id)
        VALUES (%s, %s)
        """
        mycursor.execute(insert_query2, (foodtype, new_food_id))
        db.commit()

        print("New food item added successfully!")

    except Error as e:
        print(f"An error occurred: {e}")
        db.rollback()


def delete_food_item():
    try:
        # Ask for the establishment ID first
        establishment_id = int(input("Enter the establishment ID: "))

        # Fetch and display existing food items for the establishment
        mycursor.execute("SELECT food_id, food_name FROM food_item WHERE establishment_id = %s", (establishment_id,))
        results = mycursor.fetchall()
        if results:
            print("Existing Food Items:")
            for food_id, food_name in results:
                print(f"ID: {food_id}, Name: {food_name}")
        else:
            print("No food items found for this establishment.")
            return

        # User inputs the ID of the food item to delete
        food_id = int(input("Enter the ID of the food item to delete: "))

        # Delete the food item
        delete_query = "DELETE FROM food_item WHERE food_id = %s AND establishment_id = %s"
        mycursor.execute(delete_query, (food_id, establishment_id))
        db.commit()

        if mycursor.rowcount == 0:
            print("No food item found with that ID.")
        else:
            print("Food item deleted successfully!")

    except Error as e:
        print("An error occurred:", e)
        db.rollback()


def search_food_item():
    try:
        # Ask for the establishment ID first
        establishment_id = int(input("Enter the establishment ID: "))

        # Fetch and display existing food items for the establishment
        mycursor.execute("SELECT food_id, food_name, price FROM food_item WHERE establishment_id = %s", (establishment_id,))
        results = mycursor.fetchall()
        if results:
            print("Existing Food Items:")
            for food_id, food_name, price in results:
                print(f"ID: {food_id}, Name: {food_name}, Price: {price}")
        else:
            print("No food items found for this establishment.")
            return
        
    except Error as e:
        print("An error occurred:", e)
        db.rollback()
        
def update_food_item():
    try:
        # Ask for the establishment ID first
        establishment_id = int(input("Enter the establishment ID: "))

        # Fetch and display existing food items for the establishment
        mycursor.execute("SELECT food_id, food_name, price FROM food_item WHERE establishment_id = %s", (establishment_id,))
        results = mycursor.fetchall()
        if results:
            print("Existing Food Items:")
            for food_id, food_name, price in results:
                print(f"ID: {food_id}, Name: {food_name}, Price: {price}")
        else:
            print("No food items found for this establishment.")
            return

        # User selects which food item to update
        food_id = int(input("Enter the ID of the food item to update: "))

        # New details for the food item
        new_name = input("Enter the new name of the food item: ")
        new_price = float(input("Enter the new price of the food item: "))

        # Update the food item details
        update_query = """
        UPDATE food_item
        SET food_name = %s, price = %s
        WHERE food_id = %s AND establishment_id = %s
        """
        mycursor.execute(update_query, (new_name, new_price, food_id, establishment_id))
        db.commit()

        print("Food item updated successfully!")

    except Error as e:
        print("An error occurred:", e)
        db.rollback()


def show_establishments():
    try:
        # Fetch and display all food establishments
        mycursor.execute("SELECT * FROM food_establishment")
        results = mycursor.fetchall()
        if results:
            print("All Food Establishments:")
            for establishment in results:
                print(f"ID: {establishment[0]}, Name: {establishment[1]}, Location: {establishment[2]}, Average Rating: {establishment[3]}")
        else:
            print("No establishments found.")
    except Exception as e:
        print("An error occurred while fetching establishments:", e)

def view_all_food_reviews():
    try:
        establishment_id, food_id = select_establishment_and_food()
        if establishment_id and food_id:
            # View all food reviews for the selected food item
            mycursor.execute("SELECT Review, Rating, Date FROM food_review WHERE food_id = %s AND establishment_id = %s", (food_id, establishment_id))
            reviews = mycursor.fetchall()
            if reviews:
                print("Food Reviews:")
                for review in reviews:
                    print(f"Review: {review[0]}, Rating: {review[1]}, Date: {review[2]}")
            else:
                print("No reviews found for the selected food item in the selected establishment.")
        else:
            print("Invalid establishment or food item.")
    except Exception as e:
        print("An error occurred while fetching reviews:", e)

def view_all_food_items():
    try:
        # Display available establishments
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        establishments = mycursor.fetchall()
        if not establishments:
            print("No establishments found.")
            return

        print("Available Establishments:")
        for est_id, name in establishments:
            print(f"ID: {est_id}, Name: {name}")

        # User selects an establishment
        establishment_id = input("Enter the ID of the establishment: ")

        # View all food items for the selected establishment
        mycursor.execute("SELECT food_id, food_name, price FROM food_item WHERE establishment_id = %s", (establishment_id,))
        food_items = mycursor.fetchall()
        if food_items:
            print("Food Items in the Establishment:")
            for food_item in food_items:
                print(f"ID: {food_item[0]}, Name: {food_item[1]}, Price: {food_item[2]}")
        else:
            print("No food items found in the selected establishment.")
    except Exception as e:
        print("An error occurred while fetching food items:", e)

def view_all_food_items_by_type():
    try:
        # Display available establishments
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        establishments = mycursor.fetchall()
        if not establishments:
            print("No establishments found.")
            return

        print("Available Establishments:")
        for est_id, name in establishments:
            print(f"ID: {est_id}, Name: {name}")

        # User selects an establishment
        establishment_id = input("Enter the ID of the establishment: ")

        # User selects a food type
        food_type = input("Enter the food type (Vegetable, Meat, Seafood, Pasta): ")
  
        # View all food items for the selected establishment and food type
        mycursor.execute("""
        SELECT fi.food_id, fi.food_name, fi.price 
        FROM food_item fi 
        JOIN food_item_food_type ft ON fi.food_id = ft.food_id 
        WHERE fi.establishment_id = %s AND ft.food_type = %s
        """, (establishment_id, food_type))
        food_items = mycursor.fetchall()
        if food_items:
            print(f"Food Items in the Establishment ({food_type}):")
            for food_item in food_items:
                print(f"ID: {food_item[0]}, Name: {food_item[1]}, Price: {food_item[2]}")
        else:
            print(f"No food items found in the selected establishment for the food type '{food_type}'.")
    except Exception as e:
        print("An error occurred while fetching food items by type:", e)

def view_reviews_within_month():
    try:
        establishment_id, food_id = select_establishment_and_food()
        if establishment_id and food_id:
            # View all reviews made within the last 30 days for the selected food item
            mycursor.execute("""
            SELECT review_id, Date, Rating, Review
            FROM food_review
            WHERE food_id = %s AND establishment_id = %s
            AND Date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            """, (food_id, establishment_id))
            reviews = mycursor.fetchall()
            if reviews:
                print("Food Reviews within the last 30 days:")
                for review in reviews:
                    print(f"ID: {review[0]}, Date: {review[1]}, Rating: {review[2]}, Review: {review[3]}")
            else:
                print("No reviews found for the selected food item in the selected establishment within the last 30 days.")
        elif establishment_id:
            # View all reviews made within the last 30 days for the selected establishment
            mycursor.execute("""
            SELECT review_id, Date, Rating, Review
            FROM establishment_review
            WHERE establishment_id = %s
            AND Date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            """, (establishment_id,))
            reviews = mycursor.fetchall()
            if reviews:
                print("Establishment Reviews within the last 30 days:")
                for review in reviews:
                    print(f"ID: {review[0]}, Date: {review[1]}, Rating: {review[2]}, Review: {review[3]}")
            else:
                print("No reviews found for the selected establishment within the last 30 days.")
        else:
            print("Invalid establishment or food item.")
    except Exception as e:
        print("An error occurred while fetching reviews within the last 30 days:", e)

def view_high_rated_establishments():
    try:
        # Fetch and display all establishments with an average rating >= 4
        mycursor.execute("""
        SELECT establishment_id, establishment_name, average_rating 
        FROM food_establishment 
        WHERE average_rating >= 4
        """)
        establishments = mycursor.fetchall()

        if establishments:
            print("High Rated Establishments (Rating >= 4):")
            for establishment in establishments:
                print(f"ID: {establishment[0]}, Name: {establishment[1]}, Average Rating: {establishment[2]}")
        else:
            print("No establishments found with a high average rating.")
    except Exception as e:
        print("An error occurred while fetching high-rated establishments:", e)


def view_food_items_by_price():
    try:
        # Display available establishments
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        establishments = mycursor.fetchall()
        if not establishments:
            print("No establishments found.")
            return

        print("Available Establishments:")
        for est_id, name in establishments:
            print(f"ID: {est_id}, Name: {name}")

        # User selects an establishment
        establishment_id = input("Enter the ID of the establishment: ")

        # Ask user for sorting preference
        sort_order = input("Do you want to sort by price in ascending or descending order? (Enter 'asc' for ascending and 'desc' for descending): ").strip().lower()

        if sort_order not in ['asc', 'desc']:
            print("Invalid sorting order. Please enter 'asc' or 'desc'.")
            return

        # View all food items for the selected establishment, sorted by price
        sort_order_sql = "ASC" if sort_order == 'asc' else "DESC"
        mycursor.execute(f"""
        SELECT food_id, food_name, price 
        FROM food_item 
        WHERE establishment_id = %s 
        ORDER BY price {sort_order_sql}
        """, (establishment_id,))
        food_items = mycursor.fetchall()

        if food_items:
            print(f"Food Items in the Establishment sorted by price ({sort_order_sql}):")
            for food_item in food_items:
                print(f"ID: {food_item[0]}, Name: {food_item[1]}, Price: {food_item[2]}")
        else:
            print("No food items found in the selected establishment.")
    except Exception as e:
        print("An error occurred while fetching food items:", e)

def search_food_items_by_price_and_type():
    try:
        # Get user input for price range
        min_price = input("Enter the minimum price: ").strip()
        max_price = input("Enter the maximum price: ").strip()

        # Get user input for food type
        food_type = input("Enter the food type (Meat, Vegetable, Seafood, Pasta): ").strip()

        # Build the SQL query based on the inputs
        query = """
        SELECT fi.food_id, fi.food_name, fi.price, fe.establishment_name 
        FROM food_item fi 
        JOIN food_establishment fe ON fi.establishment_id = fe.establishment_id
        """
        conditions = []
        params = []

        if min_price:
            conditions.append("fi.price >= %s")
            params.append(min_price)
        if max_price:
            conditions.append("fi.price <= %s")
            params.append(max_price)
        if food_type:
            query += " JOIN food_item_food_type ft ON fi.food_id = ft.food_id"
            conditions.append("ft.food_type = %s")
            params.append(food_type)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute the query
        mycursor.execute(query, params)
        food_items = mycursor.fetchall()

        # Display the results
        if food_items:
            print("Search Results:")
            for food_item in food_items:
                print(f"ID: {food_item[0]}, Name: {food_item[1]}, Price: {food_item[2]}, Establishment: {food_item[3]}")
        else:
            print("No food items found matching the criteria.")
    except Exception as e:
        print("An error occurred while searching for food items:", e)




def exit_program():
    print("Exiting program...")
    exit()

def default():
    print("Invalid option. Please choose again!")


def foodReview(user_id):
    print("""
    1. Review a Food item
    2. Update an exitsting Food review
    3. Delete an exitsting Food review
    4. Back
    """)
    choice = input("Enter your choice: ")
    
    if choice == '1':
        add_food_review(user_id)
    elif choice == '2':
        update_food_review(user_id)
    elif choice == '3':
        delete_food_review(user_id)
    elif choice == '4':
        menu
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")



def foodEstablishment():
    print("""
    1. Add a Food Establishment
    2. Search a Food Establishment 
    3. Update an exitsting Food Establishment
    4. Delete an exitsting Food Establishment
    5. Back
    """)
    choice = input("Enter your choice: ")
    
    if choice == '1':
        add_food_establishment()
    elif choice == '2':
        search_food_establishment()
    elif choice == '3':
        update_food_establishment()
    elif choice == '4':
        delete_food_establishment()
    elif choice == '5':
        menu
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

def foodItem():
    print("""
    1. Search a Food item
    2. Add a Food item
    3. Update a existing Food item
    4. Delete a existing Food item
    5. Back
    """)
    choice = input("Enter your choice: ")
    
    if choice == '1':
        search_food_item()
    elif choice == '2':
        add_food_item()
    elif choice == '3':
        update_food_item()
    elif choice == '4':
        delete_food_item()
    elif choice == '5':
        menu
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")


def reports():
    print("""
    1. Show All Establishments
    2. View Food review
    3. View All Food 
    4. View Food Items by Type
    5. View reviews within month
    6. View High Rated
    7. View Food Items by Price
    8. Search food items by price and type
    9. Back
    """)
    choice = input("Enter your choice: ")

    if choice == '1':
        show_establishments()
    elif choice == '2':
        view_all_food_reviews()
    elif choice == '3':
        view_all_food_items()
    elif choice == '4':
        view_all_food_items_by_type()
    elif choice == '5':
        view_reviews_within_month()
    elif choice == '6':
        view_high_rated_establishments()
    elif choice == '7':
        view_food_items_by_price()
    elif choice == '8':
        search_food_items_by_price_and_type()
    elif choice == '9':
        menu
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")


def menu():
    while True:
        print("""
        1. Food review
        2. Food establishment
        3. Food item
        4. General Reports
        5. Exit
        """)
        choice = input("Enter your choice: ")

        if choice == '1':
            foodReview(user_id)
        elif choice == '2':
            foodEstablishment()
        elif choice == '3':
            foodItem()
        elif choice == '4':
            reports()
        elif choice == '5':
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def newUser():
    print("""
    Are you a new User? 
    1. Yes
    2. No
    """)
    choice = input("Enter your choice: ")
    return int(choice)

newUser_options = {
    1: sign_up,
    2: login,
}

newUser_options = {
    1: foodReview,
    2: foodEstablishment,
    3: foodItem,
    4: reports,
    5: exit_program,
}


foodEstablishment_options = {
    1: add_food_establishment, 
    2: search_food_establishment,
    3: update_food_establishment,
    4: delete_food_establishment,
    5: menu
}

foodItem_options = {
    1: search_food_item, 
    2: add_food_item,
    3: update_food_item,
    4: delete_food_item,
    5: menu
}

reports_options = { #dito mo lagay yung reports
    1: select_establishment_and_food, 
    2: search_food_item,
    3: add_food_item,
    4: delete_food_item,
    5: update_food_item,
    6: menu
}

if __name__ == "__main__":
    while True:
        print("Welcome to KRIMSTIX")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            sign_up()
        elif choice == '2':
            user_id = login()
            if user_id:
                menu()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")