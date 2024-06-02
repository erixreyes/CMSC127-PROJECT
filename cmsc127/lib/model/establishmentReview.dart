final String estabReviewTable = 'estabReview';

class EstabReviewFields {
  static final List<String> values = [
    id, date, rating, review, uid, eid
  ];
  
  static final String id = '_id';
  static final String date = 'date';
  static final String rating = 'rating';
  static final String review = 'review';
  static final String uid = 'uid';
  static final String eid = 'eid';
}

class EstabReview {
  final int? id;
  final DateTime date;
  final int rating;
  final String review;
  final int uid;
  final int eid;

  const EstabReview({
    this.id,
    required this.date,
    required this.rating,
    required this.review,
    required this.uid,
    required this.eid,
  });

  EstabReview copy({
    int? id,
    DateTime? date,
    int? rating,
    String? review,
    int? uid,
    int? eid,

  }) => EstabReview (
      id: id ?? this.id,
      date: date ?? this.date,
      rating: rating ?? this.rating,
      review: review ?? this.review,
      uid: uid ?? this.uid,
      eid: eid ?? this.eid,
    );

  static EstabReview fromJson(Map<String, Object?> json) => EstabReview(
    id: json[EstabReviewFields.id] as int?,
    date: DateTime.parse(json[EstabReviewFields.date] as String),
    rating: json[EstabReviewFields.rating] as int,
    review: json[EstabReviewFields.review] as String,
    uid: json[EstabReviewFields.uid] as int,
    eid: json[EstabReviewFields.eid] as int,
  );

    Map<String, Object?> toJson() => {
    EstabReviewFields.id: id,
    EstabReviewFields.date: date.toIso8601String(),
    EstabReviewFields.rating: rating,
    EstabReviewFields.review: review,
    EstabReviewFields.uid: uid,
    EstabReviewFields.eid: eid,
  }; 
}