from fuzzywuzzy import fuzz
import csv
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
import asyncio
from threading import Thread
import datetime

STORAGE_FILE_NAME = Path(__file__).parent / "students.csv"
results = set()
tasks : set[asyncio.Task] = set()
refresh_time = 1


class Repository:
    def __init__(self):
        with open(STORAGE_FILE_NAME, "r") as file:
            self.file = file
            self.students = asyncio.run(self.get_storage())

    async def get_storage(self):
        reader = list(csv.DictReader(self.file, fieldnames=["id", "name", "marks", "info"], delimiter=";"))
        for item in reader:
            item["marks"] = eval(item["marks"])
        return reader

    async def update_storage(self):
        with open(STORAGE_FILE_NAME, "w") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
            for student in self.students:
                writer.writerow(student)


repository = Repository()

def inject_repository(func):
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs, repo=repository)
    return wrapped


class ReportSender:

    def __init__(self, sender, password):
        self.sender = sender
        self.password = password

    @inject_repository
    def average_mark(self, repo: Repository = None) -> str:
        today_marks = []
        for student in repo.students:
            maks_to_add = map(lambda x: x[0],filter(lambda mark: mark[1] == datetime.date.today(), student["marks"]))
            today_marks.extend(list(maks_to_add))

        return f"{sum(today_marks) / len(today_marks):.1f}"

    async def daily_email_send(self, recipients):
        msg = MIMEText(f"Today The average mark is {self.average_mark()}")
        msg['Subject'] = "daily_Average Mark"
        msg['From'] = self.sender
        msg['To'] = recipients
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(self.sender, self.password)
                smtp_server.sendmail(self.sender, recipients, msg.as_string())
        except Exception as e:
            print(e, "Unable to send email")

    @inject_repository
    async def monthly_email_send(self, recipients, repo: Repository = None):
        msg = MIMEText(f"Total Digital Journal students -- {len(repo.students)} persons")
        msg['Subject'] = "Monthly total number of students"
        msg['From'] = self.sender
        msg['To'] = recipients
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(self.sender, self.password)
                smtp_server.sendmail(self.sender, recipients, msg.as_string())
        except Exception as e:
            print(e, "Unable to send email")


# Input you data to log in to gmail
sender1 =  ReportSender("login@gmail.com", "password")


def generate_id() -> str:
    students_ids = [int(student["id"]) for student in repository.students]
    new_id = max(students_ids) + 1
    return str(new_id)

def add_date(mark):
    return int(mark), datetime.date.today()


class StudentService:

    @inject_repository
    def add_student(self, student: dict, repo: Repository = None) -> dict:
        if not student.get("name"):
            print("==============================\n"
                  "Enter at least the student Name ")
            while not student.get("name"):
                student = ask_student_payload()
            repo.students.append(student)
            return student
        else:
            # action
            repo.students.append(student)
            return student

    @inject_repository
    def add_marks(self,  target_id: str, raw_marks: str, repo: Repository = None) -> dict | None:
        """
        Function to add Marks
        """
        try:
            raw_marks = list(map(add_date, raw_marks.split(",")))
        except ValueError as err:
            print("Invalid value" + str(err))
        for index, target in enumerate(repo.students):
            if target_id == target["id"]:
                if repo.students[index]["marks"] == "No marks":
                    repo.students[index]["marks"] = raw_marks
                else:
                    repo.students[index]["marks"].extend(raw_marks)
                return target
            return None
        return None

    @inject_repository
    def update_student_data(self, student_id: str, repo: Repository = None) -> dict | None:
        """
        Function to update student data
        """
        def change_name(name_for_update):
            repo.students[index]["name"] = name_for_update
            repo.students[index]["marks"] = ""
            repo.students[index]["info"] = ""
            print("Name is Updated, marks and info erased due to new Name")

        def additional_marks(marks_to_add):
            marks_to_add = list(map(add_date, marks_to_add.split(",")))
            if repo.students[index]["marks"] == "No marks":
                repo.students[index]["marks"] = marks_to_add
            else:
                repo.students[index]["marks"].extend(marks_to_add)
            return None

        def change_info(info_to_update):
            current_info: str = repo.students[index]["info"]
            if current_info == "No info":
                current_info = ""
            info_match = fuzz.token_sort_ratio(info_to_update, current_info)
            if info_match < 50:
                if current_info:
                    repo.students[index]["info"] += ", " + new_info
                else:
                    repo.students[index]["info"] = new_info
            else:
                repo.students[index]["info"] = new_info

        if student_id not in [ids['id'] for ids in repository.students]:
            return None
        else:
            for index, target in enumerate(repo.students):
                if student_id == target["id"]:
                    print(f"What you Like to update for {repo.students[index]['name']}?\n"
                          f"{'For Name Enter  ':<25} '1'\n"
                          f"{'For Marks Enter  ':<25} '2'\n"
                          f"{'For Info Enter  ':<25} '3'\n"
                          f"{'For Marks and Info Enter':<25} '4'\n"
                          f"===========================")
                    item_to_update = input("Please select :")
                    if item_to_update == "1":
                        new_name: str = input("Please Enter a NEW Name :")
                        if new_name:
                            change_name(new_name)
                        else:
                            return None
                    elif item_to_update == "2":
                        marks = input("Please Input a new Marks, separated by ',' :")
                        if marks:
                            additional_marks(marks)
                            print("Marks Added")
                        else:
                            return None
                    elif item_to_update == "3":
                        new_info: str = input("Please Enter a NEW Info :")
                        if new_info:
                            change_info(new_info)
                        else:
                            return None
                    elif item_to_update == "4":
                        marks = input("Please Input a new Marks, separated by ',' :")
                        if marks:
                            additional_marks(marks)
                        else:
                            return None
                        new_info: str = input("Please Enter a NEW Info :")
                        if new_info:
                            change_info(new_info)
                        else:
                            return None
                    elif item_to_update == "":
                        return None
                    return repo.students[index]
                return None
            return None

    @inject_repository
    def show_students(self, repo: Repository = None):
        print("=========================\n")
        for student in repo.students:
            print(f"{student['id']}. Student {student['name']}\n")
        print("=========================\n")

    @inject_repository
    def search_student(self, student_id: str, repo: Repository = None) -> None:

        for student in repo.students:
            marks = ",".join([str(mark[0]) for mark in student["marks"]])
            info = (
                "=========================\n"
                f"[{student['id']}] Student {student['name']}\n"
                f"Marks: {marks}\n"
                f"Info: {student['info']}\n"
                "=========================\n"
            )

            if student["id"] == student_id:
                print(info)
                return

        print(f"Student {student_id} not found")

    @inject_repository
    def delete_student(self, student_id: str, repo: Repository = None):
        print("=========================\n")
        for index, student in enumerate(repo.students):
            if student_id == student["id"]:
                name_to_delete = student['name']
                del repo.students[index]
                print(f"Student {name_to_delete} Deleted\n")
        print("=========================\n")





def ask_student_payload() -> dict:
    print("==============================")
    name = input("Please Enter The student Name : ")
    marks = input("Please Enter the Student marks if it exist separated by ',' :").split(",")
    try:
        marks = list(map(add_date, marks))
    except ValueError as err:
        print("Invalid value" + str(err))

    if not marks:
        marks = "No marks"
    info = input("Please Enter the additional information if applicable :")
    if not info:
        info = "No info"

    return {
        "id": generate_id(),
        "name": name,
        "marks": marks,
        "info": info
    }


def student_management_command_handle(command: str, loop :asyncio.AbstractEventLoop):
    student_service = StudentService()
    if command == "show_students":
        student_service.show_students()
    elif command == "add_student":
        data = ask_student_payload()
        if data:
            student_service.add_student(data)
            print(f"Student: {data['name']} is added with ID {data['id']}")
            task = loop.create_task(repository.update_storage())
            tasks.add(task)
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search_student":
        student_service.show_students()
        student_id: str = input("\nEnter student's ID: ")
        if student_id:
            student_service.search_student(student_id=student_id)
        else:
            print("Student's name is required to search")
    elif command == "add_marks":
        student_service.show_students()
        target_id = input("Please Enter The Student ID to add marks:")
        if target_id in [ids['id'] for ids in repository.students]:
            raw_marks = input("Please input the marks to add separated by ',':")
            target = student_service.add_marks(target_id, raw_marks)
            task = loop.create_task(repository.update_storage())
            tasks.add(task)
            print(f"{target['name']} Marks added...")
        else:
            print("Student not Found")
    elif command == "update_student":
        student_service.show_students()
        student_id: str = input("Please Enter Student ID to UPDATE: ")
        if student_id:
            updated_student = student_service.update_student_data(student_id)
            if updated_student:
                print(f"{updated_student['name']} updated accordingly ...")
                task = loop.create_task(repository.update_storage())
                tasks.add(task)
            else:
                print("Error to Update")
    elif command == "delete_student":
        student_service.show_students()
        student_id: str = input("Please Enter Student ID to DELETE: ")
        if student_id in [ids['id'] for ids in repository.students]:
            student_service.delete_student(student_id)
            task = loop.create_task(repository.update_storage())
            tasks.add(task)
        else:
            print("Student not Found")
    elif command == "send_daily":
        task = loop.create_task(sender1.daily_email_send("sashamixa14@gmail.com"))
        tasks.add(task)
    elif command == "send_monthly":
        task = loop.create_task(sender1.monthly_email_send("sashamixa14@gmail.com"))
        tasks.add(task)


async def crawler():
    global tasks
    while True:
        if not tasks:
            await asyncio.sleep(1)
        else:
            done, pending = await asyncio.wait(tasks, timeout=refresh_time)
            tasks -= done

def main():

    loop = asyncio.new_event_loop()
    Thread(target=loop.run_until_complete, args=(crawler(),), daemon=True).start()

    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show_students", "add_student", "search_student", "add_marks",
                                   "update_student", "delete_student", "send_daily", "send_monthly")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "Hello in the Journal! User the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(HELP_MESSAGE)


    while True:

        command = input("\n Select command: ")

        if command == "quit":
            print("\nThanks for using the Journal application")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command, loop)


if __name__ == "__main__":
    main()
