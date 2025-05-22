

from collections import UserDict
from datetime import datetime, timedelta 
import pickle  

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Ten signs are expected")
        

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
            
       

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # реалізація класу
    def add_phone(self, number_phone):
        phone = Phone(number_phone)
        self.phones.append(phone)

    def remove_phone(self, number_phone):
        self.find_phone(number_phone)
        return self.phones.remove(number_phone)
    

    def edit_phone(self, number_phone, new_number_phone):
        phone = self.find_phone(number_phone)
        if phone:
            self.add_phone(new_number_phone)
            self.phones.remove(phone)
        else:
            raise ValueError("Enter the phone number again") 
           


    def find_phone(self, number_phone):
        for phone in self.phones:
            if phone.value == number_phone:
                return phone   
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        birthday = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"{self.name.value}: {phones}{birthday}"    


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find (self, name):
        return self.data.get(name)


    def delete (self, name):
        del self.data[name]



    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if not record.birthday:
                continue 
            bday = record.birthday.value
            try:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            except ValueError:
                continue
            birthday_this_year = bday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year =bday.replace(year=today.year + 1)
            

            if 0 <= (birthday_this_year - today).days <= 7:
                greet_day = birthday_this_year
                if greet_day.weekday() >= 5:
                    greet_day += timedelta(days=(7 - greet_day.weekday()))
                upcoming.append({"name": record.name.value, "birthday": greet_day.strftime("%d.%m.%Y")})
        return upcoming
            
      
            


    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command" 
        except KeyError:
            return "Invalid argument entered for command"
        except IndexError:
            return "Enter the name after command" 

    return inner



def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 


def parse_input(user_input):
    if len(user_input) == 0:
        return " "
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args



@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    message = "Contact added."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old, new = args
    record = book.find(name)
    record.edit_phone(old, new)
    return "Change contact"

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return "".join(phone.value for phone in record.phones)


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added"


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday.value}"
    elif record:
        return f"{name} has no birthday set."
    return "Contact not found"


@input_error
def birthdays(_, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays this week."
    return "\n".join(f"{el['name']}: {el['birthday']}" for el in upcoming)

def all_contact(_, book):
    return "\n".join(str(record) for record in book.data.values())

   
def main():
    # book = AddressBook()
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command == " ":
            print("Not command")

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "all":
            print(all_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))
       
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()