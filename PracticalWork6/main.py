import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from colorama import Fore, Style

# Подключение к локальному блокчейну (ganache)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

with open('contract_abi.json', 'r') as f:
    contract_abi = json.load(f)

# Адрес смарт-контракта
contract_address = Web3.to_checksum_address("0xA6834842B725c52fCd7249C89aFF9382e2d64563")
# Создание экземпляра смарт-контракта
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def safe_input_string(prompt):
    while True:
        try:
            value = input(prompt)
            return str(value)
        except ValueError:
            print(Fore.RED + "Ошибка ввода. Введите строку." + Style.RESET_ALL)


def safe_input_number(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print(Fore.RED + "Ошибка ввода. Введите число." + Style.RESET_ALL)


# Адрес банка
bank_address = '0x889c51d52EaF04F86564D8E95f9C7d298E2B4f37'

# Адреса админов, магазинов и покупателей (пример)
admin_address = '0x11614E973B933e8EcE811a79a37e6c2912f144c8'
shop_address = '0x502F436DE88F1F049bA474c971000FBf3318E397'
seller_address = '0x68072E71Dc958A2ddb8FDDE2fc78F8Cc8f9adE00'
buyer_address = '0xc1b798c323759046A1CC56E5d085f914a5eD1810'

current_address = ""


def register_user(role, login, full_name, sender):
    try:
        tx_hash = contract.functions.registerUser(role, login, full_name).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("User registration successful.")
        print(f"Two-factor code: {contract.functions.checkCode().call({'from': sender})}")
    except Exception as e:
        print(Fore.RED + "User registration failed:", str(e) + Style.RESET_ALL)


def register_shop(login, full_name, sender):
    try:
        tx_hash = contract.functions.registerShop(login, full_name).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Shop registration successful.")
        print(f"Two-factor code: {contract.functions.checkCode().call({'from': sender})}")
    except Exception as e:
        print(Fore.RED + "Shop registration failed:", str(e) + Style.RESET_ALL)


def generate_two_factor_code():
    try:
        return contract.functions.generateTwoFactorCode().call()
    except Exception as e:
        print(Fore.RED + "Error generating two-factor code:", str(e) + Style.RESET_ALL)


def add_admin(admin, login, full_name, sender):
    try:
        tx_hash = contract.functions.addAdmin(admin, login, full_name).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Admin added successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to add admin:", str(e) + Style.RESET_ALL)


def remove_shop(shop, sender):
    try:
        tx_hash = contract.functions.removeShop(shop).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Shop removed successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to remove shop:", str(e) + Style.RESET_ALL)


def get_admin_list():
    try:
        return contract.functions.getAdminList().call()
    except Exception as e:
        print(Fore.RED + "Error retrieving admin list:", str(e) + Style.RESET_ALL)


def get_seller_list():
    try:
        return contract.functions.getSellerList().call()
    except Exception as e:
        print(Fore.RED + "Error retrieving seller list:", str(e) + Style.RESET_ALL)


def login(sender, two_factor_code):
    try:
        login = contract.functions.login(two_factor_code).call({'from:': sender})
        print("You logged as: " + login)
        return login
    except Exception as e:
        print(Fore.RED + "Login failed:", str(e) + Style.RESET_ALL)


def get_balance():
    try:
        return contract.functions.getBalance().call()
    except Exception as e:
        print(Fore.RED + "Error retrieving balance:", str(e) + Style.RESET_ALL)


def change_user_role(user, new_role, sender):
    try:
        tx_hash = contract.functions.changeUserRole(user, new_role).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("User role changed successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to change user role:", str(e) + Style.RESET_ALL)


def switch_seller_to_buyer_role(sender):
    try:
        tx_hash = contract.functions.switchSellerToBuyerRole().transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("User role switched to buyer successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to switch user role to buyer:", str(e) + Style.RESET_ALL)


def add_complaint(shop, comment, rating, sender):
    try:
        tx_hash = contract.functions.addComplaint(shop, comment, rating).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Complaint added successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to add complaint:", str(e) + Style.RESET_ALL)


def add_comment(complaint_id, comment, sender):
    try:
        tx_hash = contract.functions.addComment(complaint_id, comment).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Comment added successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to add comment:", str(e) + Style.RESET_ALL)


def add_like(complaint_id, sender):
    try:
        tx_hash = contract.functions.addLike(complaint_id).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Like added successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to add like:", str(e) + Style.RESET_ALL)


def add_dislike(complaint_id, sender):
    try:
        tx_hash = contract.functions.addDislike(complaint_id).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Dislike added successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to add dislike:", str(e) + Style.RESET_ALL)


def add_confirmation(complaint_id, sender):
    try:
        tx_hash = contract.functions.addConfirmation(complaint_id).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Confirmation added successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to add confirmation:", str(e) + Style.RESET_ALL)


def add_refutation(complaint_id, sender):
    try:
        tx_hash = contract.functions.addRefutation(complaint_id).transact({'from': sender})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Refutation added successfully.")
    except Exception as e:
        print(Fore.RED + "Failed to add refutation:", str(e) + Style.RESET_ALL)


def get_complaint(complaint_id, sender):
    try:
        return contract.functions.getComplaint(complaint_id).call()
    except Exception as e:
        print(Fore.RED + "Error retrieving complaint:", str(e) + Style.RESET_ALL)


w3.eth.default_account = admin_address


def main():
    while True:
        print(
            'В рамках данной платформы вы можете сделать следующее: \n 1 - Войти\n 2 - Зарегистрироваться\n 3 - '
            'Просмотреть книгу Жалоб и предложений\n 4 - Выйти')
        command = safe_input_number("Выберите действие: ")

        if command == 1:
            msg = login(safe_input_string("Введите адрес пользователя: "),
                        safe_input_number("Введите код двухфакторной авторизации (для сохранённых аккаунтов - 0): "))
            print(msg)
            menu()
        elif command == 2:
            current_address = safe_input_string("Введите адрес: ")
            register_user("admin", safe_input_string("Введите логин пользователя: "),
                          safe_input_string("Введите ФИО пользователя: "), current_address)
        elif command == 3:
            get_complaint(safe_input_number("Введите номер записи в книге: "), admin_address)
        elif command == 4:
            break
        else:
            print("Неверная команда.")


def menu():
    while True:
        print(Fore.CYAN + "==== МЕНЮ ====" + Style.RESET_ALL)
        print("1. Получить список администраторов")
        print("2. Получить список продавцов")
        print("3. Получить баланс")
        print("4. Изменить роль пользователя")
        print("5. Переключиться на роль покупателя")
        print("6. Добавить жалобу")
        print("7. Добавить комментарий")
        print("8. Добавить лайк")
        print("9. Добавить дизлайк")
        print("10. Добавить подтверждение")
        print("11. Добавить опровержение")
        print("12. Получить жалобу")
        print("0. Выход")

        choice = input("Введите ваш выбор: ")

        if choice == "1":
            admin_list = get_admin_list()
            print("Список администраторов:", admin_list)
        elif choice == "2":
            seller_list = get_seller_list()
            print("Список продавцов:", seller_list)
        elif choice == "3":
            balance = get_balance()
            print("Баланс:", balance)
        elif choice == "4":
            user_address = input("Введите адрес пользователя: ")
            new_role = input("Введите новую роль: ")
            change_user_role(user_address, new_role, current_address)
        elif choice == "5":
            switch_seller_to_buyer_role(current_address)
        elif choice == "6":
            shop = input("Введите адрес магазина: ")
            comment = input("Введите комментарий: ")
            rating = int(input("Введите рейтинг: "))
            add_complaint(shop, comment, rating, current_address)
        elif choice == "7":
            complaint_id = int(input("Введите ID жалобы: "))
            comment = input("Введите комментарий: ")
            add_comment(complaint_id, comment, current_address)
        elif choice == "8":
            complaint_id = int(input("Введите ID жалобы: "))
            add_like(complaint_id, current_address)
        elif choice == "9":
            complaint_id = int(input("Введите ID жалобы: "))
            add_dislike(complaint_id, current_address)
        elif choice == "10":
            complaint_id = int(input("Введите ID жалобы: "))
            add_confirmation(complaint_id, current_address)
        elif choice == "11":
            complaint_id = int(input("Введите ID жалобы: "))
            add_refutation(complaint_id, current_address)
        elif choice == "12":
            complaint_id = int(input("Введите ID жалобы: "))
            complaint = get_complaint(complaint_id, current_address)
            print("Жалоба:", complaint)
        elif choice == "0":
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")


if __name__ == '__main__':
    print("Вас приветствует платформа торговой системы")
    main()
