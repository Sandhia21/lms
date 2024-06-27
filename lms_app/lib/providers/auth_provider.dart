import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../models/user.dart';

class AuthProvider with ChangeNotifier {
  final String baseUrl = "http://10.0.2.2:8000/api/";

  User? _loggedInUser;

  User? get loggedInUser => _loggedInUser;

  Future<void> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl + 'auth/login/'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        // Parse the response JSON to extract user details
        final userJson = jsonDecode(response.body);
        _loggedInUser = User.fromJson(userJson);

        // Notify listeners that authentication was successful
        notifyListeners();
      } else {
        throw 'Login failed: ${response.statusCode}';
      }
    } catch (error) {
      throw 'Login failed: $error';
    }
  }

  Future<void> register(String username, String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl + 'auth/registration/'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'username': username,
          'email': email,
          'password1': password,
          'password2': password,
        }),
      );

      if (response.statusCode == 201) {
        // Registration successful, login the user
        await login(username, password);
      } else {
        throw 'Registration failed: ${response.statusCode}';
      }
    } catch (error) {
      throw 'Registration failed: $error';
    }
  }

  Future<void> logout() async {
    // Implement logout logic here if needed
    _loggedInUser = null;
    notifyListeners();
  }
}
