import sqlite3
# user class (base class)
class User:
    def __init__(self, username, password):
        #constructor
        self.username = username
        self.password = password
    def set_attributes(self, new_username, new_password):
        #method to change attributes
        self.username = new_username
        self.lastname = new_password
class Course:
    def __init__(self, course_CRN, course_TITLE, course_DEPARTMENT, course_INSTRUCTOR, course_PERIOD, course_SEMESTER, course_YEAR, course_CREDITS, course_CLASSLIST):
        self.course_CRN = course_CRN
        self.course_TITLE = course_TITLE
        self.course_DEPARTMENT = course_DEPARTMENT
        self.course_INSTRUCTOR = course_INSTRUCTOR
        self.course_PERIOD = course_PERIOD
        self.course_SEMESTER = course_SEMESTER
        self.course_YEAR = course_YEAR
        self.course_CREDITS = course_CREDITS
        self.course_CLASSLIST = course_CLASSLIST
class Student(User):
    def authenticate(self, username, password):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM STUDENTS WHERE USERNAME = ? AND PASSWORD = ?",  (username, password))
        # FETCH DATA FROM STUDENT
        student_data = cursor.fetchone()
        if student_data:
            student_id = student_data[0]
            student_name = student_data[1]
            self.user_type = "STUDENT"
            self.user_data = (student_id, student_name)
            return True
        return False
    def print_info(self, username, password):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM STUDENTS WHERE USERNAME = ? AND PASSWORD = ?",  (username, password))
        student_data = cursor.fetchone()
        
        if student_data:
            student_name = student_data[1]
            student_surname = student_data[2]
            print(f"Welcome Student {student_name} {student_surname}!")

        conn.close()
    def print_options(self):
        print("------------- OPTIONS ---------------")
        print("Enter 1 to search courses")
        print("Enter 2 to add a course to your schedule")
        print("Enter 3 to drop a course from your schedule")
        print("Enter 4 to print your schedule")
        print("Enter 0 to exit")
    def search_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        print("Enter 1 to search all courses")
        print("Enter 2 to search a specific course")
        parameter = str(input())

        if parameter == "1":
            print("Searching all courses...")
            cursor.execute("SELECT * FROM COURSES")

        if parameter == "2":
            course_CRN = input("Enter CRN: ")
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (course_CRN,))

        rows = cursor.fetchall()
        for row in rows:
            print(f"CRN: {row[0]}, TITLE: {row[1]}, DEPARTMENT: {row[2]}, INSTRUCTOR: {row[3]}, PERIOD: {row[4]}, SEMESTER: {row[5]}, YEAR: {row[6]}, CREDITS: {row[7]}")

        conn.close()
    def add_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        course_CRN = input("Enter CRN: ")
        cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (course_CRN,))

        rows = cursor.fetchall()

        for row in rows:
            cursor.execute("INSERT INTO SCHEDULE (CRN, TITLE, DEPARTMENT, INSTRUCTOR, PERIOD, SEMESTER, YEAR, CREDITS) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            conn.commit()
            print(f"{row[1]} added to your schedule!")

        conn.close()
    def drop_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        course_CRN = input("Enter CRN: ")

        cursor.execute("DELETE FROM SCHEDULE WHERE CRN = ?", (course_CRN,))

        conn.commit()
        print(f"Course removed from schedule!")
        conn.close()
    def print_schedule(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM SCHEDULE")
        rows = cursor.fetchall()

        for row in rows:
            print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}")

        conn.close()

class Instructor(User):
    def authenticate(self, username, password):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM INSTRUCTORS WHERE USERNAME = ? AND PASSWORD = ?",  (username, password))
        # FETCH DATA FOR INSTRUCTOR
        instructor_data = cursor.fetchone()
        if instructor_data:
            instructor_id = instructor_data[0]
            instructor_name = instructor_data[1]
            self.user_type = "INSTRUCTORS"
            self.user_data = (instructor_id, instructor_name)
            return True
        return False
    def print_info(self, username, password):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM INSTRUCTORS WHERE USERNAME = ? AND PASSWORD = ?",  (username, password))
        instructor_data = cursor.fetchone()
        
        if instructor_data:
            instructor_name = instructor_data[1]
            instructor_surname = instructor_data[2]
            print(f"Welcome Instructor {instructor_name} {instructor_surname}!")

        conn.close()
    def print_options(self):
        print("------------- OPTIONS ---------------")
        print("Enter 1 to search course")
        print("Enter 2 to print your schedule")
        print("Enter 3 to print classlist")
        print("Enter 0 to exit")
    def print_schedule(self, username, password):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT NAME, SURNAME FROM INSTRUCTORS WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
        
        # FETCH DATA FOR INSTRUCTOR
        instructor_data = cursor.fetchone()

        if instructor_data:
            instructor_name = instructor_data[0]
            instructor_surname = instructor_data[1]

        instructor_fullname = instructor_name + " " + instructor_surname

        cursor.execute("SELECT * FROM COURSES WHERE INSTRUCTOR = ?", (instructor_fullname,))
        rows = cursor.fetchall()

        for row in rows:
            print(f"CRN: {row[0]}, TITLE: {row[1]}, DEPARTMENT: {row[2]}, INSTRUCTOR: {row[3]}, PERIOD: {row[4]}, SEMESTER: {row[5]}, YEAR: {row[6]}, CREDITS: {row[7]}")

        conn.close()
    def print_classlist(self):
        # method to print class list
        print("Printing classlist...")
    def search_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        print("Enter 1 to search all courses")
        print("Enter 2 to search a specific course")
        parameter = str(input())

        if parameter == "1":
            print("Searching all courses...")
            cursor.execute("SELECT * FROM COURSES")

        if parameter == "2":
            course_CRN = input("Enter CRN: ")
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (course_CRN,))

        rows = cursor.fetchall()
        for row in rows:
            print(f"CRN: {row[0]}, TITLE: {row[1]}, DEPARTMENT: {row[2]}, INSTRUCTOR: {row[3]}, PERIOD: {row[4]}, SEMESTER: {row[5]}, YEAR: {row[6]}, CREDITS: {row[7]}")

        conn.close()

class Admin(User):
    def authenticate(self, username, password):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM ADMIN WHERE USERNAME = ? AND PASSWORD = ?",  (username, password))
        # FETCH DATA FOR ADMIN
        admin_data = cursor.fetchone()
        if admin_data:
            admin_id = admin_data[0]
            admin_name = admin_data[1]
            self.user_type = "ADMIN"
            self.user_data = (admin_id, admin_name)
            return True
        return False
    def print_info(self, username, password):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM ADMIN WHERE USERNAME = ? AND PASSWORD = ?",  (username, password))
        admin_data = cursor.fetchone()
        
        if admin_data:
            admin_name = admin_data[1]
            admin_surname = admin_data[2]
            print(f"Welcome Admin {admin_name} {admin_surname}!")

        conn.close()
    def print_options(self):
        print("------------- OPTIONS ---------------")
        print("Enter 1 to add a course to the system")
        print("Enter 2 to drop a course from the system")
        print("Enter 3 to add a user to the system")
        print("Enter 4 to drop a user from the system")
        print("Enter 5 to add a student to a course")
        print("Enter 6 to remove a student from a course")
        print("Enter 7 to search roster")
        print("Enter 8 to print roster")
        print("Enter 9 to search course")
        print("Enter 10 to print all courses")
        print("Enter 0 to exit")
    def search_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        print("Enter 1 to search all courses")
        print("Enter 2 to search a specific course")
        parameter = str(input())

        if parameter == "1":
            print("Searching all courses...")
            cursor.execute("SELECT * FROM COURSES")

        if parameter == "2":
            course_CRN = input("Enter CRN: ")
            cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (course_CRN,))

        rows = cursor.fetchall()
        for row in rows:
            print(f"CRN: {row[0]}, TITLE: {row[1]}, DEPARTMENT: {row[2]}, INSTRUCTOR: {row[3]}, PERIOD: {row[4]}, SEMESTER: {row[5]}, YEAR: {row[6]}, CREDITS: {row[7]}")

        conn.close()
    def print_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM STUDENTS")
        rows = cursor.fetchall()
        print("---------------------COURSES--------------------")
        for row in rows:
            print(f"ID: {row[0]}, NAME: {row[1]}, SURNAME: {row[2]}, GRADYEAR: {row[3]}, MAJOR: {row[4]}, EMAIL: {row[5]}")
        conn.commit()
        conn.close()
    def add_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        CRN = input("Enter CRN: ")
        TITLE = input("Enter TITLE: ")
        DEPARTMENT = input("Enter DEPARTMENT: ")
        INSTRUCTOR = input("Enter INSTRUCTOR: ")
        PERIOD = input("Enter PERIOD: ")
        SEMESTER = input("Enter SEMESTER: ")
        YEAR = input("Enter YEAR: ")
        CREDITS = input("Enter CREDITS: ")
        course = Course(CRN, TITLE, DEPARTMENT, INSTRUCTOR, PERIOD, SEMESTER, YEAR, CREDITS)

        cursor.execute("INSERT INTO COURSES (CRN, TITLE, DEPARTMENT, INSTRUCTOR, PERIOD, SEMESTER, YEAR, CREDITS) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (course.course_CRN, 
                        course.course_TITLE, 
                        course.course_DEPARTMENT, 
                        course.course_INSTRUCTOR, 
                        course.course_PERIOD, 
                        course.course_SEMESTER, 
                        course.course_YEAR, 
                        course.course_CREDITS))
        conn.commit()

        print("Course added!")
        conn.close()
    def drop_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        course_CRN = input("Enter CRN: ")
        cursor.execute("DELETE FROM COURSES WHERE CRN = ?", (course_CRN,))

        conn.commit()
        print("Course removed!")
        conn.close()
    def add_user(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        STATUS = input("Enter STATUS: ")
        ID = input("Enter ID: ")
        NAME = input("Enter NAME: ")
        SURNAME = input("Enter SURNAME: ")

        if STATUS == "Student" or STATUS == "student":
            GRADYEAR = input("Enter GRADYEAR: ")
            MAJOR    = input("Enter MAJOR: ")
            EMAIL    = input("Enter EMAIL: ")
            USERNAME = input("Enter USERNAME: ")
            PASSWORD = input("Enter PASSWORD: ")

            cursor.execute("INSERT INTO STUDENTS (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL, USERNAME, PASSWORD) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL, USERNAME, PASSWORD))
            conn.commit()
            print("Student added!")

        if STATUS == "Instructor" or STATUS == "instructor":
            TITLE    = input("Enter TITLE: ")
            HIRE     = input("Enter HIRE: ")
            DEPT     = input("Enter DEPT: ")
            EMAIL    = input("Enter EMAIL: ")
            USERNAME = input("Enter USERNAME: ")
            PASSWORD = input("Enter PASSWORD: ")

            cursor.execute("INSERT INTO INSTRUCTORS (ID, NAME, SURNAME, TITLE, HIRE, DEPT, EMAIL, USERNAME, PASSWORD) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (ID, NAME, SURNAME, TITLE, HIRE, DEPT, EMAIL, USERNAME, PASSWORD))
            conn.commit()
            print("Instructor added!")

        if STATUS == "Admin" or STATUS == "admin":
            TITLE    = input("Enter TITLE: ")
            OFFICE   = input("Enter OFFICE: ")
            EMAIL    = input("Enter EMAIL: ")
            USERNAME = input("Enter USERNAME: ")
            PASSWORD = input("Enter PASSWORD: ")

            cursor.execute("INSERT INTO ADMIN (ID, NAME, SURNAME, TITLE, OFFICE, EMAIL, USERNAME, PASSWORD) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (ID, NAME, SURNAME, TITLE, OFFICE, EMAIL, USERNAME, PASSWORD))
            conn.commit()
            print("Admin added!")

        conn.close()
    def drop_user(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        STATUS = input("Enter STATUS: ")
        ID = input("Enter ID: ")

        if STATUS == "Student" or STATUS == "student":
            cursor.execute("DELETE FROM STUDENTS WHERE ID = ?", (ID,))
            conn.commit()
            print("Student removed!")

        if STATUS == "Instructor" or STATUS == "instructor":
            cursor.execute("DELETE FROM INSTRUCTORS WHERE ID = ?", (ID,))
            conn.commit()
            print("Instructor removed!")

        if STATUS == "Admin" or STATUS == "admin":
            cursor.execute("DELETE FROM ADMIN WHERE ID = ?", (ID,))
            conn.commit()
            print("Admin removed!")

        conn.close()
    def add_student_to_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        course_CRN = input("Enter COURSE CRN: ")
        cursor.execute("SELECT TITLE FROM COURSES WHERE CRN = ?", (course_CRN,))
        courses_data = cursor.fetchone()

        if courses_data:
            courses_title = courses_data[0]

        student_ID = input("Enter STUDENT ID: ")

        cursor.execute("SELECT * FROM STUDENTS WHERE ID = ?", (student_ID,))
        rows = cursor.fetchall()

        for row in rows:
            student_NAME = row[1]
            student_SURNAME = row[2]
            student_GRADYEAR = row[3]
            student_MAJOR = row[4]
            student_EMAIL = row[5]

        student_FULLNAME = student_NAME + " " + student_SURNAME

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {courses_title} (ID INT PRIMARY KEY, NAME TEXT, SURNAME TEXT, GRADYEAR TEXT, MAJOR TEXT, EMAIL TEXT);")

        cursor.execute(f"INSERT INTO {courses_title} (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (student_ID, student_NAME, student_SURNAME, student_GRADYEAR, student_MAJOR, student_EMAIL))

        conn.commit()
        print(f"{student_FULLNAME} added to {courses_title}")
        conn.close()
    def drop_student_from_course(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        course_CRN = input("Enter COURSE CRN: ")
        cursor.execute("SELECT TITLE FROM COURSES WHERE CRN = ?", (course_CRN,))
        courses_data = cursor.fetchone()

        if courses_data:
            courses_title = courses_data[0]

        student_ID = input("Enter STUDENT ID: ")

        cursor.execute(f"DELETE FROM {courses_title} WHERE ID = ?", (student_ID,))

        conn.commit()
        print(f"Student removed from {courses_title}!")
    def search_roster(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        status = str(input("Enter Students, Instructors, or Admin (s, i, a): "))

        if status == "s":
           print("Enter 1 to search all students")
           print("Enter 2 to search a specific student")
           parameter = str(input())
           
           if parameter == "1":
                print("Searching all students...")
                cursor.execute("SELECT * FROM STUDENTS")

           if parameter == "2":
               student_id = input("Enter Student ID: ")
               print("Searching for student...")
               cursor.execute("SELECT * FROM STUDENTS WHERE ID = ?", (student_id,))
           
           rows = cursor.fetchall()

           for row in rows:
               print(f"ID: {row[0]}, NAME: {row[1]}, SURNAME: {row[2]}, GRADYEAR: {row[3]}, MAJOR: {row[4]}, EMAIL: {row[5]}")

        if status == "i":
           print("Enter 1 to search all instructors")
           print("Enter 2 to search a specific instructor")
           parameter = str(input())
           
           if parameter == "1":
                print("Searching all instructors...")
                cursor.execute("SELECT * FROM INSTRUCTORS")

           if parameter == "2":
               instructor_id = input("Enter Instructor ID: ")
               print("Searching for instructor...")
               cursor.execute("SELECT * FROM INSTRUCTORS WHERE ID = ?", (instructor_id,))

           rows = cursor.fetchall()

           for row in rows:
               print(f"ID: {row[0]}, NAME: {row[1]}, SURNAME: {row[2]}, TITLE: {row[3]}, HIRE: {row[4]}, DEPT: {row[5]}, EMAIL: {row[6]}")

        if status == "a":
           print("Enter 1 to search all admins")
           print("Enter 2 to search a specific admin")
           parameter = str(input())
           
           if parameter == "1":
                print("Searching all admins...")
                cursor.execute("SELECT * FROM ADMIN")

           if parameter == "2":
               admin_id = input("Enter Admin ID: ")
               print("Searching for admin...")
               cursor.execute("SELECT * FROM ADMIN WHERE ID = ?", (admin_id))

           rows = cursor.fetchall()

           for row in rows:
               print(f"ID: {row[0]}, NAME: {row[1]}, SURNAME: {row[2]}, TITLE: {row[3]}, OFFICE: {row[4]}, EMAIL: {row[5]}")

        conn.close()
    def print_roster(self):
        conn = sqlite3.connect('leopardDB.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM STUDENTS")
        rows = cursor.fetchall()
        print("---------------------STUDENTS--------------------")
        for row in rows:
            print(f"ID: {row[0]}, NAME: {row[1]}, SURNAME: {row[2]}, GRADYEAR: {row[3]}, MAJOR: {row[4]}, EMAIL: {row[5]}")

        cursor.execute("SELECT * FROM INSTRUCTORS")
        rows = cursor.fetchall()
        print()
        print("---------------------INSTRUCTORS--------------------")
        for row in rows:
            print(f"ID: {row[0]}, NAME: {row[1]}, SURNAME: {row[2]}, TITLE: {row[3]}, HIRE: {row[4]}, DEPT: {row[5]}, EMAIL: {row[6]}")

        cursor.execute("SELECT * FROM ADMIN")
        rows = cursor.fetchall()
        print()
        print("---------------------ADMIN--------------------")
        for row in rows:
            print(f"ID: {row[0]}, NAME: {row[1]}, SURNAME: {row[2]}, TITLE: {row[3]}, OFFICE: {row[4]}, EMAIL: {row[5]}")

        conn.close()


