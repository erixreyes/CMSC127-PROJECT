import mysql.connector
from mysql.connector import Error

db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="caleb"
    )

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS KRIMSTIX")

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "caleb",
    database = "KRIMSTIX",
)

mycursor = db.cursor()

mycursor.execute("USE KRIMSTIX")

UserTable = "CREATE TABLE IF NOT EXISTS user (user_id INT(5) PRIMARY KEY AUTO_INCREMENT, real_name VARCHAR(70), username VARCHAR(20), password VARCHAR(15), isAdmin BOOLEAN)"
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

tables = [UserTable, FoodEstabTable, FoodItemTable, FoodType, FoodReview, EstabReview]
for table in tables:
    mycursor.execute(table)


def sign_upAdmin(): #signup function for admin
    try:
        real_name = input("Enter your real name: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        insert_query = "INSERT INTO user (real_name, username, password, isAdmin) VALUES (%s, %s, %s, True)"
        mycursor.execute(insert_query, (real_name, username, password))
        db.commit()

        print("Sign up successful! You can now log in with your username and password.")
    except Error as e:
        print(f"An error occurred: {e}")
        db.rollback()

def sign_upReg(): #signup function for regular
    try:
        real_name = input("Enter your real name: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        insert_query = "INSERT INTO user (real_name, username, password, isAdmin) VALUES (%s, %s, %s, False)"
        mycursor.execute(insert_query, (real_name, username, password))
        db.commit()

        print("Sign up successful! You can now log in with your username and password.")
    except Error as e:
        print(f"An error occurred: {e}")
        db.rollback()

def login(): #login function for both admin and regular
    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        query = "SELECT user_id, real_name, isAdmin FROM user WHERE username = %s AND password = %s"
        mycursor.execute(query, (username, password))
        user = mycursor.fetchone()

        if user:
            user_id, real_name, isAdmin = user
            print(f"Welcome back, {real_name}!")
            return user_id, isAdmin  # return both user_id and isAdmin for global access
        else:
            print("Invalid username or password. Please try again.")
            return None, None
    except Error as e:
        print(f"An error occurred: {e}")
        return None, None

#EXTRA FEATURES
def view_all_users(): #view all regular users
    try:
        mycursor.execute("SELECT user_id, username, real_name FROM user")
        results = mycursor.fetchall()
        if results:
            print("----- Userbase -----")
            for est_id, user_name, name in results:
                print(f"""
-----------------------
ID: {est_id}
Username: {user_name}, 
Name: {name}
-----------------------""")
        else:
            print("No Users found.")
            return
        
    except Exception as e:
        print("An error occurred:", e)
        db.rollback()

def delete_user(): #delete selected regular users
    try:
        mycursor.execute("SELECT user_id, username, real_name FROM user")
        results = mycursor.fetchall()
        if results:
            print("----- Userbase -----")
            for user_id, username, real_name in results:
                print(f"""
-----------------------
ID: {user_id}
Username: {username}, 
Name: {real_name}
-----------------------""")
        else:
            print("No Users found.")
            return
        
        user_id = input("Enter the ID of the user to delete: ")

        # check the id of the user, only regular can be deleted
        check_admin_query = "SELECT isAdmin FROM user WHERE user_id = %s"
        mycursor.execute(check_admin_query, (user_id,))
        result = mycursor.fetchone()

        if result is None:
            print("No user found with that ID.")
            return

        if result[0]:  #result[0] is the isAdmin value
            print("Cannot delete an admin user.")
            return

        delete_queries = [ # delete related records
            "DELETE FROM establishment_review WHERE user_id = %s",
            "DELETE FROM food_review WHERE user_id = %s",
            "DELETE FROM user WHERE user_id = %s"
        ]

        for query in delete_queries:
            mycursor.execute(query, (user_id,))

        db.commit()

        if mycursor.rowcount == 0:
            print("No user found with that ID.")
        else:
            print("User and related records deleted successfully!")

    except Exception as e:
        print("An error occurred:", e)
        db.rollback()



#BASIC FEATURES   
def select_establishment_and_food():    # function where it asks for what establishment and food item
    try:
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment") #display available establishments
        establishments = mycursor.fetchall()
        if not establishments:
            print("No establishments found.")
            return None, None

        print("Available Establishments:")
        for est_id, name in establishments:
            print(f"ID: {est_id}, Name: {name}")

        establishment_id = input("Enter the ID of the establishment: ")

        mycursor.execute("SELECT food_id, food_name FROM food_item WHERE establishment_id = %s", (establishment_id,))  #display available food items in the selected establishment
        food_items = mycursor.fetchall()
        if not food_items:
            print("No food items found in this establishment.")
            return None, None

        print("Available Food Items in the Establishment:")
        for food_id, food_name in food_items:
            print(f"ID: {food_id}, Name: {food_name}")

        food_id = input("Enter the ID of the food item: ")

        return establishment_id, food_id

    except Exception as e:
        print("An error occurred while selecting establishment and food item:", e)
        return None, None
    
def update_average_rating(establishment_id): #function that updates the average rating of a food establishment after any event that is related to a food establishment
    update_query = """
    UPDATE food_establishment 
    SET average_rating = (SELECT AVG(Rating) FROM food_review WHERE establishment_id = %s)
    WHERE establishment_id = %s
    """
    mycursor.execute(update_query, (establishment_id, establishment_id))
    db.commit()

#CRUD FOOD ESTABLISHMENT REVIEWS
def add_estab_review(user_id):  #create a establishment review
    try:
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        establishments = mycursor.fetchall()
        if not establishments:
            print("No establishments found.")
            return

        print("Available Establishments:")
        for est_id, name in establishments:
            print(f"ID: {est_id}, Name: {name}")

        establishment_id = input("Enter the ID of the establishment: ")

        review = input("Enter your review (up to 100 characters): ")

        while True:
            rating = input("Enter your rating (1-5): ")
            if rating.isdigit() and 1 <= int(rating) <= 5:
                rating = int(rating)
                break
            else:
                print("Invalid input. Please enter a number between 1 and 5.")

        insert_query = """
        INSERT INTO establishment_review (Rating, Review, user_id, establishment_id)
        VALUES (%s, %s, %s, %s)
        """
        mycursor.execute(insert_query, (rating, review, user_id, establishment_id))
        db.commit()

        update_average_rating(establishment_id)

        print("New review added successfully!")

    except Exception as e:
        print("An error occurred while adding the review:", e)
        db.rollback()

def update_estab_review(user_id): #updates an existing establishment review
    try:
        query = """
        SELECT e.review_id, fe.establishment_id, fe.establishment_name, fi.food_name, e.Review, e.Rating
        FROM establishment_review e
        JOIN food_establishment fe ON e.establishment_id = fe.establishment_id
        WHERE e.user_id = %s
        """
        mycursor.execute(query, (user_id,))
        reviews = mycursor.fetchall()
        
        if not reviews:
            print("No reviews found for this user.")
            return

        print("Existing Establishment Reviews:")
        for review_id, establishment_id, establishment_name, review, rating in reviews:
            print(f"Review ID: {review_id}, Establishment: {establishment_name}, Review: {review}, Rating: {rating}")

        review_id = input("Enter the Review ID you want to update: ")

        selected_review = next((r for r in reviews if str(r[0]) == review_id), None)
        if not selected_review:
            print("Invalid Review ID selected.")
            return

        new_review = input("Enter your new review (up to 100 characters): ")

        while True:
            new_rating = input("Enter your new rating (1-5): ")
            if new_rating.isdigit() and 1 <= int(new_rating) <= 5:
                new_rating = int(new_rating)
                break
            else:
                print("Invalid input. Please enter a number between 1 and 5.")

        update_query = """
        UPDATE establishment_review
        SET Review = %s, Rating = %s
        WHERE review_id = %s
        """
        mycursor.execute(update_query, (new_review, new_rating, review_id))
        db.commit()

        update_average_rating(establishment_id)    #update the average rating for the establishment

        print("Review updated successfully!")

    except Exception as e:
        print("An error occurred while updating the review:", e)
        db.rollback()

def delete_estab_review(user_id):   #deletes an existing establishment review
    try:
        if isAdmin: # if admin, can delete any existing establishment review from any user
            mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
            establishments = mycursor.fetchall()
            if not establishments:
                print("No establishments found.")
                return

            print("Available Establishments:")
            for est_id, name in establishments:
                print(f"ID: {est_id}, Name: {name}")

            establishment_id = input("Enter the ID of the establishment: ")

            query = """
            SELECT f.review_id, f.Review, f.Rating, f.Date, u.username
            FROM establishment_review f
            LEFT JOIN user u ON f.user_id = u.user_id
            WHERE f.establishment_id=%s"""

            mycursor.execute(query, (establishment_id,))
            reviews = mycursor.fetchall()

            if not reviews:
                print("No reviews found for this establishment.")
                return

            print("Existing Reviews for the Establishment:")
            for review_id, review, rating, date, username in reviews:
                print(f"Review ID: {review_id}, Username: {username}, Review: {review}, Rating: {rating}, Date: {date}")

        else:  # if regular, can only delete their existing establishment review

            query = """
            SELECT fr.review_id, fe.establishment_name, fr.Rating
            FROM establishment_review fr
            JOIN food_establishment fe ON fr.establishment_id = fe.establishment_id
            WHERE fr.user_id = %s
            """
            mycursor.execute(query, (user_id))
            reviews = mycursor.fetchall()

            if not reviews:
                print("No reviews found for this user.")
                return

            print("Existing Establishment Reviews:")
            for review_id, establishment_name, food_name, rating in reviews:
                print(f"Review ID: {review_id}, Establishment: {establishment_name}, Food Item: {food_name}, Rating: {rating}")

        review_id = input("Enter the Review ID you want to delete: ")

        delete_query = "DELETE FROM establishment_review WHERE review_id = %s"
        mycursor.execute(delete_query, (review_id,))
        db.commit()

        if mycursor.rowcount == 0:
            print("No review found with that ID.")
        else:
            if isAdmin:
                # For admin, update the average rating of the selected establishment
                update_average_rating(establishment_id)
            else:
                # For regular, find the establishment_id related to the deleted review
                establishment_id_query = """
                SELECT establishment_id
                FROM establishment_review
                WHERE review_id = %s
                """
                mycursor.execute(establishment_id_query, (review_id,))
                establishment_id_result = mycursor.fetchone()

                if establishment_id_result:
                    update_average_rating(establishment_id_result[0])

            print("Review deleted successfully!")

    except Exception as e:
        print("An error occurred while deleting the review:", e)
        db.rollback()


#CRUD FOOD REVIEW
def add_food_review(user_id):   #add food review
    establishment_id, food_id = select_establishment_and_food() #get establishment_id and food_id from select_establishment_and_food() function
    if not establishment_id or not food_id:
        return

    try:
        review = input("Enter your review (up to 100 characters): ")

        while True:
            rating = input("Enter your rating (1-5): ")
            if rating.isdigit() and 1 <= int(rating) <= 5:
                rating = int(rating)
                break
            else:
                print("Invalid input. Please enter a number between 1 and 5.")

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
    try:
        # display all reviews made by the user
        query = """
        SELECT fr.review_id, fe.establishment_id, fe.establishment_name, fi.food_name, fr.Review, fr.Rating
        FROM food_review fr
        JOIN food_establishment fe ON fr.establishment_id = fe.establishment_id
        JOIN food_item fi ON fr.food_id = fi.food_id
        WHERE fr.user_id = %s
        """
        mycursor.execute(query, (user_id,))
        reviews = mycursor.fetchall()
        
        if not reviews:
            print("No reviews found for this user.")
            return

        print("Existing Reviews:")
        for review_id, establishment_id, establishment_name, food_name, review, rating in reviews:
            print(f"Review ID: {review_id}, Establishment: {establishment_name}, Food Item: {food_name}, Review: {review}, Rating: {rating}")

        review_id = input("Enter the Review ID you want to update: ")

        # Check if the selected review_id is valid
        selected_review = next((r for r in reviews if str(r[0]) == review_id), None)
        if not selected_review:
            print("Invalid Review ID selected.")
            return

        new_review = input("Enter your new review (up to 100 characters): ")

        while True:
            new_rating = input("Enter your new rating (1-5): ")
            if new_rating.isdigit() and 1 <= int(new_rating) <= 5:
                new_rating = int(new_rating)
                break
            else:
                print("Invalid input. Please enter a number between 1 and 5.")

        update_query = """
        UPDATE food_review
        SET Review = %s, Rating = %s
        WHERE review_id = %s
        """
        mycursor.execute(update_query, (new_review, new_rating, review_id))
        db.commit()

        update_average_rating(establishment_id)  # Update the average rating for the establishment

        print("Review updated successfully!")

    except Exception as e:
        print("An error occurred while updating the review:", e)
        db.rollback()



def delete_food_review(user_id, isAdmin):   #delete a food review
    try:
        if isAdmin: #if admin, can delete any food review from any regular
            establishment_id, food_id = select_establishment_and_food()
            if not establishment_id or not food_id:
                return

            # display existing reviews for the selected food item
            query = """
            SELECT f.review_id, f.Review, f.Rating, f.Date, u.username
            FROM food_review f
            LEFT JOIN user u ON f.user_id = u.user_id
            WHERE f.food_id = %s AND f.establishment_id = %s"""

            mycursor.execute(query, (food_id, establishment_id))
            reviews = mycursor.fetchall()

            if not reviews:
                print("No reviews found for this food item in this establishment.")
                return

            print("Existing Reviews for the Food Item:")
            for review_id, review, rating, date, username in reviews:
                print(f"Review ID: {review_id}, Username: {username}, Review: {review}, Rating: {rating}, Date: {date}")

        else:
            # display existing reviews by the user
            query = """
            SELECT fr.review_id, fe.establishment_name, fi.food_name, fr.Rating
            FROM food_review fr
            JOIN food_establishment fe ON fr.establishment_id = fe.establishment_id
            JOIN food_item fi ON fr.food_id = fi.food_id
            WHERE fr.user_id = %s
            """
            mycursor.execute(query, (user_id,))
            reviews = mycursor.fetchall()

            if not reviews:
                print("No reviews found for this user.")
                return

            print("Existing Reviews:")
            for review_id, establishment_name, food_name, rating in reviews:
                print(f"Review ID: {review_id}, Establishment: {establishment_name}, Food Item: {food_name}, Rating: {rating}")

        review_id = input("Enter the Review ID you want to delete: ")

        delete_query = "DELETE FROM food_review WHERE review_id = %s"
        mycursor.execute(delete_query, (review_id,))
        db.commit()

        if mycursor.rowcount == 0:
            print("No review found with that ID.")
        else:
            if isAdmin:
                # For admin, update the average rating of the selected establishment
                update_average_rating(establishment_id)
            else:
                # For regular, find the establishment_id related to the deleted review
                establishment_id_query = """
                SELECT establishment_id
                FROM food_review
                WHERE review_id = %s
                """
                mycursor.execute(establishment_id_query, (review_id,))
                establishment_id_result = mycursor.fetchone()

                if establishment_id_result:
                    update_average_rating(establishment_id_result[0])

            print("Review deleted successfully!")

    except Exception as e:
        print("An error occurred while deleting the review:", e)
        db.rollback()



def add_food_establishment():   #add a food establishment
    try:
        establishment_name = input("Enter the establishment name: ")
        location = input("Enter the location: ")

        insert_query = """
        INSERT INTO food_establishment (establishment_name, location)
        VALUES (%s, %s)
        """
        mycursor.execute(insert_query, (establishment_name, location))
        db.commit()

        new_establishment_id = mycursor.lastrowid   # Get the auto-incremented establishment_id of the newly inserted row

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


def delete_food_establishment():    #deletes a food establishment as well as related reviews, food items
    try:
        # User inputs the ID of the establishment to delete
        print("""
    CAUTION: DELETION OF ESTABLISHMENT WILL RESULT TO DELETION OF RELATED REVIEWS AND FOOD ITEMS
    1. Proceed
    2. Back
    """)
        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            
            mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
            establishments = mycursor.fetchall()
            if not establishments:
                print("No establishments found.")
                return None, None

            print("Available Establishments:")
            for est_id, name in establishments:
                print(f"ID: {est_id}, Name: {name}")
            
            establishment_id = input("Enter the ID of the establishment to delete: ")

            # Delete queries from affected tables
            delete_query1 = "DELETE FROM establishment_review WHERE establishment_id = %s"
            mycursor.execute(delete_query1, (establishment_id,))

            delete_query2 = "DELETE FROM food_review WHERE establishment_id = %s"
            mycursor.execute(delete_query2, (establishment_id,))

            delete_query3 = "DELETE FROM food_item_food_type WHERE food_id IN (SELECT food_id FROM food_item WHERE establishment_id = %s)"
            mycursor.execute(delete_query3, (establishment_id,))

            delete_query4 = "DELETE FROM food_item WHERE establishment_id = %s"
            mycursor.execute(delete_query4, (establishment_id,))

            delete_query5 = "DELETE FROM food_establishment WHERE establishment_id = %s"
            mycursor.execute(delete_query5, (establishment_id,))

            db.commit()

            if mycursor.rowcount == 0:
                print("No establishment found with that ID.")
            else:
                print("Establishment deleted successfully!")

        elif choice == '2': 
            menu        
    except Exception as e:
        print("An error occurred:", e)
        db.rollback()


def search_food_establishment():    #browse all food establishments
    try:
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        results = mycursor.fetchall()
        if results:
            print("Existing Establishments:")
            for est_id, name in results:
                print(f"""
--------------
ID: {est_id}
Name: {name}
--------------
""")
        else:
            print("No establishments found.")
            return
        
    except Exception as e:
        print("An error occurred:", e)
        db.rollback()


def update_food_establishment():    #update an existing food establishment
    try:
        mycursor.execute("SELECT establishment_id, establishment_name FROM food_establishment")
        results = mycursor.fetchall()
        if results:
            print("Existing Establishments:")
            for est_id, name in results:
                print(f"ID: {est_id}, Name: {name}")
        else:
            print("No establishments found.")
            return

        establishment_id = input("Enter the ID of the establishment to update: ")
        
        # New details for the establishment
        new_name = input("Enter the new name of the establishment: ")
        new_location = input("Enter the new location: ")

        update_query = """
        UPDATE food_establishment
        SET establishment_name = %s, location = %s
        WHERE establishment_id = %s
        """
        mycursor.execute(update_query, (new_name, new_location, establishment_id))
        db.commit()

        print("Establishment updated successfully!")

    except Exception as e:
        print("An error occurred:", e)
        db.rollback()

def add_food_item():    #add food items
    try:
        # ask for the establishment ID first
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

        mycursor.execute("SELECT food_id, food_name, price FROM food_item WHERE establishment_id = %s", (establishment_id,))
        results = mycursor.fetchall()
        print("Existing Food Items:")
        for food_id, food_name, price in results:
            print(f"ID: {food_id}, Name: {food_name}, Price: {price}")

        food_name = input("Enter the food item name: ")
        price = float(input("Enter the price of the food item: "))
        foodtype = input("Enter the food type of food item: ")

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


def delete_food_item(): #delete an existing food item
    try:
        # User inputs the ID of the food item to delete
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
        
        print("""
    CAUTION: DELETION OF FOOD ITEM WILL RESULT IN THE DELETION OF RELATED REVIEWS AND ASSOCIATIONS
    1. Proceed
    2. Back
    """)
        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            mycursor.execute("SELECT food_id, food_name, price FROM food_item WHERE establishment_id = %s", (establishment_id,))
            results = mycursor.fetchall()
            if results:
                print("Existing Food Items:")
                for food_id, food_name, price in results:
                    print(f"ID: {food_id}, Name: {food_name}, Price: {price}")
            else:
                print("No food items found for this establishment.")
                return

            food_id = input("Enter the ID of the food item to delete: ")

            # Delete queries from affected tables
            delete_query2 = "DELETE FROM food_item_food_type WHERE food_id = %s"
            mycursor.execute(delete_query2, (food_id,))

            delete_query3 = "DELETE FROM food_review WHERE food_id = %s"
            mycursor.execute(delete_query3, (food_id,))

            delete_query4 = "DELETE FROM food_item WHERE food_id = %s"
            mycursor.execute(delete_query4, (food_id,))

            db.commit()

            if mycursor.rowcount == 0:
                print("No food item found with that ID.")
            else:
                print("Food item and related records deleted successfully!")

        elif choice == '2':
            menu()
    except Exception as e:
        print("An error occurred:", e)
        db.rollback()

def search_food_item(): #browse food items from food establishments
    try:
        # ask for the establishment ID first
        establishment_id = int(input("Enter the establishment ID: "))

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
        # ask for the establishment ID first
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

        mycursor.execute("SELECT food_id, food_name, price FROM food_item WHERE establishment_id = %s", (establishment_id,))
        results = mycursor.fetchall()
        if results:
            print("Existing Food Items:")
            for food_id, food_name, price in results:
                print(f"ID: {food_id}, Name: {food_name}, Price: {price}")
        else:
            print("No food items found for this establishment.")
            return

        food_id = int(input("Enter the ID of the food item to update: "))

        # New details for the food item
        new_name = input("Enter the new name of the food item: ")
        new_price = float(input("Enter the new price of the food item: "))

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

#REPORTS TO BE GENERATED
def show_establishments():  #View all food establishments
    try:
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

def view_all_food_reviews():    #View all food reviews for an establishment or a food item
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

def view_all_food_items():  #View all food items from an establishment
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

        establishment_id = input("Enter the ID of the establishment: ")

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

def view_all_food_items_by_type():  #View all food items from an establishment that belong to a food type
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

        establishment_id = input("Enter the ID of the establishment: ")

        food_type = input("Enter the food type (Vegetable, Meat, Seafood, Pasta): ")

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

def view_reviews_within_month():    #View all reviews made within a month for an establishment or a food item
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

def view_high_rated_establishments():   #View all establishments with a high average rating (>=4)
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


def view_food_items_by_price(): #View all food items from an establishment arranged according to price
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

def search_food_items_by_price_and_type():  #Search food items from any establishment based on a given price range and/or food type
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

def foodReview(user_id, isAdmin):   #food review menu page
    if isAdmin:
        print("""
        1. Delete an existing Food review
        2. Delete an existing Establishment review
        3. Back
        """)
        choice = input("Enter your choice: ")
    
        if choice == '1':
            delete_food_review(user_id, isAdmin)
        elif choice == '2':
            delete_estab_review(user_id)
        elif choice == '3':
            menu
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    else:
        print("""
        1. Review a Food item
        2. Update an existing Food review
        3. Delete an existing Food review
        4. Back
        """)
        choice = input("Enter your choice: ")
    
        if choice == '1':
            add_food_review(user_id)
        elif choice == '2':
            update_food_review(user_id)
        elif choice == '3':
            delete_food_review(user_id, isAdmin)
        elif choice == '4':
            menu
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")



def foodEstablishment(user_id, isAdmin):    #food establishment menu page
    if isAdmin:
        print("""
        1. Add a Food Establishment
        2. Search a Food Establishment 
        3. Update an existing Food Establishment
        4. Delete an existing Food Establishment
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
    else:
        print("""
        1. Review a Food Establishment
        2. Update an existing Establishment review
        3. Delete an existing Establishment review
        4. Search a Food Establishment
        5. Back
        """)
        choice = input("Enter your choice: ")

        if choice == '1':
            add_estab_review(user_id)
        elif choice == '2':
            update_estab_review(user_id)
        elif choice == '3':
            delete_estab_review(user_id) 
        elif choice == '4':
            search_food_establishment()    
        elif choice == '5':
            menu    

def foodItem(isAdmin):  #food item menu page
    if isAdmin:
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
    else:
        print("""
        1. Search a Food item
        2. Back
        """)
        choice = input("Enter your choice: ")

        if choice == '1':
            search_food_item()
        elif choice == '2':
            menu
        


def reports():  #reports menu page
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

def manageUsers():  #manage users menu page
    print("""
    1. View All Users
    2. Remove an existing User (Only Regular Users)
    3. Back
    """)
    choice = input("Enter your choice: ")

    if choice == '1':
        view_all_users()
    elif choice == '2':
        delete_user()
    elif choice == '3':
        menu
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

def menu(): #main menu page for both admin and regular
    if isAdmin:
        while True:
            print("""
-----ADMIN HOMEPAGE-----
1. Food review
2. Food establishment
3. Food item
4. General Reports
5. Manage Users
6. Exit
------------------------
""")
            choice = input("Enter your choice: ")

            if choice == '1':
                foodReview(user_id, isAdmin)
            elif choice == '2':
                foodEstablishment(user_id, isAdmin)
            elif choice == '3':
                foodItem(isAdmin)
            elif choice == '4':
                reports()
            elif choice == '5':
                manageUsers()
            elif choice == '6':
                exit()
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
    else:
        while True:
            print("""
--------HOMEPAGE--------
1. Food review
2. Food establishment
3. Food item
4. General Reports
5. Exit
------------------------
            """)
            choice = input("Enter your choice: ")

            if choice == '1':
                foodReview(user_id, isAdmin)
            elif choice == '2':
                foodEstablishment(user_id, isAdmin)
            elif choice == '3':
                foodItem(isAdmin)
            elif choice == '4':
                reports()
            elif choice == '5':
                exit()
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":  #main
    while True:
        print("Welcome to KRIMSTIX")
        print("1. Sign Up as Regular")
        print("2. Sign Up as Admin")
        print("3. Log In")
        print("4. Exit")
        
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            sign_upReg()
        elif choice == '2':
            sign_upAdmin()
        elif choice == '3':
            user_id, isAdmin = login()
            if user_id:
                menu()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")