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
        pass


class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment  # Optional extra info

    def __str__(self):
        return f"Subject: {self.subject}\n\n Message: {self.message}\n Additional attachment: {self.attachment}\n"

    def format(self) -> str:
        #  implement basic notification formatting
        #  think about `__str__` usage instead of `format`
        pass


class StudentNotification(Notification):
    def __init__(self, subject: str, message: str, attachment: str = ""):
        super().__init__(
            subject=subject,
            message="".join((message, "\n\nSent via Student Portal")),
            attachment=attachment
        )

    def format(self) -> str:
        #  add "Sent via Student Portal" to the message
        pass


class TeacherNotification(Notification):
    def __init__(self, subject: str, message: str, attachment: str = ""):
        super().__init__(
            subject=subject,
            message="".join((message, "\n\nTeacher's Desk Notification")),
            attachment=attachment
        )
    def format(self)\
            -> str:
        #  add "Teacher's Desk Notification" to the message
        pass


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
    pass


if __name__ == "__main__":
    main()
