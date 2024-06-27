import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/course.dart';

class ApiService {
  final String baseUrl = "http://127.0.0.2:8000/api/auth/";

  Future<void> login(String username, String password) async {
    try {
      final response = await http
          .post(
            Uri.parse(baseUrl + 'login/'),
            headers: <String, String>{
              'Content-Type': 'application/json; charset=UTF-8',
            },
            body: jsonEncode({
              'username': username,
              'password': password,
            }),
          )
          .timeout(Duration(seconds: 30)); // Adjust timeout duration as needed

      if (response.statusCode == 200) {
        // Handle successful login
        print('Login successful');
      } else {
        // Handle non-200 status codes
        throw 'Login failed: ${response.statusCode}';
      }
    } on TimeoutException catch (e) {
      throw 'Timeout during login: $e';
    } catch (error) {
      throw 'Error during login: $error';
    }
  }

  Future<void> register(String username, String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl + 'register/'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'username': username,
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 201) {
        // Handle successful registration
        print('Registration successful');
      } else {
        // Handle non-201 status codes
        throw 'Registration failed: ${response.statusCode}';
      }
    } catch (error) {
      throw 'Error during registration: $error';
    }
  }

  Future<List<Course>> getCourses() async {
    final response = await http.get(Uri.parse(baseUrl + 'courses/'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((course) => Course.fromJson(course)).toList();
    } else {
      throw Exception('Failed to load courses');
    }
  }

  Future<Course> createCourse(String title, String description) async {
    final response = await http.post(
      Uri.parse(baseUrl + 'courses/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'title': title,
        'description': description,
      }),
    );
    if (response.statusCode == 201) {
      return Course.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to create course');
    }
  }
}
