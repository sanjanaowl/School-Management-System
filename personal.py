import sqlite3

my_db = sqlite3.connect("mydb.db")
c = my_db.cursor()


# personal object template
class UniversityPersonal:
    def __init__(self, id, fname, lname, email):
        self._id = id
        self._fname = fname
        self._lname = lname
        self._email = email

    # getters
    @property
    def id(self):
        return self._id

    def fname(self):
        return self._fname

    @property
    def lname(self):
        return self._lname

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._fname + self._lname


# creating lecturer object
class Lecturer(UniversityPersonal):
    def __init__(self, id, fname, lname, email, taughtCourses):
        super().__init__(id, fname, lname, email)
        self._taughtCourses = taughtCourses

    def addCourse(self, course):
        if course in self._taughtCourses:
            return f"Lecturer is already teaching {course}, it can't be added"

        a = []
        for i, _ in enumerate(self._taughtCourses):
            if _ == None:
                a.append(i)
        if len(a) == 0:
            return "You are already teaching four courses which is a limit, to add this couser please remove other course"

        courseNumber = "course" + str(a[0] + 1)
        c.execute(
            f"UPDATE taught SET {courseNumber} = ? WHERE id = ?",
            (
                course,
                self.id,
            ),
        )
        my_db.commit()
        return f"You have added the course {course}"

    def removeCourse(self, course):
        if course not in self._taughtCourses:
            return f"Lecturer is not teaching {course}, it can't be removed"

        a = 0
        for i, _ in enumerate(self._taughtCourses):
            if _ == course:
                a = i + 1
        courseNumber = "course" + str(a)
        c.execute(f"UPDATE taught SET {courseNumber} = NULL WHERE id = ?", (self.id,))
        my_db.commit()
        return f"You have removed the course {course}"


# creating student object
class Student(UniversityPersonal):
    def __init__(self, id, fname, lname, email, enrolledCourses):
        super().__init__(id, fname, lname, email)
        self._enrolledCourses = enrolledCourses

    def enroll(self, course):
        if course in self._enrolledCourses:
            return f"You are already enrolled in {course}, it can't be enrolled"

        # itirating through enrolledcourse to get course1, course2, course3 or course4
        a = []
        for i, _ in enumerate(self._enrolledCourses):
            if _ == None:
                a.append(i)
        if len(a) == 0:
            return "You are already enrolled in four courses which is a limit, to enroll in this course please widthraw from other subject"

        courseNumber = "course" + str(a[0] + 1)
        c.execute(
            f"UPDATE enrolled SET {courseNumber} = ? WHERE id = ?",
            (
                course,
                self.id,
            ),
        )
        my_db.commit()
        return "You have been enrolled in the course"

    def withdraw(self, course):
        if course not in self._enrolledCourses:
            return f"You are not enrolled in {course}, it can't be withdrawn"

        # itirating through enrolledcourse to get course1, course2, course3 or course4
        a = 0
        for i, _ in enumerate(self._enrolledCourses):
            if _ == course:
                a = i + 1

        courseNumber = "course" + str(a)
        c.execute(f"UPDATE enrolled SET {courseNumber} = NULL WHERE id = ?", (self.id,))
        my_db.commit()
        return "You have been withdrawn from this course"
