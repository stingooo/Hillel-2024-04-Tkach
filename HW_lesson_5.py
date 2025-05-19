from typing import Any


class Price:
    rates = {
        "USD": 41.62,
        "EUR": 46.94,
    }

    def __init__(self, value: int, currency: str):
        self.value: int = value
        self.currency: str = currency.upper()

    def __str__(self):
        return f"{self.value:.2f} {self.currency}"

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operations only with `Price` objects")
        else:
            if self.currency != other.currency:
                if other.currency in Price.rates.keys():
                    if self.currency.upper() == "USD":
                        self.value, other.value = self.value * Price.rates[self.currency], other.value * Price.rates[
                            other.currency]
                        return Price((self.value + other.value) / Price.rates[self.currency], self.currency.upper())
                    elif self.currency.upper() == "EUR":
                        self.value, other.value = self.value * Price.rates[self.currency], other.value * Price.rates[
                            other.currency]
                        return Price((self.value + other.value) / Price.rates[self.currency], self.currency.upper())
                else:
                    print("Currency not Supported")
            else:
                return Price(self.value + other.value, self.currency.upper())

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operations only with `Price` objects")
        else:
            if self.currency != other.currency:
                if other.currency in Price.rates.keys():
                    if self.currency.upper() == "USD":
                        self.value, other.value = self.value * Price.rates[self.currency], other.value * Price.rates[
                            other.currency]
                        return Price((self.value - other.value) / Price.rates[self.currency], self.currency.upper())
                    elif self.currency.upper() == "EUR":
                        self.value, other.value = self.value * Price.rates[self.currency], other.value * Price.rates[
                            other.currency]
                        return Price((self.value - other.value) / Price.rates[self.currency], self.currency.upper())
                else:
                    print("Currency not Supported")
            else:
                return Price(self.value - other.value, self.currency.upper())


phone = Price(500, "usd")
tablet = Price(50, "eur")

total: Price = phone + tablet
print(total)


class User:
    def __init__(self, username, password):
        self.username: str = username
        self.password: str = password

    def user_check(self, username, password):
        if username == self.username and password == self.password:
            return True
        else:
            return False


users = [
    User("john", 'john123'),
    User("marry", "marry123")
]

authorized_user = None


def auth(func):
    def wrapper(*args, **kwargs):
        global authorized_user
        if authorized_user:
            return func(*args, **kwargs, user=authorized_user)
        while True:
            print("To Execute The command need authorization")
            login = input("Please Enter Login: ").strip()
            password = input("Please Enter Password: ").strip()
            for target in users:
                authorization = target.user_check(login, password)
                if authorization:
                    authorized_user = target
                    print("\nAuthorization Complete\n ")
                    return func(*args, **kwargs, user=target)
            else:
                print("\nLogin and Password are incorrect !!!\n")
    return wrapper


@auth
def command(payload, user: User):
    print(f"Executing command by authorized user {user.username}.\nCommand: {payload}\n")


while user_input := input("Enter anything: "):
    command(user_input)
