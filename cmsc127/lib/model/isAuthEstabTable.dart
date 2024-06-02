final String isAuthEstabTable = 'isAuthEstab';

class isAuthEstabFields {
  static final String eid = '_eid';
  static final String uid = '_uid';
}

class isAuthEstab{
  final int? eid;
  final int uid;


  const isAuthEstab({
    this.eid,
    required this.uid,
  });

    Map<String, Object?> toJson() => {
    isAuthEstabFields.eid: eid,
    isAuthEstabFields.uid: uid,
  }; 
}