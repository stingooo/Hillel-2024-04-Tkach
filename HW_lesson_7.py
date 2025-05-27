import enum


class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()


class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    def send_notification(self, notification):
        print(f"From {self.role.capitalize()}: {self.name.capitalize()}\n"
              f"Email: {self.email}\n"
              f"--------------\n{notification}--------------\n")
        #  print out or log the notification


class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment  # Optional extra info

    def __str__(self):
        return self.format()

    def format(self) -> str:
        return f"Subject: {self.subject}\n\n Message: {self.message}\n Additional attachment: {self.attachment}\n"


class StudentNotification(Notification):
    def __init__(self, subject: str, message: str, attachment: str = ""):
        super().__init__(
            subject=subject,
            message=message,
            attachment=attachment
        )

    def __str__(self):
        return self.format()

    def format(self) -> str:
        return "".join((self.message, "\n\nSent via Student Portal\n"))


class TeacherNotification(Notification):
    def __init__(self, subject: str, message: str, attachment: str = ""):
        super().__init__(
            subject=subject,
            message=message,
            attachment=attachment
        )
    def __str__(self):
        return self.format()

    def format(self):
        return "".join((self.message, "\n\nTeacher's Desk Notification\n"))


def main():
    student = User("John", "john@gmail.com", Role.STUDENT)
    teacher = User("Marry", "marry@gmail.com", Role.TEACHER)
    notification_1 = StudentNotification(subject="Help with Homework",
                                         message="Please help to understand the HW number 5")
    notification_2 = TeacherNotification(subject="Assist with homework",
                                         message="Please look to the page number 56 in the book")

    student.send_notification(notification_1)
    teacher.send_notification(notification_2)
    #  create users of both types
    #  create notifications
    #  have users print (aka send) their notifications


if __name__ == "__main__":
    main()
