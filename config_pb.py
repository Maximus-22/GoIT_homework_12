import json
import os
from collections import UserDict
from datetime import datetime


class Field:

    def __init__(self, value: str) -> None:
        self.value = value


class Name(Field):
   
   def __init__(self, name: str) -> None:
        self.name = name


class Phone(Field):

    def __init__(self, phone: str):
        self.__private_phone = ""
        self.phone = phone

    @property
    def phone(self):
        return self.__private_phone
    
    @phone.setter
    def phone(self, phone: str):
        if phone != "" and phone.isdigit() and len(phone) >= 10:
            self.__private_phone = phone
        else:
            raise Exception("You entered an incorrect phone number!\n\
                            The [lenght] of phone number should be >= 10!")


class Birthday(Field):

    def __init__(self, birthday: str):
        self.__private_birthday = ""
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__private_birthday
    
    @birthday.setter
    def birthday(self, birthday: str):
        if birthday != "":
            db_day, db_month, db_year = birthday.split('/')
            if db_day.isdigit() and db_month.isdigit() and db_year.isdigit():
                if 1 <= int(db_day) <= 31 and 1 <= int(db_month) <= 12 and int(db_year) > 1900:
                    self.__private_birthday = birthday
                else:
                    raise Exception("You entered wrong date of birth!\n\
                                     Format date of birth is [dd/mm/yyyy].")
            else:
                raise Exception("You entered wrong date of birth!\n\
                                 Format date of birth is [dd/mm/yyyy].")
        # else:
        #     self.__private_birthday = ""
            # if 1 <= int(db_day) <= 31 and 1 <= int(db_month) <= 12 and int(db_year) > 1900:
            # # if datetime(year = db_year, month = db_month, day = db_day):
            #     self.__private_birthday = birthday
            # else:
            #     raise Exception("You entered wrong date of birth!\n\
            #                     Format date of birth is [dd/mm/yyyy].")


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = Name(name)
        self.phones = [phone] if phone else []
        self.birthday = birthday if birthday else ""

    def add_phone(self, phone: str):
        if phone not in [tel.phone for tel in self.phones]:
        # if phone not in [tel for tel in self.phones]:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        for tel in self.phones:
            if tel.phone == phone:
                self.phones.remove(tel)

    def change_phone(self, old_phone: str, new_phone: str):
        for tel in self.phones:
            if tel.phone == old_phone:
                tel.phone = new_phone

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
        # self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now()
            db_day, db_month, _ = map(int, self.birthday.birthday.split('/'))
            next_birthday = datetime(year = current_datetime.year, month = db_month, day = db_day)
            if current_datetime < next_birthday:
               days_to_birthday = (next_birthday - current_datetime).days
            else:
               next_birthday = next_birthday.replace(year=next_birthday.year + 1)
               days_to_birthday = (next_birthday - current_datetime).days
            return days_to_birthday
        else:
            return None


class AddressBookIterator:

    def __init__(self, address_book):
        self.address_book = address_book
        self.current_index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_index >= len(self.address_book.data):
            raise StopIteration
        else:
            keys = list(self.address_book.data.keys())
            record = self.address_book.data[keys[self.current_index]]
            self.current_index += 1
            return record


class AddressBook(UserDict):

    def __iter__(self):
        return AddressBookIterator(self)

    def add_record(self, record: Record):
        # Record.name -> Record(Name(name)) -> Record.name.name
        # { Record.name.name : Record() }
        if record.name.name in self.data:
            existing_record = self.data[record.name.name]
            for tel in record.phones:
                existing_record.add_phone(tel.phone)
            # existing_record.add_phone(record.phones[0])
        else:
            self.data[record.name.name] = record

    def save_birthday(self, record: Record):
        # Record.name -> Record(Name(name)) -> Record.name.name
        # { Record.name.name : Record() }
        if record.name.name in self.data:
            existing_record = self.data[record.name.name]
            existing_record.add_birthday(record.birthday.birthday)
        else:
            self.data[record.name.name] = record

    def edit_record(self, name, phone):
        if name in self.data:
            record = self.data[name]
            record.remove_phone(phone)

    def show_record(self, name):
        if name in self.data:
            record = self.data[name]
            phones = ", ".join([phone.phone for phone in record.phones])
            print(f"Contact {name} has phone: {phones}")

    def show_day_to_birthday(self, name):
        # Record.name -> Record(Name(name)) -> Record.name.name
        # { Record.name.name : Record() }
        if name in self.data:
            record = self.data[name]
            if record.birthday:
                print(f"{name} was born {record.birthday.birthday}, he (she) birthday will be in {record.days_to_birthday()} days.")
            else:
                print(f"There is no birthday date for {name}.")

    # def show_addressbook(self):
        # for name in sorted(self.data):
        #     record = self.data[name]
        #     phones = ", ".join([phone.phone for phone in record.phones])
        #     print("{:<20} | {:^14} | --> {:<15}".format(name, record.birthday.birthday, phones))
    def show_addressbook(self, address_book):
        iterator = iter(address_book)
        page_size = 10  # Розмір сторінки
        while 1:
            try:
                for _ in range(page_size):
                    record = next(iterator)
                    # Виведення запису
                    print("{:<20} | {:^14} | --> {:<15}".format(record.name.name, 
                                                                record.birthday.birthday if record.birthday else "",
                                                                ", ".join([phone.phone for phone in record.phones])))
            except StopIteration:
                break

    def search_record(self, search_fragment):
        search_record = 0
        for name in sorted(self.data):
            record = self.data[name]
            phones = ", ".join([phone.value for phone in record.phones])
            birthday = record.birthday.value
            if search_fragment.isalpha() and search_fragment.lower() in name.lower():
                print("{:<20} | {:^14} | --> {:<15}".format(name, birthday, phones))
                search_record +=1
            elif search_fragment.isdigit() and search_fragment in phones:
                print("{:<20} | {:^14} | --> {:<15}".format(name, birthday, phones))
                search_record +=1
        if not search_record:
            print("Nothing found!")

    def open_addressbook(self, file_name: str):
        # if os.path.exists(file_name):
        #     with open(file_name, "r", encoding = "UTF-8") as file:
        #         for line in file:
        #             name, file_phones, birthday = line.strip().split(';')
        #             # record = Record(Name(name))
        #             record = Record(name)
        #             for tel in file_phones.split(','):
        #                 record.add_phone(tel)
        #             if birthday:
        #                 record.add_birthday(birthday)
        #             self.add_record(record)
        if os.path.exists(file_name):

            with open(file_name, "r", encoding = "UTF-8") as file:
                restore_data = json.load(file)
            
                for element in restore_data:
                    record = Record(element["name"])
            
                    if element["birthday"]:
                        record.add_birthday(element["birthday"])
            
                    for tel in element["phones"].split(','):
                        record.add_phone(tel)
                    
                    self.add_record(record)

    def close_addressbook(self, file_name: str):
        # with open(file_name, "w", encoding = "UTF-8") as file:
        #     for name in self.data:
        #         record = self.data[name]
        #         phones = ",".join([phone.phone for phone in record.phones])
        #         # file.write(f"{record.name.name};{phones}\n")
        #         # if record.birthday != "":
        #         if record.birthday:
        #             file.write(f"{name};{phones};{record.birthday.birthday}\n")
        #         else:
        #             file.write(f"{name};{phones};\n")
        with open(file_name, "w", encoding = "UTF-8") as file:
            pocket_data = []
            
            for name, record in self.data.items():
                    user_data ={"name": name,
                                "birthday": record.birthday.birthday if record.birthday else "",
                                "phones": ",".join([phone.phone for phone in record.phones])}
                    pocket_data.append(user_data)
            
            json.dump(pocket_data, file, ensure_ascii=False, indent=5)



if __name__ == "__main__":

    address_book = AddressBook()

    file_name = "phonebook.json"
    address_book.open_addressbook(file_name)

    record1 = Record("John")
    record2 = Record("Britny")
    record1.add_birthday("11/11/1991")
    print(record1.birthday.birthday, record1.days_to_birthday())

    record1.add_phone("0976312904")
    record1.add_phone("0563157905")
    record2.add_phone("0508432960")
    record2.add_phone("0732071801")

    record1.change_phone("0976312904", "0673120732")
    record1.remove_phone("0563157905")

    address_book.add_record(record1)
    address_book.add_record(record2)

    record3 = Record("Petro")
    record3.add_phone("0975312570")
    address_book.add_record(record3)

    record4 = Record("Kim")
    record4.add_phone("0976312904")
    record4.add_birthday("03/12/1981")
    address_book.add_record(record4)

    address_book.show_addressbook(address_book)
    address_book.close_addressbook(file_name)

    assert isinstance(address_book["Kim"], Record)
    assert isinstance(address_book["Kim"].name, Name)
    assert isinstance(address_book["Kim"].phones, list)
    assert isinstance(address_book["Kim"].phones[0], Phone)
    assert address_book["Kim"].phones[2].phone == "0976312904"
    assert address_book["Kim"].birthday.birthday == "03/12/1981"