import sqlite3
from user import Student
from user import Course
from user import Instructor
from user import Admin

def init_user_database():
    conn = sqlite3.connect('leopardDB.db')
    cursor = conn.cursor()

    # CREATE ADMIN TABLE
    cursor.execute("DROP TABLE IF EXISTS ADMIN")
    cursor.execute("CREATE TABLE IF NOT EXISTS ADMIN (ID INT PRIMARY KEY, NAME TEXT, SURNAME TEXT, TITLE TEXT, OFFICE TEXT, EMAIL TEXT, USERNAME TEXT, PASSWORD TEXT);")
    cursor.execute("INSERT INTO ADMIN VALUES (30001,'Margaret','Hamilton','President','Dobbs 1600','hamiltonm','hamilton6895','alexander123'),"
                                             "(30002,'Vera','Rubin','Vice-President','Wentworth 101','rubinv','rubinvera1016','iluvcats168'),"
                                             "(42069,'Default','User3','President','Dobbs 202','User','User3','Pass');")
    # CREATE COURSES TABLE
    cursor.execute("DROP TABLE IF EXISTS COURSES")
    cursor.execute("CREATE TABLE IF NOT EXISTS COURSES (CRN INT PRIMARY KEY, TITLE TEXT, DEPARTMENT TEXT, INSTRUCTOR TEXT, PERIOD TEXT, SEMESTER TEXT, YEAR TEXT, CREDITS INT);")
    cursor.execute("INSERT INTO COURSES VALUES (33817,'ALGORITHMS','BSAS','Joseph Fourier','11:00 AM - 12:20 PM','SUMMER','2023',4)," 
                                               "(33950,'ADVANCED DIGITAL CIRCUIT DESIGN','BSEE','Nelson Patrick','8:00 AM - 9:20 AM','SUMMER','2023',4),"
                                               "(33955,'APPLIED PROGRAMMING CONCEPTS','HUSS','Galileo Galilei','8:00 AM - 9:50 AM','SUMMER','2023',3),"
                                               "(33946,'COMPUTER NETWORKS','BCOS','Katie Bouman','12:30 PM - 1:50 PM','SUMMER','2023',4),"
                                               "(33923,'MACHINE LEARNING','BCOS','Katie Bouman','1:00 PM - 2:50 PM','SUMMER','2023',4),"
                                               "(33959,'SIGNALS AND SYSTEMS','BSME','Daniel Bernoulli','1:00 PM - 2:20 PM','SUMMER','2023',4);")

    # CREATE STUDENTS TABLE
    cursor.execute("DROP TABLE IF EXISTS STUDENTS")
    cursor.execute("CREATE TABLE IF NOT EXISTS STUDENTS (ID INT PRIMARY KEY, NAME TEXT, SURNAME TEXT, GRADYEAR TEXT, MAJOR TEXT, EMAIL TEXT, USERNAME TEXT, PASSWORD TEXT);")
    cursor.execute("INSERT INTO STUDENTS VALUES (10001,'Issac','Newton','1668','BSAS','newtoni','newtoni1668','appletree123')," 
                                              "(10002,'Marie','Curie','1903','BSAS','curiem','curiem1903','polish1934'),"
                                              "(10003,'Mikola','Tesla','1878','BSEE','telsan','telsan1878','ny1943'),"
                                              "(10004,'Thomas','Edison','1879','BSEE','notcool','notcool1879','nj1931'),"
                                              "(10005,'John','von Neumann','1923','BSCO','vonneumannj','vonneumannj1923','hungary1903'),"
                                              "(10006,'Grace','Hopper','1928','BCOS','hopperg','hopperg1928','va1992'),"
                                              "(10007,'Mae','Jemison','1981','BSCH','jemisonm','jemisonm1981','al66'),"
                                              "(10008,'Mark','Dean','1979','BSCO','deanm','deanm1979','tn1956'),"
                                              "(10009,'Michael','Faraday','1812','BSAS','faradaym','faradaym1812','uk1867'),"
                                              "(10010,'Ada','Lovelace','1832','BCOS','lovelacea','lovelacea1832','uk1852'),"
                                              "(42069,'Default','User1','President','Dobbs 202','User','User1','Pass');")
    
    # CREATE INSTRUCTORS TABLE
    cursor.execute("DROP TABLE IF EXISTS INSTRUCTORS")
    cursor.execute("CREATE TABLE IF NOT EXISTS INSTRUCTORS (ID INT PRIMARY KEY, NAME TEXT, SURNAME TEXT, TITLE TEXT, HIRE YEAR TEXT, DEPT TEXT, EMAIL TEXT, USERNAME TEXT, PASSWORD TEXT);")
    cursor.execute("INSERT INTO INSTRUCTORS VALUES (20001,'Joseph','Fourier','Full Prof.','1820','BSEE','fourierj','fourierj1820','fourier123')," 
                                                  "(20002,'Nelson','Patrick','Full Prof.','1994','HUSS','patrickn','patrickn1994','patrickn123'),"
                                                  "(20003,'Galileo','Galilei','Full Prof.','1600','BSAS','galileig','galileig1600','galileig123'),"
                                                  "(20004,'Katie','Bouman','Assistant Prof.','2019','BCOS','boumank','boumank2019','boumank123'),"
                                                  "(20005,'Daniel','Bernoulli','Assistant Prof.','1760','BSME','bernoullid','bernoullid1760','bernoullid123'),"
                                                  "(42069,'Default','User2','President','2001','BSCO','User','User2','Pass');")
    
    # CREATE SCHEDULE TABLE
    cursor.execute("DROP TABLE IF EXISTS SCHEDULE")
    cursor.execute("CREATE TABLE IF NOT EXISTS SCHEDULE (CRN INT PRIMARY KEY, TITLE TEXT, DEPARTMENT TEXT, INSTRUCTOR TEXT, PERIOD TEXT, SEMESTER TEXT, YEAR TEXT, CREDITS INT);")

    # CREATING COURSE OBJECTS
    cursor.execute("SELECT * FROM COURSES")
    rows = cursor.fetchall()

    course_list = []
    for row in rows:
        course_list.append(Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], []))

    conn.commit()                                   
    conn.close()

init_user_database()

# LOGIN SYSTEM

print("--------------Welcome to Leopard Web!----------------")

choice = str(input("Enter 1 to login, 0 to exit: "))

if choice == "0":
    print("Seeya next time!")
    exit()

if choice == "1":
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # CREATE 3 DEFAULT USERS
        student = Student(username, password)
        instructor = Instructor(username, password)
        admin = Admin(username, password)

        if student.authenticate(username, password) == True:
            user = student
            user.print_info(username, password)

            while True:
                user.print_options()
                option = str(input())

                # STUDENT OPTIONS
                match option:
                    case "1":
                        print("------------SEARCH COURSE--------------")
                        user.search_course()
                    case "2":
                        print("------------ADD COURSE TO YOUR SCHEDULE--------------")
                        user.add_course()
                    case "3":
                        print("------------DROP COURSE FROM YOUR SCHEDULE--------------")
                        user.drop_course()
                    case "4":
                        print("-------------SCHEDULE--------------")
                        user.print_schedule()
                    case "0":
                        print("Bye Student!")
                        exit()

        if instructor.authenticate(username, password) == True:
            user = instructor
            user.print_info(username, password)

            while True:
                user.print_options()
                option = str(input())

                # INSTRUCTOR OPTIONS
                match option:
                    case "1":
                        print("------------SEARCH COURSE--------------")
                        user.search_course()
                    case "2":
                        print("------------PRINT YOUR SCHEDULE--------------")
                        user.print_schedule(username, password)
                    case "3":
                        print("------------PRINT CLASSLIST--------------")
                    case "0":
                        print("Bye Instructor!")
                        exit()

        if admin.authenticate(username, password) == True:
            user = admin
            user.print_info(username, password)

            while True:
                user.print_options()
                option = str(input())

                # ADMIN OPTIONS
                match option:
                    case "1":
                        print("------------ADD COURSE TO SYSTEM--------------")
                        user.add_course()
                    case "2":
                        print("------------REMOVE COURSE FROM SYSTEM--------------")
                        user.drop_course()
                    case "3":
                        print("------------ADD A USER TO SYSTEM--------------")
                        user.add_user()
                    case "4":
                        print("------------DROP A USER FROM THE SYSTEM--------------")
                        user.drop_user()
                    case "5":
                        print("------------ADD STUDENT TO A COURSE--------------")
                        user.add_student_to_course()
                    case "6":
                        print("------------REMOVE STUDENT FROM A COURSE--------------")
                        user.drop_student_from_course()
                    case "7":
                        print("------------SEARCH ROSTER--------------")
                        user.search_roster()
                    case "8":
                        user.print_roster()
                    case "9":
                        print("------------SEARCH COURSE--------------")
                        user.search_course()
                    case "10":
                        user.print_course()
                    case "0":
                        print("Bye Admin!")
                        exit()

        else:
            print("Invalid credentials. Please try again.")









    