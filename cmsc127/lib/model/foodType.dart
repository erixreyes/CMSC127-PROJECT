final String foodTypeTable = 'foodType';

class FoodTypeFields {
  static final String id = '_id';
  static final String foodType = 'foodType';

}

class FoodType {
  final int? id;
  final String foodType;


  const FoodType({
    this.id,
    required this.foodType,
  });

    Map<String, Object?> toJson() => {
    FoodTypeFields.id: id,
    FoodTypeFields.foodType: foodType,
  }; 
}