import codecs
import csv
import hashlib
import uuid
from tabulate import tabulate

def main():
    """
    Функция позволяет пользователю выбрать действие:
    1 - Авторизоваться
    2 - Зарегистрироваться
    """
    print("Выберите операцию:\n 1 - Авторизоваться.\n 2 - Зарегистрироваться.")

    try:
        choice = int(input())
    except ValueError:
        print("Введено неверное значение!")
        main()

    if choice == 1 or choice == 2:
        login = input("Введите логин: ")
        if len(login) < 3:
            print("Длина логина должна быть больше 2 символов!")
            main()
        password = input("Введите пароль: ")
        if len(password) < 8:
            print("Длина пароля должна быть больше 7 символов!")
            main()
        file_reading(choice=choice, login=login, password=password)

    else:
        print("Введено неверное значение операции!")
        main()


def file_reading(choice: int, login: str, password: str):
    """
    Функция считывает файл с данными зарегистрированных пользователей (логин, пароль, роль, соль пароля) и в зависимости
    от выбора в главном меню (функции main) перенаправляет в функцию аутентификации или проверки на занятость логина
    :param choice: выбор в функции main
    :param login: введённый пользователем логин
    :param password: введённый пользователем пароль
    """
    with open("users.csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        users = []
        for row in csv_reader:
            users.append(row)

    csv_file.close()

    if choice == 1:
        authentication(users=users, login=login, password=password)
    elif choice == 2:
        checking_for_existing(users=users, login=login, password=password)


def authentication(users: [], login: str, password: str):
    """
    Функция проверяет введённые пользователем логин и пароль со значениями в базе данных и при совпадении вызывает
    функцию Admin или Seller или Buyer (в зависимости от роли в базе данных) класса User, в обратном случае - выводит
    ошибку
    :param users: база данных зарегистрированных пользователей (логин, пароль, роль, соль пароля)
    :param login: введённый пользователем логин
    :param password: введённый пользователем пароль
    """
    if any(login == user[0] and hashlib.sha256(password.encode() + user[3].encode()).hexdigest() == user[1] for user in users):
        for user in users:
            if login == user[0] and hashlib.sha256(password.encode() + user[3].encode()).hexdigest() == user[1] == user[1]:
                role = user[2]

                if role == "admin":
                    print(f"Добро пожаловать, администратор {login}!")
                    Admin(login=login, password=password)

                elif role == "seller":
                    print(f"Добро пожаловать, продавец {login}!")
                    Seller(login=login, password=password, registration=False)  # Флаг регистрации

                elif role == "buyer":
                    print(f"Добро пожаловать, покупатель {login}!")
                    Seller(login=login, password=password, registration=False)  # Флаг регистрации
    else:
        print("Введён неправильный логин или пароль!")
        main()


def checking_for_existing(users: [], login: str, password: str):
    """
    Функция проверяет базу данных на наличие введённого пользователем логина для регистрации и соответствие двух
    введённых паролей и, в зависимости от результата, вызывает функцию Seller класса User или вызывает функцию Buyer
    класса User, или выводит ошибку
    :param users: база данных зарегистрированных пользователей (логин, пароль, роль, соль пароля)
    :param login: введённый пользователем логин
    :param password: введённый пользователем пароль
    """
    if not any(login == user[0] for user in users):
        password_check = input("Введите пароль повторно: ")

        if password_check == password:
            print("Вы продавец (1) или покупатель (2)?")

            try:
                choice = int(input())
            except ValueError:
                print("Введено неверное значение!")
                main()

            if choice == 1:
                Buyer(login=login, password=password, registration=True)
            elif choice == 2:
                Seller(login=login, password=password, registration=True)

            else:
                print("Введено неверное значение операции!")
                main()
        else:
            print("Введённые пароли не совпадают!")
            main()

    else:
        print("Пользователь с таким именем уже зарегистрирован.")
        authentication(users=users, login=login, password=password)


class User:
    def __init__(self, login: str, password: str):
        """
        Конструктор класса User, атрибуты класса - логин и пароль для регистрации пользователя и дальнейшем сохранении
        для аутентификации
        :param login: введённый пользователем логин
        :param password: введённый пользователем пароль
        """
        self.__login = login
        self.__password = password

    def registration(self):
        """
        Функция регистрации пользователя - сохраняет логин, захэшированный пароль, соль и роль нового пользователя в базе данных, вызывается
        только из конструкторов подклассов Admin, Seller и Buyer класса User
        """
        salt = uuid.uuid4().hex
        hash_password = hashlib.sha256(self.password.encode() + salt.encode())
        hash_password = hash_password.hexdigest()

        new_user = [self.login, hash_password, self.role, salt]


        with open("users.csv", 'a', newline='') as csv_file:
            csv_write = csv.writer(csv_file)
            csv_write.writerow(new_user)

        csv_file.close()
        print("Вы успешно зарегистрировались!")

    @staticmethod
    def visualization():
        """
        Функция прочитывает базу данных пользователей и выводит её в форме сортированной по названию таблицы с помощью
        библиотеки tabulate (заголовки, индексы, центрирование)
        """
        users = []

        with codecs.open("users.csv", 'r', encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)

            for row in csv_reader:
                users.append(row)

        csv_file.close()

        users = sorted(users, key=lambda x: x[0])
        headers = ["Логин", "Пароль", "Роль", "Соль пароля"]
        print(tabulate(users, headers=headers, tablefmt="grid", showindex=True, stralign='center'))

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, login):
        self.__login = login

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password


class Seller(User):
    def __init__(self, login: str, password: str, registration: bool):
        """
        Конструктор подкласса Seller класса User - представляет собой функционал обычного пользователя: регистрация,
        показ таблицы товаров
        :param login: введённый пользователем логин
        :param password: введённый пользователем пароль
        :param registration: флаг регистрации зависит от выбора в главном меню (функции main)
        """
        super().__init__(login, password)
        self.__role = "seller"
        if registration:
            self.registration()
        print("Вы вошли в личный кабинет продавца. Скоро здесь появится функционал для данной роли пользователя.")

    @property
    def role(self):
        return self.__role


class Buyer(User):
    def __init__(self, login: str, password: str, registration: bool):
        """
        Конструктор подкласса Buyer класса User - представляет собой функционал обычного пользователя: регистрация,
        показ таблицы товаров
        :param login: введённый пользователем логин
        :param password: введённый пользователем пароль
        :param registration: флаг регистрации зависит от выбора в главном меню (функции main)
        """
        super().__init__(login, password)
        self.__role = "buyer"
        if registration:
            self.registration()
        print("Вы вошли в личный кабинет покупателя. Скоро здесь появится функционал для данной роли пользователя.")

    @property
    def role(self):
        return self.__role



class Admin(User):
    def __init__(self, login: str, password: str):
        """
        Конструктор подкласса Admin класса User - представляет собой функционал супер-пользователя: регистрация,
        показ и редактирование значений таблицы пользователей
        :param login: введённый пользователем логин
        :param password: введённый пользователем пароль
        """
        super().__init__(login, password)
        self.__role = "admin"
        print("Личный кабинет администратора.")
        self.visualization()
        self.change_lobby()

    def change_lobby(self):
        """
        Функция считывает базу данных пользователей и позволяет супер-пользователю сделать выбор:
        1 - Редактирование пользователей
        4 - Выход в главное меню
        """
        users = []

        with codecs.open("users.csv", 'r', encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                users.append(row)

        users = sorted(users, key=lambda x: x[0])

        csv_file.close()

        print("Выберите действие: \n 1 - Редактирование пользователей.\n 2 - Выход в главное меню.")

        choice = int(input())

        if choice == 1:
            self.users_edit(users=users)
        elif choice == 2:
            main()

    def users_edit(self, users: []):
        """
        Функция позволяет выбрать ячейку отображённой таблицы для изменения её значения и изменить значение выбранной
        ячейки
        :param users: база данных пользователей (логин, пароль, роль, соль пароля)
        """
        print("Выберите столбец для изменения: \n 1 - Логин\n 2 - Пароль\n 3 - Роль\n 4 - Соль пароля")
        try:
            column = int(input())
        except ValueError:
            print("Введено неверное значение для столбца!")
            self.users_edit(users=users)
        try:
            row = int(input("Выберите строку для изменения: "))
        except ValueError:
            print("Введено неверное значение для строки!")
            self.users_edit(users=users)

        print(f"Изменяемое значение: {users[row][column - 1]}")
        users[row][column - 1] = input("Введите новое значение: ")

        if users[row][column - 1] == "":
            users[row][column - 1] = "null"

        self.users_save(users=users)


    def users_save(self, products: []):
        """
        Функция сохраняет значения базы данных пользователей после изменения значения ячейки выведенной таблицы или удаления
        строки из базы данных
        :param products: база данных товаров (логин, пароль, роль, соль пароля)
        """
        with codecs.open("users.csv", 'w', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(users)
        csv_file.close()

        self.visualization()
        self.change_lobby()


if __name__ == "__main__":
    main()