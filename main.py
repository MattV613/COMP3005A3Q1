import psycopg2
import datetime

class A3database:
    # This class holds all the functions for question 1
    # It connects to the database using psycopg2
    # Functions other than the assignment specified functions are connect(), disconnect(), and setdbInfo()

    # In order for this class to complete initialization, the user must correctly connect to an existing postgres database
    def __init__(self):
        self.dbname = "Assignment3"
        self.user = "postgres"
        self.host = "localhost"
        self.port = "5433"
        self.password = ""
        self.conn = None

        while True:
            try:
                self.setdbInfo()
                self.connect()
                print("<<Connection Successful>>")
                break
            except Exception as e:
                print(f"{e}")
    def setdbInfo(self):
        # This function will prompt the user to input the database name, user,
        # host, port, and password required to connect to the postgres database
        dbname = input("Input Database name or leave empty for default 'Assignment3'\n-> ")
        user = input("Input user or leave empty for default 'postgres'\n-> ")
        host = input("Input host name or leave empty for default 'localhost'\n-> ")
        port = input("Input port or leave empty for default '5433'\n-> ")
        password = input("Input password (Required)\n-> ")
        if len(dbname) < 1:
            self.dbname = "Assignment3"
        else:
            self.dbname = dbname
        if len(user) < 1:
            self.user = "postgres"
        else:
            self.user = user
        if len(host) < 1:
            self.host = "localhost"
        else:
            self.host = host
        if len(host) < 1:
            self.port = "5433"
        else:
            self.port = port
        self.password = password

    def connect(self):
        # this function takes the class variables that were set in function setdbInfo()
        # and attempts to connect to a postgres database
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def disconnect(self):
        # this function disconnects from a database if one has been connected to
        try:
            self.conn.close()
        except Exception as e:
            print("no database to disconnect")

    def getAllStudents(self):
        # Cursor to get all information from the students table
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM students")

        rows = cur.fetchall()

        # print all rows
        for row in rows:
            print(row)

        cur.close()

        input("press any key...")

    def addStudent(self, first_name, last_name, email, enrollment_date):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('{first_name}', '{last_name}', '{email}', '{enrollment_date}')")
        self.conn.commit()
        cur.close()

    def updateStudentEmail(self, student_id, new_email):
        cur = self.conn.cursor()
        cur.execute(
            f"UPDATE students\nSET email = '{new_email}'\nWHERE student_id = {student_id};")
        self.conn.commit()
        cur.close()

    def deleteStudent(self, student_id):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM students\nWHERE student_id = {student_id};")
        self.conn.commit()
        cur.close()

def main():
    # Create the database object
    db = A3database()

    while True:
        # User will stay in this loop until they exit with option 5

        print("_______________\n[1] Get All Students\n[2] Add Student\n[3] Update Student Email\n[4] DeleteStudent\n[5] Exit\n_______________")
        while True:
            # User will stay in this loop until they input a valid option (1-5)

            option = input("-> ")
            try:
                # Makes sure user input is valid
                option = int(option)
                assert 0 < option < 6
                break
            except Exception as e:
                continue
        match option:
            case 1:
                db.getAllStudents()
            case 2:
                print("-----Add Student-----")
                try:
                    # get and check all needed user inputs for adding a student
                    fn = input("first_name -> ")
                    if len(fn) == 0:
                        print("\tYou must enter a first name")
                        continue
                    ln = input("last_name -> ")
                    if len(ln) == 0:
                        print("\tYou must enter a last name")
                        continue
                    email = input("email -> ")
                    if len(email) == 0:
                        print("\tYou must enter an email")
                        continue
                    ed = input("enrollment_date (In format 'YYYY-MM-DD') -> ")
                    try:
                        # Make sure the date was input in the correct format
                        assert len(ed) == 10
                        edlist = ed.split("-")
                        assert len(edlist) == 3
                        assert len(edlist[0]) == 4
                        assert len(edlist[1]) < 3
                        assert len(edlist[2]) < 3
                        assert 0 <= int(edlist[1]) <= 12
                        date_obj = datetime.date(int(edlist[0]),int(edlist[1]), int(edlist[2]))
                        db.addStudent(fn,ln,email,ed)
                    except psycopg2.errors.UniqueViolation as e:
                        # If the email was not unique, this will catch that error
                        print("\n<ERROR> Email already in use")
                    except Exception as e:
                        print("\n<ERROR> Invalid date format")
                        print(f"{type(e)}:{e}")
                except Exception as e:
                    print(f"{type(e)}:{e}")

            case 3:
                # Get and check all user inputs needed for changing a students email
                print("-----Change Students Email-----")
                student_id = input("Input student ID -> ")
                email = input("Input new email -> ")
                try:
                    student_id = int(student_id)
                    assert len(email) > 2 # needs at least an @ and a .
                    db.updateStudentEmail(student_id, email)
                except AssertionError as e:
                    print("You must input a valid email")
                except Exception as e:
                    print(f"{type(e)}:{e}")

            case 4:
                # get and check that the user inputs a valid student ID
                print("-----Delete Student-----")
                student_id = input("Input student ID -> ")
                try:
                    student_id = int(student_id)
                    db.deleteStudent(student_id)
                except Exception as e:
                    # if not a valid student ID, this will catch it
                    print(f"{type(e)}:{e}")

            case 5:
                #Disconnect from the database and break from the while loop
                db.disconnect()
                break

main()
