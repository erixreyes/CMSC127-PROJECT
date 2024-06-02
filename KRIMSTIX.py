import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "", #password niyo
    database = "testdatabase"
    )

mycursor = db.cursor()

UserTable = "CREATE TABLE user (user_id INT(5) PRIMARY KEY, real_name VARCHAR(70), username VARCHAR(20), password VARCHAR(15), isAdmin BOOLEAN, isRegular BOOLEAN)"
#user TABLE
FoodEstabTable = "CREATE TABLE food_establishment (establishment_id INT(5) PRIMARY KEY, establishment_name VARCHAR(50), location VARCHAR(100), average_rating DECIMAL(3,1))"
#food_establishment TABLE
FoodItemTable = "CREATE TABLE food_item (food_id INT(5) PRIMARY KEY, food_name VARCHAR(50), price DECIMAL(5,2) NOT NULL, establishment_id INT(5), FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#food_item TABLE
FoodType = "CREATE TABLE food_item_food_type (food_type VARCHAR(15), food_id INT(5), PRIMARY KEY (food_type, food_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id))"
#food_item_food_type TABLE
FoodReview = "CREATE TABLE food_review (review_id INT(5) PRIMARY KEY AUTO_INCREMENT, Date DATE DEFAULT CURRENT_DATE, Rating INT(1), Review VARCHAR(100), user_id INT(5), food_id INT(5), establishment_id INT(5), FOREIGN KEY (User_id) REFERENCES user(user_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id),FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#food_review TABLE
EstabReview = "CREATE TABLE establishment_review (review_id INT(5) PRIMARY KEY AUTO_INCREMENT, Date DATE DEFAULT CURRENT_DATE, Rating INT(1), Review VARCHAR(100), User_id INT(5), establishment_id INT(5), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (establishment_id) REFERENCES food_establishment(establishment_id))"
#establishment_review TABLE
IsManagedByTable = "CREATE TABLE is_managed_by (review_id INT(5), user_id INT(5), FOREIGN KEY (review_id) REFERENCES food_review(review_id), FOREIGN KEY (user_id) REFERENCES user(user_id))"
#is_authorized_food TABLE
IsAuthorizedFoodTable = "CREATE TABLE is_authorized_food (user_id INT(5), food_id INT(5), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (food_id) REFERENCES food_item(food_id))"
#is_authorized_establishment TABLE
IsAuthorizedEstabTable = "CREATE TABLE is_authorized_establishment (food_id INT(5), user_id INT(5), FOREIGN KEY (food_id) REFERENCES food_item(food_id), FOREIGN KEY (user_id) REFERENCES user(user_id))"

mycursor.execute(UserTable)
mycursor.execute(FoodEstabTable)
mycursor.execute(FoodItemTable)
mycursor.execute(FoodType)
mycursor.execute(FoodReview)
mycursor.execute(EstabReview)
mycursor.execute(IsManagedByTable)
mycursor.execute(IsAuthorizedFoodTable)
mycursor.execute(IsAuthorizedEstabTable)

for(x) in mycursor:
    print(x)