final String estabTable = 'estab';

class EstabFields {
  static final List<String> values = [
    id, estabName, loc, avgRating
  ];
  static final String id = '_id';
  static final String estabName = 'estabName';
  static final String loc = 'loc';
  static final String avgRating = 'avgRating';
}

class Estab {
  final int? id;
  final String estabName;
  final String loc;
  final double avgRating;

  const Estab({
    this.id,
    required this.estabName,
    required this.loc,
    required this.avgRating,
  });

  Estab copy({
    int? id,
    String? estabName,
    String? loc,
    double? avgRating,
  }) => Estab (
      id: id ?? this.id,
      estabName: estabName ?? this.estabName,
      loc: loc ?? this.loc,
      avgRating: avgRating ?? this.avgRating,
    );

  static Estab fromJson(Map<String, Object?> json) => Estab(
    id: json[EstabFields.id] as int?,
    estabName: json[EstabFields.estabName] as String,
    loc: json[EstabFields.loc] as String,
    avgRating: json[EstabFields.avgRating] as double,
  );

    Map<String, Object?> toJson() => {
    EstabFields.id: id,
    EstabFields.estabName: estabName,
    EstabFields.loc: loc,
    EstabFields.avgRating: avgRating,
  }; 
}