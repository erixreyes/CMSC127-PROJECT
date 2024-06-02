final String foodReviewTable = 'foodReview';

class FoodReviewFields {
  static final List<String> values = [
    id, date, rating, review, uid, fid, eid
  ];

  static final String id = '_id';
  static final String date = 'date';
  static final String rating = 'rating';
  static final String review = 'review';
  static final String uid = 'uid';
  static final String fid = 'fid';
  static final String eid = 'eid';
}

class FoodReview {
  final int? id;
  final DateTime date;
  final int rating;
  final String review;
  final int uid;
  final int fid;
  final int eid;

  const FoodReview({
    this.id,
    required this.date,
    required this.rating,
    required this.review,
    required this.uid,
    required this.fid,
    required this.eid,
  });

  FoodReview copy({
    int? id,
    DateTime? date,
    int? rating,
    String? review,
    int? uid,
    int? fid,
    int? eid,
  }) => FoodReview (
      id: id ?? this.id,
      date: date ?? this.date,
      rating: rating ?? this.rating,
      review: review ?? this.review,
      uid: uid ?? this.uid,
      fid: fid ?? this.fid,
      eid: eid ?? this.eid,
    );

    static FoodReview fromJson(Map<String, Object?> json) => FoodReview(
    id: json[FoodReviewFields.id] as int?,
    date: DateTime.parse(json[FoodReviewFields.date] as String),
    rating: json[FoodReviewFields.rating] as int,
    review: json[FoodReviewFields.review] as String,
    uid: json[FoodReviewFields.uid] as int,
    fid: json[FoodReviewFields.fid] as int,
    eid: json[FoodReviewFields.eid] as int,
  );

  Map<String, Object?> toJson() => {
    FoodReviewFields.id: id,
    FoodReviewFields.date: date.toIso8601String(),
    FoodReviewFields.rating: rating,
    FoodReviewFields.review: review,
    FoodReviewFields.uid: uid,
    FoodReviewFields.fid: fid,
    FoodReviewFields.eid: eid,
  }; 
}