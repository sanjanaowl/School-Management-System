from project import exitProgram, getInt, getEmail, passwordgetter
import sqlite3
from personal import Lecturer, Student

my_db = sqlite3.connect("mydb.db")
c = my_db.cursor()


def main():
    test_getInt()
    test_getEmail()
    test_passwordgetter()
    test_enroll()
    test_withdraw()
    test_addCourse()
    test_removeCourse()


def test_getInt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert getInt("Enter a number: ") == 1


def test_getEmail(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "kiran@uni.edu")
    assert getEmail("Enter a email: ") == "kiran@uni.edu"


def test_passwordgetter(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Kirankiran")
    assert passwordgetter("Enter a password: ") == "Kirankiran"


def test_enroll():
    s = getting_student()
    assert s.enroll("cs50") == "You have been enrolled in the course"


def test_withdraw():
    s = getting_student()
    assert s.withdraw("cs50") == "You have been withdrawn from this course"


def test_addCourse():
    l = getting_lecturer()
    assert l.addCourse("cs50") == "You have added the course cs50"


def test_removeCourse():
    l = getting_lecturer()
    assert l.removeCourse("cs50") == "You have removed the course cs50"


def getting_student():
    c.execute("SELECT * FROM student WHERE email = ?", ("test@uni.edu",))
    try:
        result = c.fetchall()[0]
    except IndexError:
        print("testing student has been removed from the database")
        return
    sid = result[0]
    c.execute("SELECT * FROM enrolled WHERE id = ?", (sid,))
    try:
        result1 = c.fetchall()[0]
    except IndexError:
        print(
            "testing student enrolled subjects info has been removed from the database"
        )

    return Student(result[0], result[1], result[2], result[3], result1[1:])


def getting_lecturer():
    c.execute("SELECT * FROM lecturer WHERE email = ?", ("tester@uni.edu",))
    try:
        result = c.fetchall()[0]
    except IndexError:
        print("testing lecturer has been removed from the database")
        return
    lid = result[0]
    c.execute("SELECT * FROM taught WHERE id = ?", (lid,))
    try:
        result1 = c.fetchall()[0]
    except IndexError:
        print(
            "testing lecturer teaching subjects info has been removed from the database"
        )

    return Lecturer(result[0], result[1], result[2], result[3], result1[1:])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping the Program")
        exitProgram()
