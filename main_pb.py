from colorama import init, Fore
from config_pb import Name, Phone, Birthday, Record, AddressBook


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


def handler_com_change(name: str, phone_old: str, phone_new: str, *args):
    address_book.edit_record("change", name, phone_old, phone_new)
    print(f"Contact {name} with number {phone_new} was successfully changed.")


def handler_com_remove(name: str, phone: str, *args):
    address_book.edit_record("remove", name, phone)
    print(f"Phone number {phone} from contact {name} was successfully removed.")


def handler_com_info(name: str, *args):
    address_book.show_record(name)


def handler_com_showall(*args):
    init(autoreset = True)
    print(Fore.YELLOW + "Current list of all contacts:")
    address_book.show_addressbook(address_book)


def handler_com_search(search_fragment, *args):
    address_book.search_record(search_fragment)


def handler_com_help(*args):
    init(autoreset = True)
    introduse = "This is pocket phonebook.\n" \
                "For exit write [\"close\", \"exit\", \"goodbye\"].\n" \
                "Available Commands:\n" \
                "[\"add NAME PHONE\", \"change NAME OLD-PHONE NEW-PHONE\", \"remove NAME PHONE\",\n" \
                "\"search NAME[PHONE]\", \"info NAME\", \"showall\", \"help\",\n" \
                "\"birthday[add] NAME dd/mm/yyyy\", \"day NAME\"]."
    print(Fore.YELLOW + introduse)


def handler_com_exit(*args):
    init(autoreset = True)
    print(Fore.YELLOW + "Good bye!")


COMMANDS = {"add": handler_com_add, "change": handler_com_change, "close": handler_com_exit,\
            "exit": handler_com_exit, "goodbye": handler_com_exit, "help": handler_com_help,\
            "info": handler_com_info, "remove": handler_com_remove, "showall": handler_com_showall,\
            "search": handler_com_search, "birthday": handler_com_add_birthday, "day": handler_com_day_to_birthday}


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
def get_handler(command, arg1, arg2, arg3):
    return COMMANDS[command](arg1, arg2, arg3)


def command_validator(command, arg1, arg2, arg3):    # з командою [birthday] приходить "dd/mm/yyyy"
    if command not in COMMANDS:
        error = KeyError
    elif command == "change" and (arg1 is None or arg2 is None or arg3 is None):
        error = IndexError
    elif command in ("add", "change", "remove", "birthday") and (arg1 is None or arg2 is None):
        error = IndexError
    elif command in ("phone", "search") and arg1 is None:
        error = IndexError
    elif command in ("change", "phone", "remove") and arg1 not in address_book:
        error = ValueError
    elif command == "search" and not (arg1.isalpha() or arg1.isdigit()):
        error = ValueError
    elif command == "remove" and not (arg2.isdigit() and len(arg2) >= 10):
        error = ValueError
    elif command == "change" and not (arg2.isdigit() and len(arg2) >= 10 and arg3.isdigit() and len(arg3) >= 10):
        error = ValueError
    # elif command == "add" and not arg1.isalpha():
    #     error = ValueError
    # elif command == "add" and not (arg2.isdigit() and len(arg2) >= 10):
    #     error = ValueError
    # об'єднання попередніх двох умов у одну
    elif command == "add" and (not arg1.isalpha() or not (arg2.isdigit() and len(arg2) >= 10)):
        error = ValueError
    elif command == "birthday" and not ("/" in arg2 and len(arg2) == 10):
        error = ValueError
    else:
        error = None
    return error


def command_parser(command_input: str) -> tuple:
    command_split = command_input.split()
    command = command_split[0].lower() if len(command_split) > 0 else None
    arg1 = command_split[1].lower().title() if len(command_split) > 1 else None
    arg2 = command_split[2] if len(command_split) > 2 else None
    arg3 = command_split[3] if len(command_split) > 3 else None
    return command, arg1, arg2, arg3


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
        
        (command, arg1, arg2, arg3) = command_parser(command_input)
        get_handler(command, arg1, arg2, arg3)
        
        if command in ("exit", "close", "goodbye"):
            address_book.close_addressbook(file_name)  
            break


if __name__ == "__main__":  
    main()