final String userTable = 'users';

class UserFields {
  static final List<String> values = [
    id, realName, userName, password, isAdmin
  ];
  
  static final String id = '_id';
  static final String realName = 'realName';
  static final String userName = 'userName';
  static final String password = 'password';
  static final String isAdmin = 'isAdmin';
}

class User {
  final int? id;
  final String realName;
  final String userName;
  final String password;
  final bool isAdmin;

  const User({
    this.id,
    required this.realName,
    required this.userName,
    required this.password,
    required this.isAdmin,
  });

  User copy({
    int? id,
    String? realName,
    String? userName,
    String? password,
    bool? isAdmin,
  }) => User (
      id: id ?? this.id,
      realName: realName ?? this.realName,
      userName: userName ?? this.userName,
      password: password ?? this.password,
      isAdmin: isAdmin ?? this.isAdmin,
    );

  static User fromJson(Map<String, Object?> json) => User(
    id: json[UserFields.id] as int?,
    realName: json[UserFields.realName] as String,
    userName: json[UserFields.userName] as String,
    password: json[UserFields.password] as String,
    isAdmin: json[UserFields.isAdmin] == 0,
  );

  Map<String, Object?> toJson() => {
    UserFields.id: id,
    UserFields.realName: realName,
    UserFields.userName: userName,
    UserFields.password: password,
    UserFields.isAdmin: isAdmin ? 1 : 0,
  }; 
}