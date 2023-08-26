# import os
from colorama import init, Fore
from config_pb import Name, Phone, Birthday, Record, AddressBook
from sanitaze_phone_number import sanitaze_phone_number as sphn


address_book = AddressBook()


def handler_com_add(name: str, phone: str, *args):
    # record = Record(Name(name))
    # record.add_phone(Phone(phone))
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    print(f"Contact {name} with number {phone} was successfully added.")


def handler_com_add_birthday(name: str, birthday: str, *args):
    record = Record(name)
    record.add_birthday(birthday)
    address_book.save_birthday(record)
    print(f"Birthday {birthday} was successfully added to Contact {name}.")


def handler_com_day_to_birthday(name: str, *args):
    address_book.show_day_to_birthday(name)


def handler_com_change(name: str, phone: str, *args):
    print(f"Contact {name} with number {phone} was successfully changed.")


def handler_com_remove(name: str, phone: str, *args):
    address_book.edit_record(name, phone)
    print(f"Phone number {phone} from contact {name} was successfully removed.")


def handler_com_phone(name: str, *args):
    address_book.show_record(name)


def handler_com_showall(*args):
    init(autoreset = True)
    print(Fore.YELLOW + "Current list of all contacts:")
    address_book.show_addressbook(address_book)


def handler_com_help(*args):
    init(autoreset = True)
    introduse = "This is pocket phonebook.\n" \
                "For exit write [\"close\", \"exit\", \"goodbye\"].\n" \
                "Available Commands [\"add Name Phone\", \"change Name Phone\", \"help\", \"phone Name\",\n" \
                "\"remove Name Phone\", \"showall\", \"birthday Name dd/mm/yyyy\", \"day Name\"]."
    print(Fore.YELLOW + introduse)


def handler_com_exit(*args):
    init(autoreset = True)
    print(Fore.YELLOW + "Good bye!")


COMMANDS = {"add": handler_com_add, "change": handler_com_change, "close": handler_com_exit,\
            "exit": handler_com_exit, "goodbye": handler_com_exit, "help": handler_com_help,\
            "phone": handler_com_phone, "remove": handler_com_remove, "showall": handler_com_showall,
            "birthday": handler_com_add_birthday, "day": handler_com_day_to_birthday}


def input_error(get_handler):
    def wrapper(*args, **kwargs):
        try:
            error = command_validator(*args, **kwargs)
            if error:
                raise error
            else:
                return get_handler(*args, **kwargs)
        except KeyError:
            init(autoreset = True)
            print(Fore.YELLOW + "Oops! Key Error.\n" \
                  "Wrong command. Please, enter the correct Command.")
        except ValueError:
            init(autoreset = True)
            print(Fore.YELLOW + "Oops! Value Error. \n" \
                  "Invalid command parameters. Please, enter valid Name or Phone [Birthday].")
        except IndexError:
            init(autoreset = True)
            print(Fore.YELLOW + "Oops! Index Error.\n" \
                  "Command parameters are missing. Please, enter correct parameters (Name or Phone).")
    return wrapper


@input_error
def get_handler(command: str, name: str, phone: str):
    return COMMANDS[command](name, phone)


def command_validator(command, name, value):    # з командою [birthday] приходить "dd/mm/yyyy"
    if command not in COMMANDS:
        error = KeyError
    elif command in ("add", "change", "remove", "birthday") and (name is None or value is None):
        error = IndexError
    elif command == "phone" and name is None:
        error = IndexError
    elif command in ("add", "change", "remove") and not (name.isalpha() and value.isdigit() and len(value) >= 10):
        error = ValueError
    elif command in ("change", "phone", "remove") and name not in address_book:
        error = ValueError
    elif command == "birthday" and len(value) != 10:
        error = ValueError
    else:
        error = None
    return error


def command_parser(command_input: str) -> tuple:
    command_split = command_input.strip().split()
    if len(command_split) == 1:
        command = command_split[0].lower()
        return command, None, None
    elif len(command_split) == 2:
        command = command_split[0].lower()
        name = command_split[1].lower().title() if len(command_split[1]) > 2 else None
        return command, name, None
    elif len(command_split) >= 3:
        if "/" in command_split[2]:
            command = command_split[0].lower()
            name = command_split[1].lower().title() if len(command_split[1]) > 2 else None
            birthday = command_split[2] if len(command_split[2]) == 10 else None
            return command, name, birthday
        else:
            command = command_split[0].lower()
            name = command_split[1].lower().title() if len(command_split[1]) > 2 else None
            phone = command_split[2] if len(command_split[2]) >= 10 else None
            sanitazed_phone = sphn(phone)
            return command, name, sanitazed_phone


def main():
    file_name = "phonebook.json"
    address_book.open_addressbook(file_name)
    
    init(autoreset = True)
    # let_begin = "Please, choose command \"help\" for begin"
    print(Fore.YELLOW + "Please, choose command \"help\" for begin")
        
    while 1:
        command_input = input("Common your command: ")
        
        if not command_input:
            continue
        
        (command, name, value) = command_parser(command_input)
        get_handler(command, name, value)
        
        if command in ("exit", "close", "goodbye"):
            address_book.close_addressbook(file_name)  
            break


if __name__ == "__main__":  
    main()