from functools import wraps

# ЗАДАЧА-1
# Написать свой декоратор который будет проверять остаток от деления числа 100 на результат работы функции ниже.
# Если остаток от деления = 0, вывести сообщение "We are OK!», иначе «Bad news guys, we got {}» остаток от деления.


def check_remainder_of_division(func):
    @wraps(func)
    def inner(divisor):
        result = func(divisor)
        print(f"\nDivision of 100 by {divisor}: {100//divisor} and remainder is {result}")
        if not result:
            msg = 'We are OK!'
        else:
            msg = f"Bad news guys, we got {result}"
        return msg
    return inner


@check_remainder_of_division
def divide_100_by(divisor):
    return 100 % divisor


print("\nTask 1. Remainder of division of 100 by divisor passed as argument")
print(divide_100_by(26))
print(divide_100_by(25))


# ЗАДАЧА-2
# Написать декоратор который будет выполнять предпроверку типа аргумента который передается в вашу функцию.
# Если это int, тогда выполнить функцию и вывести результат, если это str(),
# тогда зарейзить ошибку ValueError (raise ValueError(“string type is not supported”))


def check_type(func):
    @wraps(func)
    def inner(n):
        arg = n
        if isinstance(n, int):
            result = func(n)
        elif isinstance(n, str):
            raise ValueError("string type is not supported")
        return result
    return inner


@check_type
def fibonacci(n):
    num = 1
    if n > 2:
        num = fibonacci(n-1) + fibonacci(n-2)
    return num


print("\nTask 2. Decorator pre-checking type of an argument passed to the function\n")
print(f"Your Fibonacci number is {fibonacci(7)}\n")
# fibonacci('5')


# ЗАДАЧА-3
# Написать декоратор который будет кешировать значения аргументов и результаты работы вашей функции и записывать
# его в переменную cache. Если аргумента нет в переменной cache и функция выполняется, вывести сообщение
# «Function executed with counter = {}, function result = {}» и количество раз сколько эта функция выполнялась.
# Если значение берется из переменной cache, вывести сообщение «Used cache with counter = {}» и
# количество раз обращений в cache.


def count_calls(func):
    cache = {}

    @wraps(func)
    def inner(*args, **kwargs):
        key = args
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            inner.f_calls += 1
            print(f"Function executed with counter = {inner.f_calls} and result = {cache[key]}.")
            return cache[key]
        else:
            inner.cache_calls += 1
            print(f"Used cache with counter = {inner.cache_calls} and result = {cache[key]}.")
        return cache[key]
    inner.f_calls = 0
    inner.cache_calls = 0
    return inner


@count_calls
def capitalize_word(word):
    return word.capitalize()


print("\nTask 3. Decorator caching arguments and function results\n")
test_words = ['soul', 'banana', 'ship', 'apple', 'ship', 'sun', 'sun', 'priest', 'priest']
print(list(map(capitalize_word, test_words)))
print('-'*30)
test_words.append('new')
print('\nNow calling the same function to see that cache is used for all cases except of a new word:\n')
for x in range(len(test_words)):
    capitalize_word(test_words[x])
