# Online Judge Platform

An interactive platform for educators and students to create, manage, and solve programming problems with AI-powered code reviews.

**Last Updated**: June 10, 2025

## 🚀 Features

### 👩🏫 Teacher Profile
- **Problem Management**: Create/remove programming challenges
- **Code Validation**: Test solutions with manual inputs
- **AI Review System**: Automated code analysis on submissions
- **Submission System**: Verify solution correctness through test cases
- **Dual Mode**: Function as both compiler and assessment tool

### 🧑🎓 Student Profile
- **Problem Access**: Solve teacher-posted challenges
- **Interactive IDE**: Built-in code editor with compilation
- **Smart Feedback**: Instant AI analysis on submissions
- **Progress Tracking**: View submission history and results


##  High-Level Architecture


- **Frontend**: Django templates with HTML/CSS/Bootstrap (or React)
- **Backend**: Django Views, Models, and Forms


---

##  Core Modules

| Module             | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Authentication     | User registration, login, and role-based access (Student, Teacher)          |
| Problem Management | Teachers can add, edit, or delete problems with test cases                  |
| Code Submission    | Students can submit code for problems and get real-time verdicts            |
| Results Feedback   | Verdict: "Correct", "Wrong Answer", "Runtime Error", etc.                   |




##  Tech Stack

| Layer      | Technology                      |
|------------|----------------------------------|
| Language   | Python                          |
| Framework  | Django                          |
| Database   |                                 |
| Frontend   | HTML, CSS                       |
| Judge Engine | Python subprocess             |
| Authentication | Django's built-in auth system |

