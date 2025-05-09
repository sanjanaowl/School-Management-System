import sys
from prettytable import PrettyTable
import sqlite3
import re
from personal import Lecturer, Student
import bcrypt

my_db = sqlite3.connect("mydb.db")
c = my_db.cursor()


def main():
    printHeader("This is a School Management System")
    role = getUserRole()
    match role:
        case "admin":
            userAdmin()
        case "student":
            userStudent()
        case "lecturer":
            userlecturer()


# first page getting role
def getUserRole():
    x = PrettyTable()
    x.add_column("id", [1, 2, 3, 4])
    x.add_column("Options", ["Student", "Lecturer", "Admin", "exit"])

    print(x)
    x.clear()
    role = input("Option 1, 2, 3,or 4 : ").strip()

    if role == "1":
        return "student"
    elif role == "2":
        return "lecturer"
    elif role == "3":
        return "admin"
    elif role == "4":
        exitProgram()
    else:
        print("Invalid input, Please put 1, 2, 3,or 4")
        return getUserRole()


# second page login in
def userAdmin():
    printHeader("Hello Admin")
    adminemail = loginAdmin()
    choice = adminChoice()
    adminAction(choice, adminemail)
    userAdmin()


def userStudent():
    printHeader("Hello Student")
    studentEmail = loginStudent()
    choice = studentChoice()
    studentAction(choice, studentEmail)


def userlecturer():
    printHeader("Hello Lecturer")
    lecturerEmail = loginLecturer()
    choice = lecturerChoice()
    lecturerAction(choice, lecturerEmail)


# Logining in for admin, students and lecturers
def loginAdmin():
    userEmail = getEmail("Enter user email: ")
    c.execute("SELECT *  FROM  admin WHERE email = ?", (userEmail,))
    try:
        result = c.fetchall()[0]
    except IndexError:
        print("Wrong Email")
        return loginAdmin()
    adminEmail = result[1]
    adminPassword = result[2]
    password = input("Enter password: ").strip()

    if userEmail == adminEmail:
        if bcrypt.checkpw(password.encode(), adminPassword):
            return userEmail
        else:
            print("Wrong password")
            return loginAdmin()
    return loginAdmin()


def loginStudent():
    userEmail = getEmail("Enter user email: ")
    c.execute("SELECT * FROM student WHERE email = ?", (userEmail,))
    try:
        result = (c.fetchall())[0]
    except IndexError:
        print("Wrong Email")
        return loginStudent()
    studentEmail = result[3]
    studentPassword = result[4]
    password = input("Enter password: ")

    if userEmail == studentEmail:
        if bcrypt.checkpw(password.encode(), studentPassword):
            return userEmail
        else:
            print("Wrong password")
    return loginStudent()


def loginLecturer():
    userEmail = getEmail("Enter user email: ")
    c.execute("SELECT * FROM lecturer WHERE email = ?", (userEmail,))
    try:
        result = c.fetchall()[0]
    except IndexError:
        print("Wrong Email")
        return loginLecturer()
    lecturerEmail = result[3]
    lecturerPassword = result[4]
    password = input("Enter password: ").strip()

    if userEmail == lecturerEmail:
        if bcrypt.checkpw(password.encode(), lecturerPassword):
            return userEmail
        else:
            print("Wrong password")
    return loginLecturer()


# Choices from users
def adminChoice():
    x = PrettyTable()
    idchoice = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    x.add_column("id", idchoice)
    x.add_column(
        "Options",
        [
            "Add Student",
            "Add Lecturer",
            "Remove Student",
            "Remove Lecturer",
            "Enroll Course for Student",
            "Widthdraw Course for Student",
            "Add Course for Lecturer",
            "Remove Course for Lecturer",
            "Show Students and Lecturers",
            "Change Password",
            "exit",
        ],
    )
    print("")  # printing new line
    print(x)
    x.clear()
    choice = input("Option 1, 2, 3...., or 11: ").strip()
    if choice in idchoice:
        return choice
    print("Input have to be number between 1-11")
    return adminChoice()


def studentChoice():
    x = PrettyTable()
    idchoice = ["1", "2", "3", "4", "5"]
    x.add_column("id", idchoice)
    x.add_column(
        "Options",
        [
            "EnrollCourse",
            "WithdrawCourse",
            "Enrolled Course Table",
            "Change Password",
            "exit",
        ],
    )
    print("")  # printing new line
    print(x)
    x.clear()
    choice = input("Option 1, 2, 3, 4 or 5: ").strip()
    if choice in idchoice:
        return choice
    print("Input have to be number between 1-5")
    return studentChoice()


def lecturerChoice():
    x = PrettyTable()
    idchoice = ["1", "2", "3", "4", "5"]
    x.add_column("id", idchoice)
    x.add_column(
        "Options",
        [
            "AddCourse",
            "RemoveCourse",
            "Teaching Course Table",
            "Change Password",
            "exit",
        ],
    )
    print("")  # printing new line
    print(x)
    x.clear()
    choice = input("Option 1, 2, 3, 4 or 5: ").strip()
    if choice in idchoice:
        return choice
    print("Input have to be number between 1-5")
    return lecturerChoice()


# User Actions
def adminAction(choice, email):
    c.execute("SELECT *  FROM admin WHERE email = ?", (email,))
    result = c.fetchall()
    match choice:
        case "1":
            printHeader("Adding Student")
            sfname = input("What is the first name of the student: ").strip().title()
            slname = input("What is the last name of the student: ").strip().title()
            sid = getInt("What is the school id number of student: ", "id")
            semail = getEmail("What is the email of the student: ")
            spassword = passwordgetter("What is the initial password of the student: ")
            c.execute("SELECT * FROM student WHERE email = ?", (semail,))
            if (len(c.fetchall())) != 0:
                print("Student with this email already exits")
                adminAction(choice, email)
                exitProgram()
            c.execute("SELECT * FROM student WHERE id = ?", (sid,))

            if (len(c.fetchall())) != 0:
                print("Student with this id already exits")
                adminAction(choice, email)
                exitProgram()
            shashpassword = bcrypt.hashpw(spassword.encode(), bcrypt.gensalt(10))
            c.execute(
                "INSERT INTO student VALUES(?, ?, ?, ?, ?)",
                (
                    sid,
                    sfname,
                    slname,
                    semail,
                    shashpassword,
                ),
            )
            c.execute(
                "INSERT INTO enrolled VALUES(?, ?, ?, ?, ?)",
                (
                    sid,
                    None,
                    None,
                    None,
                    None,
                ),
            )
            my_db.commit()
            print("Student have been added")

        case "2":
            printHeader("Adding Lecturer")
            lfname = input("What is the first name of the lecturer: ").strip().title()
            llname = input("What is the last name of the lecturer: ").strip().title()
            lid = getInt("What is the school id number of the lecturer: ", "id")
            lemail = getEmail("What is the email of the lecturer: ")
            lpassword = passwordgetter("What is the initial password of the lecturer: ")
            c.execute("SELECT * FROM lecturer WHERE email = ?", (lemail,))
            if (len(c.fetchall())) != 0:
                print("Lecturer with this email already exits")
                adminAction(choice, email)
                exitProgram()
            c.execute("SELECT * FROM lecturer WHERE id = ?", (lid,))

            if (len(c.fetchall())) != 0:
                print("Lecturer with this id already exits")
                adminAction(choice, email)
                exitProgram()
            lhashpassword = bcrypt.hashpw(lpassword.encode(), bcrypt.gensalt(10))
            c.execute(
                "INSERT INTO lecturer VALUES(?, ?, ?, ?, ?)",
                (
                    lid,
                    lfname,
                    llname,
                    lemail,
                    lhashpassword,
                ),
            )
            c.execute(
                "INSERT INTO taught VALUES(?, ?, ?, ?, ?)",
                (
                    lid,
                    None,
                    None,
                    None,
                    None,
                ),
            )
            my_db.commit()
            print("Lecturer have been added")

        case "3":
            printHeader("Removing Student")
            semail = getEmail("What is the email of the student: ")
            sid = getInt("What is the id of the student: ", "id")
            c.execute("SELECT * FROM student WHERE email = ?", (semail,))
            try:
                result = c.fetchall()[0]
            except IndexError:
                print("Student with this email does not exit")
                adminAction(choice, email)
                exitProgram()

            if int(result[0]) != sid:
                print("Student id does not match")
                adminAction(choice, email)
                exitProgram()
            user = (
                input(f"Do you want to remove student with email-{semail}?: Y/N: ")
                .strip()
                .lower()
            )
            if user == "n" or user == "no":
                aChoice = adminChoice()
                adminAction(aChoice, email)
                exitProgram()

            c.execute("DELETE FROM student WHERE email = ?", (semail,))
            c.execute("DELETE FROM enrolled WHERE id = ?", (sid,))
            print("Student has been removed")
            my_db.commit()

        case "4":
            printHeader("Removing lecturer")
            lemail = getEmail("What is the email of the lecturer: ")
            lid = getInt("What is the id of the lecturer: ", "id")
            c.execute("SELECT * FROM lecturer WHERE email = ?", (lemail,))
            try:
                result = c.fetchall()[0]
            except IndexError:
                print("Lecturer with this email does not exit")
                adminAction(choice, email)
                exitProgram()

            if int(result[0]) != lid:
                print("Lecturer id does not match")
                adminAction(choice, email)
                exitProgram()
            user = (
                input(f"Do you want to remove lecturer with email-{lemail}?: Y/N: ")
                .strip()
                .lower()
            )
            if user == "n" or user == "no":
                aChoice = adminChoice()
                adminAction(aChoice, email)
                exitProgram()

            c.execute("DELETE FROM lecturer WHERE email = ?", (lemail,))
            c.execute("DELETE FROM taught WHERE id = ?", (lid,))
            my_db.commit()
            print("Lecturer has been removed")

        case "5":
            printHeader("Enrolling Course for Student")
            semail = getEmail("What is the email of the student: ").strip()
            sid = getInt("What is the id of the student: ", "id")
            c.execute("SELECT * FROM student WHERE email = ?", (semail,))
            try:
                result = c.fetchall()[0]
            except IndexError:
                print("Student with this email does not exit")
                adminAction(choice, email)
                exitProgram()
            if int(result[0]) != sid:
                print("Student id does not match")
                adminAction(choice, email)
                exitProgram()

            course = input("Enter the course code you want to enroll: ").strip()
            c.execute("SELECT *  FROM student WHERE email = ?", (semail,))
            result = c.fetchall()[0]
            sid, sfname, slname, semail = result[:4]
            c.execute("SELECT * FROM enrolled WHERE id = ?", (sid,))
            senrolledCourses = c.fetchall()[0]
            s = Student(sid, sfname, slname, semail, senrolledCourses[1:])
            print(s.enroll(course))

        case "6":
            printHeader("Withdrawing student from a course")
            semail = getEmail("What is the email of the student: ").strip()
            sid = getInt("What is the id of the student: ", "id")
            c.execute("SELECT * FROM student WHERE email = ?", (semail,))
            try:
                result = c.fetchall()[0]
            except IndexError:
                print("Student with this email does not exit")
                adminAction(choice, email)
                exitProgram()
            if int(result[0]) != sid:
                print("Student id does not match")
                adminAction(choice, email)
                exitProgram()

            course = (
                input("Code of the course you want student to withdraw from: ")
                .strip()
                .lower()
            )
            c.execute("SELECT *  FROM student WHERE email = ?", (semail,))
            result = c.fetchall()[0]
            sid, sfname, slname, semail = result[:4]
            c.execute("SELECT * FROM enrolled WHERE id = ?", (sid,))
            senrolledCourses = c.fetchall()[0]
            s = Student(sid, sfname, slname, semail, senrolledCourses[1:])
            print(s.withdraw(course))

        case "7":
            printHeader("Adding Course for Lecturer")
            lemail = getEmail("What is the email of the lecturer: ").strip()
            lid = getInt("What is the id of the lecturer: ", "id")
            c.execute("SELECT * FROM lecturer WHERE email = ?", (lemail,))
            try:
                result = c.fetchall()[0]

            except IndexError:
                print("Lecturer with this email does not exit")
                adminAction(choice, email)
                exitProgram()
            if int(result[0]) != lid:
                print("Lecturer id does not match")
                adminAction(choice, email)
                exitProgram()

            course = (
                input("Code of the course you want lecturer to add: ").strip().lower()
            )
            c.execute("SELECT * FROM lecturer WHERE email = ?", (lemail,))
            result = c.fetchall()[0]
            lid, lfname, llname, lemail = result[:4]
            c.execute("SELECT * FROM taught WHERE id = ?", (lid,))
            taughtCourses = c.fetchall()[0]
            l = Lecturer(lid, lfname, llname, email, taughtCourses[1:])
            print(l.addCourse(course))

        case "8":
            printHeader("Removing Course for Lecturer")
            lemail = getEmail("What is the email of the lecturer: ").strip()
            lid = getInt("What is the id of the lecturer: ", "id")
            c.execute("SELECT * FROM lecturer WHERE email = ?", (lemail,))
            try:
                result = c.fetchall()[0]
            except IndexError:
                print("Lecturer with this email does not exit")
                adminAction(choice, email)
                exitProgram()
            if int(result[0]) != lid:
                print("Lecturer id does not match")
                adminAction(choice, email)
                exitProgram()

            course = input("Code ot the course you want to add: ").strip().lower()
            c.execute("SELECT * FROM lecturer WHERE email = ?", (lemail,))
            result = c.fetchall()[0]
            id, lfname, llname, email = result[:4]
            c.execute("SELECT * FROM taught WHERE id = ?", (lid,))
            taughtCourses = c.fetchall()[0]
            l = Lecturer(id, lfname, llname, email, taughtCourses[1:])
            print(l.removeCourse(course))
        case "9":
            showtable()
        case "10":
            printHeader("Change Password")
            c.execute("SELECT * FROM admin WHERE email = ?", (email,))
            result = c.fetchall()[0]
            adminPassword = result[2]
            oldpassword = input("Old password: ").strip()
            newpassword = input("New password: ").strip()
            conpassword = input("Confirm password: ").strip()
            if not bcrypt.checkpw(oldpassword.encode(), adminPassword):
                print("Wrong Password")
                adminAction(choice, email)
                exitProgram()
            if newpassword != conpassword:
                print("Passwords do not match")
                adminAction(choice, email)
                exitProgram()
            if len(newpassword) <= 5:
                print("Passord too short")
                lecturerAction(choice, email)
                exitProgram()
            newHashedpassword = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt(10))
            c.execute(
                "UPDATE admin SET password = ? WHERE email = ?",
                (
                    newHashedpassword,
                    email,
                ),
            )
            my_db.commit()
            print("Password has been changed")
        case "11":
            exitProgram()
    choice = adminChoice()
    adminAction(choice, email)


def studentAction(choice, email):
    match choice:
        case "1":
            printHeader("Enrolling Course")
            course = (
                input("Code of the course you want to enrolled in: ").strip().lower()
            )
            c.execute("SELECT *  FROM student WHERE email = ?", (email,))
            result = c.fetchall()[0]
            sid, sfname, slname, semail = result[:4]
            c.execute("SELECT * FROM enrolled WHERE id = ?", (sid,))
            enrolledCourses = c.fetchall()[0]
            courses = enrolledCourses[1:]
            s = Student(sid, sfname, slname, semail, courses)
            print(s.enroll(course))
        case "2":
            printHeader("Withdrawing Course")
            course = (
                input("Code of the course you want to withdraw from: ").strip().lower()
            )
            c.execute("SELECT *  FROM student WHERE email = ?", (email,))
            result = c.fetchall()[0]
            id, fname, lname, email = result[:4]
            c.execute("SELECT * FROM enrolled WHERE id = ?", (id,))
            enrolledCourses = c.fetchall()[0]
            s = Student(id, fname, lname, email, enrolledCourses[1:])
            print(s.withdraw(course))
        case "3":
            enrolledTable(email)
        case "4":
            printHeader("Change Password")
            c.execute("SELECT * FROM student WHERE email = ?", (email,))
            result = c.fetchall()[0]
            studentPassword = result[4]
            oldpassword = input("Old password: ").strip()
            newpassword = input("New password: ").strip()
            conpassword = input("Confirm password: ").strip()
            if not bcrypt.checkpw(oldpassword.encode(), studentPassword):
                print("Wrong Password")
                studentAction(choice, email)
                exitProgram()
            if newpassword != conpassword:
                print("Passwords do not match")
                studentAction(choice, email)
                exitProgram()
            if len(newpassword) <= 5:
                print("Passord too short")
                lecturerAction(choice, email)
                exitProgram()
            newHashedPassword = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt(10))
            c.execute(
                "UPDATE student SET password = ? WHERE email = ?",
                (
                    newHashedPassword,
                    email,
                ),
            )
            my_db.commit()
            print("Password has been changed")
        case "5":
            exitProgram()

    choice = studentChoice()
    studentAction(choice, email)


def lecturerAction(choice, email):
    match choice:
        case "1":
            printHeader("Adding Course")
            course = input("Code of the course you want to add: ").strip().lower()
            c.execute("SELECT * FROM lecturer WHERE email = ?", (email,))
            result = c.fetchall()[0]
            lid, lfname, llname, email = result[:4]
            c.execute("SELECT * FROM taught WHERE id = ?", (lid,))
            taughtCourses = c.fetchall()[0]
            l = Lecturer(lid, lfname, llname, email, taughtCourses[1:])
            print(l.addCourse(course))

        case "2":
            printHeader("Removing Course")
            course = input("Code ot the course you want to add: ").strip().lower()
            c.execute("SELECT * FROM lecturer WHERE email = ?", (email,))
            result = c.fetchall()[0]
            lid, lfname, llname, email = result[:4]
            c.execute("SELECT * FROM taught WHERE id = ?", (lid,))
            taughtCourses = c.fetchall()[0]
            l = Lecturer(lid, lfname, llname, email, taughtCourses[1:])
            print(l.removeCourse(course))
        case "3":
            taughtTable(email)
        case "4":
            printHeader("Change Password")
            c.execute("SELECT * FROM lecturer WHERE email = ?", (email,))
            result = c.fetchall()[0]
            lecturerPassword = result[4]
            oldpassword = input("Old password: ").strip()
            newpassword = input("New password: ").strip()
            conpassword = input("Confirm password: ").strip()
            if not bcrypt.checkpw(oldpassword.encode(), lecturerPassword):
                print("Wrong Password")
                lecturerAction(choice, email)
                exitProgram()
            if newpassword != conpassword:
                print("Passwords do not match")
                lecturerAction(choice, email)
                exitProgram()
            if len(newpassword) <= 5:
                print("Passord too short")
                lecturerAction(choice, email)
                exitProgram()
            newHashedPassword = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt(10))
            c.execute(
                "UPDATE lecturer SET password = ? WHERE email = ?",
                (
                    newHashedPassword,
                    email,
                ),
            )
            my_db.commit()
            print("Password has been changed")

        case "5":
            exitProgram()

    choice = lecturerChoice()
    lecturerAction(choice, email)


# small functions of the programm


def getInt(s, name="This"):
    try:
        x = int(input(s).strip())
        return x
    except ValueError:
        print(f"{name} has to be integer")
        getInt(s, name)


def printHeader(s):
    l = len(s)
    print(f"\n{s}")
    for _ in range(l):
        print("=", end="")
    print("")  # printing new line


def getEmail(s):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    x = input(s).strip()
    if re.match(pattern, x):
        return x
    else:
        print("Invalid email")
        return getEmail(s)


def enrolledTable(email):
    c.execute("SELECT id FROM student WHERE email = ?", (email,))
    sid = c.fetchone()[0]
    c.execute("SELECT * FROM enrolled WHERE id = ?", (sid,))
    list = c.fetchall()[0][1:]
    x = PrettyTable()
    printHeader("Enrolled Course Table")
    x.field_names = ["Course1", "Course2", "Course3", "Course4"]
    x.add_row([list[0], list[1], list[2], list[3]])
    print(x)
    x.clear()


def taughtTable(email):
    c.execute("SELECT id FROM lecturer WHERE email = ?", (email,))
    lid = c.fetchone()[0]
    c.execute("SELECT * FROM taught WHERE id = ?", (lid,))
    list = c.fetchall()[0][1:]
    x = PrettyTable()
    printHeader("Teaching Course Table")
    x.field_names = ["Course1", "Course2", "Course3", "Course4"]
    x.add_row([list[0], list[1], list[2], list[3]])
    print(x)
    x.clear()


def showtable():
    x = PrettyTable()

    c.execute("SELECT id, fname, lname, email FROM student")
    result_S = c.fetchall()
    printHeader("Student table")
    x.field_names = ["id", "first name", "last name", "email"]
    for _ in result_S:
        x.add_row(_)
    print(x)
    x.clear()

    printHeader("Lecturer Table")
    x.field_names = ["id", "first name", "last name", "email"]
    c.execute("SELECT id, fname, lname, email FROM lecturer")
    result_L = c.fetchall()
    for _ in result_L:
        x.add_row(_)
    print(x)

    x.clear()


def passwordgetter(s):
    password = input(f"{s}").strip()
    if (len(password)) <= 5:
        print("Password too short")
        return passwordgetter(s)
    return password


def exitProgram():
    c.close()
    my_db.close()
    sys.exit("Thank you for using, Have a great day")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping the Program")
        exitProgram()
