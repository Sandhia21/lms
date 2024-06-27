import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';

class AuthService {
  static AuthProvider of(BuildContext context, {bool listen = false}) =>
      Provider.of<AuthProvider>(context, listen: listen);

  static Future<void> login(
      BuildContext context, String username, String password) async {
    await of(context, listen: false).login(username, password);
  }

  static Future<void> register(BuildContext context, String username,
      String email, String password) async {
    await of(context, listen: false).register(username, email, password);
  }

  static Future<void> logout(BuildContext context) async {
    await of(context, listen: false).logout();
  }
}
