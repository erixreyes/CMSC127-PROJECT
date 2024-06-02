final String isManagedTable = 'isManaged';

class isManagedFields {
  static final String rid = '_rid';
  static final String uid = '_uid';
}

class isManaged{
  final int? rid;
  final int uid;


  const isManaged({
    this.rid,
    required this.uid,
  });

    Map<String, Object?> toJson() => {
    isManagedFields.rid: rid,
    isManagedFields.uid: uid,
  }; 
}