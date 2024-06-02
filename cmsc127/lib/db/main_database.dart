import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

// TABLES (MODELS)
import 'package:cmsc127/model/user.dart';
import 'package:cmsc127/model/establishment.dart';
import 'package:cmsc127/model/food.dart';
import 'package:cmsc127/model/foodType.dart';
import 'package:cmsc127/model/foodReview.dart';
import 'package:cmsc127/model/establishmentReview.dart';
import 'package:cmsc127/model/isManaged.dart';
import 'package:cmsc127/model/isAuthEstabTable.dart';
import 'package:cmsc127/model/isAuthFoodTable.dart';

class MainDatabase {
  static final MainDatabase instance = MainDatabase._init();

  static Database? _database;

  MainDatabase._init();

  Future<Database> get database async {
    if (_database != null ) return  _database!;

    _database = await _initDB('main.db');
    return _database!;
  }

  
  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  Future _createDB(Database db, int version) async {
    final idType = 'INTEGER PRIMARY KEY AUTOINCREMENT';
    final boolType = 'BOOLEAN NOT NULL';
    final stringType = 'TEXT NOT NULL';
    final intType = 'INTEGER NOT NULL';
    final doubleType = 'DOUBLE NOT NULL';

    // users
    await db.execute(''' 
    CREATE TABLE $userTable (
      ${UserFields.id} $idType,
      ${UserFields.realName} $stringType,
      ${UserFields.userName} $stringType,
      ${UserFields.password} $stringType,
      ${UserFields.isAdmin} $boolType,
    )
    ''');

    // establishments
    await db.execute(''' 
    CREATE TABLE $estabTable (
      ${EstabFields.id} $idType,
      ${EstabFields.estabName} $stringType,
      ${EstabFields.loc} $stringType,
      ${EstabFields.avgRating} $doubleType,
    )
    ''');

    // food
    await db.execute(''' 
    CREATE TABLE $foodTable (
      ${FoodFields.id} $idType,
      ${FoodFields.foodName} $stringType,
      ${FoodFields.price} $intType,
      FOREIGN KEY (${FoodFields.estabID}) REFERENCES $estabTable(${EstabFields.id})
    )
    ''');

    await db.execute(''' 
    CREATE TABLE $foodTypeTable (
      FOREIGN KEY (${FoodTypeFields.id}) REFERENCES $foodTable(${FoodFields.id}),
      ${FoodTypeFields.foodType} $stringType,
    )
    ''');

    await db.execute(''' 
    CREATE TABLE $foodReviewTable (
      ${FoodReviewFields.id} $idType,
      ${FoodReviewFields.date} TEXT DEFAULT CURRENT_DATE,
      ${FoodReviewFields.rating} $intType,
      ${FoodReviewFields.review} $stringType,
      FOREIGN KEY (${FoodReviewFields.uid}) REFERENCES $userTable(${UserFields.id}),
      FOREIGN KEY (${FoodReviewFields.fid}) REFERENCES $foodTable(${FoodFields.id}),
      FOREIGN KEY (${FoodReviewFields.eid}) REFERENCES $estabTable(${EstabFields.id}),
    )
    ''');

    await db.execute(''' 
    CREATE TABLE $estabReviewTable (
      ${EstabReviewFields.id} $idType,
      ${EstabReviewFields.date} TEXT DEFAULT CURRENT_DATE,
      ${EstabReviewFields.rating} $intType,
      ${EstabReviewFields.review} $stringType,
      FOREIGN KEY (${EstabReviewFields.uid}) REFERENCES $userTable(${UserFields.id}),
      FOREIGN KEY (${EstabReviewFields.eid}) REFERENCES $estabTable(${EstabFields.id}),
    )
    ''');

    await db.execute(''' 
    CREATE TABLE $isManagedTable (
      FOREIGN KEY (${isManagedFields.rid}) REFERENCES $estabReviewTable(${EstabReviewFields.id}) ON DELETE CASCADE,
      FOREIGN KEY (${isManagedFields.rid}) REFERENCES $foodReviewTable(${FoodReviewFields.id}) ON DELETE CASCADE,
      FOREIGN KEY (${isManagedFields.uid}) REFERENCES $userTable(${UserFields.id}),
    )
    ''');

    await db.execute(''' 
    CREATE TABLE $isAuthFoodTable (
      FOREIGN KEY (${isAuthFoodFields.uid})) REFERENCES $userTable(${UserFields.id}),
      FOREIGN KEY (${isAuthFoodFields.fid})) REFERENCES $foodTable(${FoodFields.id}),
    )
    ''');

    await db.execute(''' 
    CREATE TABLE $isAuthEstabTable (
      FOREIGN KEY (${isAuthEstabFields.eid})) REFERENCES $estabTable(${EstabFields.id}),
      FOREIGN KEY (${isAuthEstabFields.uid})) REFERENCES $userTable(${UserFields.id}),
    )
    ''');
  }


  // CREATE
  Future<User> createUser(User user) async {
    final db = await instance.database;

    final id = await db.insert(userTable, user.toJson());
    return user.copy(id: id);
  }

  Future<Food> createFood(Food food) async {
    final db = await instance.database;

    final id = await db.insert(foodTable, food.toJson());
    return food.copy(id: id);
  }

  Future<FoodReview> createFoodReview(FoodReview fReview) async {
    final db = await instance.database;

    final id = await db.insert(foodReviewTable, fReview.toJson());
    return fReview.copy(id: id);
  }

  Future<Estab> createEstab (Estab estab) async {
    final db = await instance.database;

    final id = await db.insert(estabTable, estab.toJson());
    return estab.copy(id: id);
  }

  Future<EstabReview> createEstabReview (EstabReview eReview) async {
    final db = await instance.database;

    final id = await db.insert(estabReviewTable, eReview.toJson());
    return eReview.copy(id: id);
  }

  // specific read

  Future<User> viewUser(int id) async {
    final db = await instance.database;

    final maps = await db.query(
      userTable,
      columns: UserFields.values,
      where: '${UserFields.id} = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty){
      return User.fromJson(maps.first);
    } else {
      throw Exception('ID $id does not exist');
    }
  }

  Future<Food> viewFood(int id) async {
    final db = await instance.database;

    final maps = await db.query(
      foodTable,
      columns: FoodFields.values,
      where: '${FoodFields.id} = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty){
      return Food.fromJson(maps.first);
    } else {
      throw Exception('ID $id does not exist');
    }
  }

  Future<Estab> viewEstab(int id) async {
    final db = await instance.database;

    final maps = await db.query(
      estabTable,
      columns: EstabFields.values,
      where: '${EstabFields.id} = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty){
      return Estab.fromJson(maps.first);
    } else {
      throw Exception('ID $id does not exist');
    }
  }

  Future<EstabReview> viewEstabReview (int id) async {
    final db = await instance.database;

    final maps = await db.query(
      estabTable,
      columns: EstabReviewFields.values,
      where: '${EstabReviewFields.id} = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty){
      return EstabReview.fromJson(maps.first);
    } else {
      throw Exception('ID $id does not exist');
    }
  }

  Future<FoodReview> viewFoodReview (int id) async {
    final db = await instance.database;

    final maps = await db.query(
      estabTable,
      columns: FoodReviewFields.values,
      where: '${FoodReviewFields.id} = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty){
      return FoodReview.fromJson(maps.first);
    } else {
      throw Exception('ID $id does not exist');
    }
  }

  // view all

  Future<List<User>> viewAllUsers() async {
    final db = await instance.database;

    final result = await db.query(userTable, orderBy: '${UserFields.userName} ASC');
    return result.map((json) => User.fromJson(json)).toList();
  }

  Future<List<Food>> viewAllFoods() async {
    final db = await instance.database;

    final result = await db.query(foodTable, orderBy: '${FoodFields.foodName} ASC');
    return result.map((json) => Food.fromJson(json)).toList();
  }

  Future<List<FoodReview>> viewAllFoodReviews() async {
    final db = await instance.database;

    final result = await db.query(foodTable, orderBy: '${FoodReviewFields.eid} ASC');
    return result.map((json) => FoodReview.fromJson(json)).toList();
  }

  Future<List<Estab>> viewAllEstabs() async {
    final db = await instance.database;

    final result = await db.query(foodTable, orderBy: '${EstabFields.avgRating} ASC');
    return result.map((json) => Estab.fromJson(json)).toList();
  }

  Future<List<EstabReview>> viewAllEstabReviews() async {
    final db = await instance.database;

    final result = await db.query(foodTable, orderBy: '${EstabReviewFields.date} ASC');
    return result.map((json) => EstabReview.fromJson(json)).toList();
  }

  Future<List<dynamic>> viewAllReviews() async {
  final db = await instance.database;

  final foodResult = await db.query(foodReviewTable, orderBy: '${FoodReviewFields.eid} ASC');
  final foodReviews = foodResult.map((json) => FoodReview.fromJson(json)).toList();

  final estabResult = await db.query(estabReviewTable, orderBy: '${EstabReviewFields.date} ASC');
  final estabReviews = estabResult.map((json) => EstabReview.fromJson(json)).toList();

  final allReviews = [...estabReviews, ...foodReviews];

  return allReviews;
  }

  // update

  Future<int> updateFood(Food food) async {
    final db = await instance.database;

    return db.update(
      foodTable,
      food.toJson(),
      where: '${FoodFields.id} = ?',
      whereArgs: [food.id],
    );

  }

  Future<int> updateEstab(Estab estab) async {
    final db = await instance.database;

    return db.update(
      estabTable,
      estab.toJson(),
      where: '${EstabFields.id} = ?',
      whereArgs: [estab.id],
    );
    
  }

  Future<int> updateFoodReview(FoodReview foodReview) async {
    final db = await instance.database;

    return db.update(
      foodReviewTable,
      foodReview.toJson(),
      where: '${FoodReviewFields.id} = ?',
      whereArgs: [foodReview.id],
    );
    
  }

  Future<int> updateEstabReview(EstabReview estabReview) async {
    final db = await instance.database;

    return db.update(
      estabReviewTable,
      estabReview.toJson(),
      where: '${EstabReviewFields.id} = ?',
      whereArgs: [estabReview.id],
    );
  }

  // delete 

  Future<int> deleteUser(int id) async {
    final db = await instance.database;

    return await db.delete(
      userTable,
      where: '${UserFields.id} = ?',
      whereArgs: [id],
    );
  }

  Future<int> deleteFood(int id) async {
    final db = await instance.database;

    return await db.delete(
      foodTable,
      where: '${FoodFields.id} = ?',
      whereArgs: [id],
    );
  }

  Future<int> deleteFoodReview(int id) async {
    final db = await instance.database;

    return await db.delete(
      foodReviewTable,
      where: '${FoodReviewFields.id} = ?',
      whereArgs: [id],
    );
  }

  Future<int> deleteEstab(int id) async {
    final db = await instance.database;

    return await db.delete(
      estabTable,
      where: '${EstabFields.id} = ?',
      whereArgs: [id],
    );
  }

  Future<int> deleteEstabReview(int id) async {
    final db = await instance.database;

    return await db.delete(
      estabReviewTable,
      where: '${EstabReviewFields.id} = ?',
      whereArgs: [id],
    );
  }

  Future _close() async {
    final db = await instance.database;

    db.close();
  }

}