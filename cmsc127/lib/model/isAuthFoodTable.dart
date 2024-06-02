final String isAuthFoodTable = 'isAuthFood';

class isAuthFoodFields {
  static final String uid = '_uid';
  static final String fid = '_fid';
}

class isAuthFood{
  final int? uid;
  final int fid;


  const isAuthFood({
    this.uid,
    required this.fid,
  });

    Map<String, Object?> toJson() => {
    isAuthFoodFields.uid: uid,
    isAuthFoodFields.fid: fid,
  }; 
}