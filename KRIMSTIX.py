import mysql.connector
from mysql.connector import Error

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "" #password niyo,
    database = "testdatabase"
    )

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS testdatabase")
mycursor.execute("USE testdatabase")

UserTable = """
CREATE TABLE IF NOT EXISTS user (
    user_id INT(5) PRIMARY KEY,
    real_name VARCHAR(70),
    username VARCHAR(20),
    password VARCHAR(15),
    isAdmin BOOLEAN,
    isRegular BOOLEAN
)"""
#user TABLE
FoodEstabTable = "CREATE TABLE IF NOT EXISTS food_establishment (establishment_id INT(5) PRIMARY KEY, establishment_name VARCHAR(50), location VARCHAR(100), average_rating DECIMAL(3,1))"
#food_establishment TABLE
FoodItemTable = "CREATE TABLE IF NOT EXISTS food_item (food_id INT(5) PRIMARY KEY, food_name VARCHAR(50), price DECIMAL(5,2) NOT NULL, establishment_id INT(5), FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#food_item TABLE
FoodType = "CREATE TABLE IF NOT EXISTS food_item_food_type (food_type VARCHAR(15), food_id INT(5), PRIMARY KEY (food_type, food_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id))"
#food_item_food_type TABLE
FoodReview = "CREATE TABLE IF NOT EXISTS food_review (review_id INT(5) PRIMARY KEY AUTO_INCREMENT, Date DATE DEFAULT CURRENT_DATE, Rating INT(1), Review VARCHAR(100), user_id INT(5), food_id INT(5), establishment_id INT(5), FOREIGN KEY (User_id) REFERENCES user(user_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id),FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#food_review TABLE
EstabReview = "CREATE TABLE IF NOT EXISTS establishment_review (review_id INT(5) PRIMARY KEY AUTO_INCREMENT, Date DATE DEFAULT CURRENT_DATE, Rating INT(1), Review VARCHAR(100), User_id INT(5), establishment_id INT(5), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#establishment_review TABLE
IsManagedByTable = "CREATE IF NOT EXISTS TABLE is_managed_by (review_id INT(5), user_id INT(5), FOREIGN KEY (review_id) REFERENCES food_review(review_id), FOREIGN KEY (user_id) REFERENCES user(user_id))"
#is_authorized_food TABLE
IsAuthorizedFoodTable = "CREATE TABLE IF NOT EXISTS is_authorized_food (user_id INT(5), food_id INT(5), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id))"
#is_authorized_establishment TABLE
IsAuthorizedEstabTable = "CREATE TABLE IF NOT EXISTS is_authorized_establishment (food_id INT(5), user_id INT(5), FOREIGN KEY (food_id) REFERENCES food_item(food_id), FOREIGN KEY (user_id) REFERENCES user(user_id))"

menu_options = "SELECT food_name from FoodItemTable"


def add_food_review():
    # The SQL command to select food names from the food_item table
    # Ensure the table name matches your database schema
    query = "SELECT food_name FROM food_item"
    
    try:
        # Execute the query
        mycursor.execute(query)
        
        # Fetch all the results
        results = mycursor.fetchall()
        
        # Check if results were found
        if results:
            print("Available Food Items:")
            for (food_name,) in results:
                print(food_name)
        else:
            print("No food items found.")
        
        # Additional code to handle adding a food review
        # You might need user input here to choose a food item and input their review
        food_name = input("Enter the food name to review: ")
        user_id = input("Enter your user ID: ")
        review = input("Enter your review: ")
        rating = int(input("Enter your rating (1-5): "))
        
        # SQL command to insert a new review into the food_review table
        # Assumes your table and columns are set up to accept these values
        add_review_query = """
        INSERT INTO food_review (Date, Rating, Review, user_id, food_id)
        VALUES (CURDATE(), %s, %s, %s, (SELECT food_id FROM food_item WHERE food_name = %s))
        """
        mycursor.execute(add_review_query, (rating, review, user_id, food_name))
        db.commit()  # Make sure to commit the changes to the database
        
        print("Review added successfully!")

    except Exception as e:
        print("An error occurred:", e)
        db.rollback()  # Rollback in case of any error


def update_food_review():
    try:
        # Ask the user for their user ID
        user_id = input("Enter your user ID to find your reviews: ")
        
        # Fetch reviews made by the user
        mycursor.execute("SELECT review_id, food_id, Review, Rating FROM food_review WHERE user_id = %s", (user_id,))
        reviews = mycursor.fetchall()
        
        # Display the reviews
        if reviews:
            print("Your Reviews:")
            for review_id, food_id, review, rating in reviews:
                print(f"Review ID: {review_id}, Food ID: {food_id}, Review: {review}, Rating: {rating}")
        else:
            print("No reviews found for this user.")
            return
        
        # Ask the user to choose a review by review_id to update
        review_id = input("Enter the Review ID you want to update: ")
        
        # Fetch and display the current review details
        mycursor.execute("SELECT Review, Rating FROM food_review WHERE review_id = %s", (review_id,))
        review_details = mycursor.fetchone()
        if review_details:
            print(f"Current Review: {review_details[0]}, Current Rating: {review_details[1]}")
        else:
            print("Review ID not found.")
            return
        
        # User inputs for updating the review
        new_review = input("Enter your new review: ")
        new_rating = int(input("Enter your new rating (1-5): "))
        
        # SQL command to update the review
        update_query = """
        UPDATE food_review
        SET Rating = %s, Review = %s
        WHERE review_id = %s
        """
        mycursor.execute(update_query, (new_rating, new_review, review_id))
        db.commit()  # Commit the changes to the database
        
        print("Review updated successfully!")

    except Exception as e:
        print("An error occurred:", e)
        db.rollback()  # Rollback in case of any error


def delete_food_review():
    print("Deleting a food review...")
    # Add implementation code here

def add_food_establishment():
    print("Adding a food establishment...")
    # Add implementation code here

def delete_food_establishment():
    print("Deleting a food establishment...")
    # Add implementation code here

def search_food_establishment():
    print("Searching for a food establishment...")
    # Add implementation code here

def update_food_establishment():
    print("Updating a food establishment...")
    # Add implementation code here

def add_food_item():
    print("Adding a food item...")
    # Add implementation code here

def delete_food_item():
    print("Deleting a food item...")
    # Add implementation code here

def search_food_item():
    print("Searching for a food item...")
    # Add implementation code here

def update_food_item():
    print("Updating a food item...")
    # Add implementation code here

def exit_program():
    print("Exiting program...")
    exit()

def default():
    print("Invalid option. Please choose again!")

menu_options = {
    1: add_food_review,
    2: update_food_review,
    3: delete_food_review,
    4: add_food_establishment,
    5: delete_food_establishment,
    6: search_food_establishment,
    7: update_food_establishment,
    8: add_food_item,
    9: delete_food_item,
    10: search_food_item,
    11: update_food_item,
    12: exit_program
}

menu_options = {
    1: add_food_review,
    2: update_food_review,
    3: delete_food_review,
    4: add_food_establishment,
    5: delete_food_establishment,
    6: search_food_establishment,
    7: update_food_establishment,
    8: add_food_item,
    9: delete_food_item,
    10: search_food_item,
    11: update_food_item,
    12: exit_program
}

def menu():
    print("""
    1. Add a food review
    2. Update a food review
    3. Delete a food review
    4. Add a food establishment
    5. Delete a food establishment
    6. Search for a food establishment
    7. Update a food establishment
    8. Add a food item
    9. Delete a food item
    10. Search for a food item
    11. Update a food item
    12. Exit
    """)
    choice = input("Enter your choice: ")
    return int(choice)

if __name__ == "__main__":
    while True:
        option = menu()
        menu_options.get(option, default)()
