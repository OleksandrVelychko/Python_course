from re import *

# Задача-1
# Реализовать дескриптор валидации для аттрибута email.
# Ваш дескриптор должен проверять формат email который вы пытаетесь назначить


class InvalidEmailException(Exception):
    pass


class EmailDescriptor:
    def __get__(self, instance, owner):
        return self.email

    def __set__(self, instance, value):
        pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
        if pattern.match(value):
            self.email = value
        else:
            raise InvalidEmailException(f'Specified email address is not valid: {value}')


class MyClass:
    email = EmailDescriptor()


print('\nTask 1. Email attribute validation using descriptor')
my_class = MyClass()
my_class.email = "validemail@gmail.com"
print(f'Valid email is : {my_class.email}')
print(f'\nExpected ValueError exception to be raised for invalid email')
my_class.email = "novalidemail"


# Задача-2
# Реализовать синглтон метакласс(класс для создания классов синглтонов).

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyClass(metaclass=Singleton):
    pass


print('\nTask 2. Singleton using metaclass')
c = MyClass()
b = MyClass()
assert id(c) == id(b)
print(f'c and b are the same instance of MyClass: {id(c) == id(b)}')


# Задача-3
# реализовать дескриптор IngegerField(), который будет хранить уникальные
# состояния для каждого класса где он объявлен

class IngegerField:

    def __init__(self):
        self.storage = {}

    def __get__(self, instance, owner):
        self.number = self.storage.get(id(instance), None)
        if self.number is None:
            raise AttributeError(f'Value is missing for {instance}')
        else:
            return self.number

    def __set__(self, instance, value):
        self.number = value
        self.storage[id(instance)] = value


class Data:
    number = IngegerField()


data_row = Data()
new_data_row = Data()
data_row_3 = Data()

data_row.number = 5
new_data_row.number = 10
data_row_3.number = 2

assert data_row.number != new_data_row.number
assert data_row.number != data_row_3.number
assert data_row_3.number != new_data_row.number
print('\nTask 3. Unique states for different instances\' attributes with descriptor')
print(f'Data 1:  {data_row.number}')
print(f'Data 2:  {new_data_row.number}')
print(f'Data 3:  {data_row_3.number}')
