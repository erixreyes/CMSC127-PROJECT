final String foodTable = 'food';

class FoodFields {
  static final List<String> values = [
    id, foodName, price, estabID
  ];

  static final String id = '_id';
  static final String foodName = 'foodName';
  static final String price = 'price';
  static final String estabID = 'estabID';
}

class Food {
  final int? id;
  final String foodName;
  final double price;
  final String estabID;

  const Food({
    this.id,
    required this.foodName,
    required this.price,
    required this.estabID,
  });

  Food copy({
    int? id,
    String? foodName,
    double? price,
    String? estabID,
  }) => Food (
      id: id ?? this.id,
      foodName: foodName ?? this.foodName,
      price: price ?? this.price,
      estabID: estabID ?? this.estabID,
    );

  static Food fromJson(Map<String, Object?> json) => Food(
    id: json[FoodFields.id] as int?,
    foodName: json[FoodFields.foodName] as String,
    price: json[FoodFields.price] as double,
    estabID: json[FoodFields.estabID] as String,
  );

  Map<String, Object?> toJson() => {
    FoodFields.id: id,
    FoodFields.foodName: foodName,
    FoodFields.price: price,
    FoodFields.estabID: estabID,
  }; 
}