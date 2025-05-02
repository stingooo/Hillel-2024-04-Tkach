from fuzzywuzzy import fuzz

storage: list[dict] = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "marks": [7, 8, 9, 10, 6, 7, 8],
        "info": "Alice Johnson is 18 y.o. Interests: math",
    },
    {
        "id": 2,
        "name": "Michael Smith",
        "marks": [6, 5, 7, 8, 7, 9, 10],
        "info": "Michael Smith is 19 y.o. Interests: science",
    },
    {
        "id": 3,
        "name": "Emily Davis",
        "marks": [9, 8, 8, 7, 6, 7, 7],
        "info": "Emily Davis is 17 y.o. Interests: literature",
    },
    {
        "id": 4,
        "name": "James Wilson",
        "marks": [5, 6, 7, 8, 9, 10, 11],
        "info": "James Wilson is 20 y.o. Interests: sports",
    },
    {
        "id": 5,
        "name": "Olivia Martinez",
        "marks": [10, 9, 8, 7, 6, 5, 4],
        "info": "Olivia Martinez is 18 y.o. Interests: art",
    },
    {
        "id": 6,
        "name": "Emily Davis",
        "marks": [4, 5, 6, 7, 8, 9, 10],
        "info": "Daniel Brown is 19 y.o. Interests: music",
    },
    {
        "id": 7,
        "name": "Sophia Taylor",
        "marks": [11, 10, 9, 8, 7, 6, 5],
        "info": "Sophia Taylor is 20 y.o. Interests: physics",
    },
    {
        "id": 8,
        "name": "William Anderson",
        "marks": [7, 7, 7, 7, 7, 7, 7],
        "info": "William Anderson is 18 y.o. Interests: chemistry",
    },
    {
        "id": 9,
        "name": "Isabella Thomas",
        "marks": [8, 8, 8, 8, 8, 8, 8],
        "info": "Isabella Thomas is 19 y.o. Interests: biology",
    },
    {
        "id": 10,
        "name": "Benjamin Jackson",
        "marks": [9, 9, 9, 9, 9, 9, 9],
        "info": "Benjamin Jackson is 20 y.o. Interests: history",
    },
]


def generate_id() -> int:
    students_ids = [student["id"] for student in storage]
    new_id = max(students_ids) + 1
    return new_id


def add_student(student: dict) -> dict:
    if not student.get("name"):
        print("==============================\n"
              "Enter at least the student Name ")
        while not student.get("name"):
            student = ask_student_payload()
        storage.append(student)
        return student
    else:
        # action
        storage.append(student)
        return student


def add_marks(target_id: int, raw_marks: str) -> dict | None:
    """
    Function to add Marks
    """
    for index, target in enumerate(storage):
        if target_id == target["id"]:
            marks_to_add: list = [int(i) for i in raw_marks.replace(" ", "").split(",") if i]
            storage[index]['marks'].extend(marks_to_add)
            return target


def update_student_data(student_id: int) -> dict | None:
    """
    Function to update student data
    """
    if student_id not in [ids['id'] for ids in storage]:
        return None
    else:
        for index, target in enumerate(storage):
            if student_id == target["id"]:
                print(f"What you Like to update for {storage[index]['name']}?\n"
                      f"{'For Name Enter  ':<25} '1'\n"
                      f"{'For Marks Enter  ':<25} '2'\n"
                      f"{'For Info Enter  ':<25} '3'\n"
                      f"{'For Marks and Info Enter':<25} '4'\n"
                      f"===========================")
                item_to_update = input("Please select :")
                if item_to_update == "1":
                    new_name: str = input("Please Enter a NEW Name :")
                    if new_name:
                        storage[index]["name"] = new_name
                        storage[index]["marks"] = []
                        storage[index]["info"] = ""
                        print("Name is Updated, marks and info erased due to new Name")
                    else:
                        return None
                elif item_to_update == "2":
                    marks = input("Please Input a new Marks, separated by ',' :")
                    if marks:
                        try:
                            storage[index]["marks"] = [int(item) for item in marks.replace(" ", "").split(",")]
                        except ValueError:
                            print("Invalid input, Marks will be saved as Empty")
                            storage[index]["marks"] = []
                            return None
                    else:
                        return None
                elif item_to_update == "3":
                    new_info: str = input("Please Enter a NEW Info :")
                    if new_info:
                        current_info: str = storage[index]["info"]
                        info_match = fuzz.token_sort_ratio(new_info, current_info)
                        if info_match < 50:
                            storage[index]["info"] += ", " + new_info
                        else:
                            storage[index]["info"] = new_info
                    else:
                        return None
                elif item_to_update == "4":
                    marks = input("Please Input a new Marks, separated by ',' :")
                    if marks:
                        try:
                            storage[index]["marks"] = [int(item) for item in marks.replace(" ", "").split(",")]
                        except ValueError:
                            print("Invalid input, Marks will be saved as Empty")
                            storage[index]["marks"] = []
                            return None
                    else:
                        return None
                    new_info: str = input("Please Enter a NEW Info :")
                    if new_info:
                        current_info: str = storage[index]["info"]
                        info_match = fuzz.token_sort_ratio(new_info, current_info)
                        if info_match < 50:
                            storage[index]["info"] += ", " + new_info
                        else:
                            storage[index]["info"] = new_info
                    else:
                        return None

                return storage[index]


def show_students():
    print("=========================\n")
    for student in storage:
        print(f"{student['id']}. Student {student['name']}\n")
    print("=========================\n")


def search_student(student_id: int) -> None:
    for student in storage:
        info = (
            "=========================\n"
            f"[{student['id']}] Student {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"Info: {student['info']}\n"
            "=========================\n"
        )

        if student["id"] == student_id:
            print(info)
            return

    print(f"Student {student_id} not found")


def ask_student_payload() -> dict:
    print("==============================")
    name = input("Please Enter The student Name : ")
    marks = input("Please Enter the Student marks if it exist separated by ',' :")
    if marks:
        try:
            marks = [int(item) for item in marks.replace(" ", "").split(",")]
        except ValueError as err:
            print("Invalid input, Marks will be saved as Empty")
            marks = []
    else:
        marks = []
    info = input("Please Enter the additional information if applicable :")
    if not info:
        info = ""

    return {
        "id": generate_id(),
        "name": name,
        "marks": marks,
        "info": info
    }


def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict = add_student(data)
            print(f"Student: {student['name']} is added with ID {student['id']}")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if student_id:
            search_student(student_id=int(student_id))
        else:
            print("Student's name is required to search")
    elif command == "marks":
        show_students()
        target_id = int(input("Please Enter The Student ID to add marks:"))
        if target_id in [ids['id'] for ids in storage]:
            raw_marks = input("Please input the marks to add separated by ',':")
            target = add_marks(target_id, raw_marks)
            print(f"{target['name']} Marks added...")
        else:
            print("Student not Found")
    elif command == "update":
        show_students()
        try:
            student_id: int = int(input("Please Enter Student ID to UPDATE: "))
            if student_id:
                updated_student = update_student_data(student_id)
                if updated_student:
                    print(f"{updated_student['name']} updated accordingly ...")
                else:
                    print("Error to Update")
        except ValueError:
            print("Error to Update")





def main():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "marks", "update")
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
            student_management_command_handle(command)


if __name__ == "__main__":
    main()
