from typing import Any


class Price:
    rates = {
        "USD": {"CHF": 0.83},
        "EUR": {"CHF": 0.94},
        "UAH": {"CHF": 0.02},
        "CHF": {"USD": 1.21,
                "EUR": 1.07,
                "UAH": 50.17}
    }

    def __init__(self, value: int, currency: str):
        self.value: int | float = value
        self.currency: str = currency.upper()

    @staticmethod
    def _to_chf(to_convert: "Price") -> "Price":
        to_convert.value = to_convert.value * Price.rates[to_convert.currency]["CHF"]
        to_convert.currency = "CHF"
        return to_convert

    def __str__(self):
        return f"{self.value:.2f} {self.currency}"

    def __add__(self, other: Any) -> "Price | None":
        if not isinstance(other, Price):
            raise ValueError("Can perform operations only with `Price` objects")
        else:
            if self.currency != other.currency:
                if other.currency in Price.rates.keys() and self.currency in Price.rates.keys():
                    target_currency = self.currency
                    result = self._to_chf(self) + self._to_chf(other)
                    result.value, result.currency = (result.value * Price.rates[result.currency][target_currency],
                                                     target_currency)
                    return result
                else:
                    print("Currency not Supported")
                    return None
            else:
                return Price(self.value + other.value, self.currency.upper())

    def __sub__(self, other: Any) -> "Price | None":
        if not isinstance(other, Price):
            raise ValueError("Can perform operations only with `Price` objects")
        else:
            if self.currency != other.currency:
                if other.currency in Price.rates.keys() and self.currency in Price.rates.keys():
                    target_currency = self.currency
                    result = self._to_chf(self) - self._to_chf(other)
                    result.value, result.currency = (result.value * Price.rates[result.currency][target_currency],
                                                     target_currency)
                    return result
                else:
                    print("Currency not Supported")
                    return None
            else:
                return Price(self.value - other.value, self.currency.upper())


phone = Price(500, "eur")
tablet = Price(50, "usd")

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
