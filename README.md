## 🎓 student-facial-attendance
This web application automates student attendance using facial recognition, providing secure login and tailored access for both students and teachers.

---

### 🔍 Features Overview

#### 👨‍🎓 Student Side:

* **Registration & Login**
  Students can create an account by entering their details and uploading a reference face image. They can later log in using their credentials.

* **Class Filtering by Major**
  Upon login, students only see classes that belong to their **own major** via a dropdown menu.

* **Face Recognition Attendance**
  Students can mark their presence by capturing a live image with their webcam, which is matched with their registration image.

* **Attendance History **
  Students can view a **record of all the classes they were present in**.

* **Profile Management**
  Students can access and **update their personal information**.

---

#### 👩‍🏫 Teacher Side:

* **Secure Admin-Only Account Creation**
  Teachers cannot register themselves. Accounts are provided by the admin only for added security.

* **Class Filtering**
  Teachers only see **classes assigned to them**.

* **View Attendance by Date**
  Teachers can select a class and **view the list of students present**, with the ability to **filter records by date**.

* **Profile Management**
  Teachers can also **update their personal info** through the dashboard.

---

### 🔒 Security

* Hashed password storage for both students and teachers.
* UUIDs used as unique identifiers for students.
* Role-based access control for students and teachers.

### To test :

MyProject = backend Django

Frontend = Html , CSS , JS

The student creates an account and marks his presence in a certain class or all the classes then the teacher logs in :
email : souzi@gmail.com 
password :  123

then selects a class he was assigned to in order to see the presence
