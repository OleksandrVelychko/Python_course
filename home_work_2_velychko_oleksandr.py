import random
import pprint
import re
from collections import Counter

# 1) Сгенерировать dict() из списка ключей ниже по формуле
# (key : key* key).keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] ожидаемый результат: {1: 1, 2: 4, 3: 9 …}

keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# using dictionary comprehension
dict_1 = {x: x*x for x in keys}

# via iterating through the elements of list:
dict_2 = {}
for i in keys:
    dict_2[i] = i*i

# using zip function and list comprehension
dict_zip = dict(zip(keys, [x*x for x in keys]))
print(f"\nTask 1. Generated dictionaries using 3 methods:\n\t\
dict comprehension: {dict_1}\n\titeration: {dict_zip}\n\tzip: {dict_zip}")


# 2) Сгенерировать массив(list()). Из диапазона чисел от 0 до 100 записать в результирующий массив только четные числа. 
even_numbers = [x for x in range(101) if x % 2 == 0]
print(f"\nTask 2. Even numbers from 0 to 100: \n{even_numbers}")


# 3)Заменить в произвольной строке согласные буквы на гласные.  
def replace_consonants(text):
    """Replaces every consonant letter in given text with random lower-case vowel"""
    vowels = 'aeiou'
    for ch in text:
        if ch.isalpha() and ch.lower() not in vowels:
            text = text.replace(ch, random.choice(vowels))
    return text


test_string = 'ABbOosdE!@#%^&*()RZGdfu1234!!!'
print(f"\nTask 3. Replacing consonants from {test_string} with random vowels:\
        \n{replace_consonants(test_string)}")

# 4)Дан массив чисел. [10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1] 
# 4.1) убрать из него повторяющиеся элементы
# 4.2) вывести 3 наибольших числа из исходного массива
# 4.3) вывести индекс минимального элемента массива
# 4.4) вывести исходный массив в обратном порядке 

init_numbers = [10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]
unique_numbers = list(set(init_numbers))
max_3_numbers = sorted(init_numbers)[-3:]
min_elems_indexes = [i for i, x in enumerate(init_numbers) if x == min(init_numbers)]
reversed_numbers = list(reversed(init_numbers))

print(f"\nTask 4.1. unique_numbers {unique_numbers}")
print(f"\nTask 4.2. 3 max values from initial list: {max_3_numbers}")
print(f"\nTask 4.3. Index(es) of MIN value element(s) from initial list: {min_elems_indexes}")
print(f"\nTask 4.4. Initial list in reversed order: {reversed_numbers}")


# 5) Найти общие ключи в двух словарях: 
dict_one = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
dict_two = {'a': 6, 'b': 7, 'z': 20, 'x': 40}

# simple way to find common keys
common_keys = list(dict_one.keys() & dict_two.keys())
print(f"\nTask 5. Common keys in two dictionaries are {common_keys}")

# using intersection method for sets created from dictionaries
common_keys2 = []
for k in set(dict_one).intersection(set(dict_two)):
    common_keys2.append(k)
print(f"\n\tAnother way to get common keys via intersection method gives {common_keys2}")


# 6)Дан массив из словарей 
# data = [
#     {'name': 'Viktor', 'city': 'Kiev', 'age': 30 },
#     {'name': 'Maksim', 'city': 'Dnepr', 'age': 20},
#     {'name': 'Vladimir', 'city': 'Lviv', 'age': 32},
#     {'name': 'Andrey', 'city': 'Kiev', 'age': 34},
#     {'name': 'Artem', 'city': 'Dnepr', 'age': 50},
#     {'name': 'Dmitriy', 'city': 'Lviv', 'age': 21}]

# 6.1) отсортировать массив из словарей по значению ключа ‘age' 
# 6.2) сгруппировать данные по значению ключа 'city' 
# вывод должен быть такого вида :
# result = {
#    'Kiev': [
#       {'name': 'Viktor', 'age': 30 },
#       {'name': 'Andrey', 'age': 34}],
#
#    'Dnepr': [ {'name': 'Maksim', 'age': 20 },
#               {'name': 'Artem', 'age': 50}],
#    'Lviv': [ {'name': 'Vladimir', 'age': 32 },
#              {'name': 'Dmitriy', 'age': 21}]
# }
# =======================================================

data = [
    {'name': 'Viktor', 'city': 'Kiev', 'age': 30},
    {'name': 'Maksim', 'city': 'Dnepr', 'age': 20},
    {'name': 'Vladimir', 'city': 'Lviv', 'age': 32},
    {'name': 'Andrey', 'city': 'Kiev', 'age': 34},
    {'name': 'Artem', 'city': 'Dnepr', 'age': 50},
    {'name': 'Dmitriy', 'city': 'Lviv', 'age': 21}]

data_sorted_by_age = sorted(data, key=lambda x: x['age'])
print("\nTask 6.1. Data sorted by age:\n")
my_printer = pprint.PrettyPrinter(width=80, sort_dicts=False)
my_printer.pprint(data_sorted_by_age)

def group_data_by(grouper):
    #grouper_val = 'city'
    group_keys = []
    for i in data:
        if i[grouper] not in group_keys:
            group_keys.append(i[grouper])

    grouped_dict = {}
    for x in group_keys:
        temp_values_list = []
        for j in data:
            if j[grouper] == x:
                t = dict(j)
                del t[grouper]
                temp_values_list.append(t)
        grouped_dict[x] = temp_values_list
    return grouped_dict


group_by_city = group_data_by('city')
print('\nTask 6.2. Data grouped by city:\n')
my_printer = pprint.PrettyPrinter(width=60, sort_dicts=False)
my_printer.pprint(group_by_city)


# 7) У вас есть последовательность строк.
# Необходимо определить наиболее часто встречающуюся строку в последовательности.
# Например:
# most_frequent(['a', 'a', 'bi', 'bi', 'bi']) == 'bi'


def most_frequent(list_var):
        """Case-sensitive. I.e., 'a' and 'A' are considered to be different items
            Use [0][0] index to retrieve the most frequent item, otherwise
            function returns value with number of occurences in passed value
        """
        res = Counter(list_var).most_common(1)
        return res[0][0]

frequent_res = most_frequent(['a', 'a', 'bi', 'bi', 'bi'])
print(f"\nTask 7. Most frequent item in the list is: {frequent_res}\n")


def most_frequent_m_set(list_var):
    res = max(set(list_var), key=list_var.count)
    return res

frequent_res_2 = most_frequent_m_set(['a', 'a', 'bi', 'bi', 'bi', 'bi'])
print(f"\tAnother way using set and count: {frequent_res_2}\n")


# =======================================================
# 8) Дано целое число. Необходимо подсчитать произведение всех цифр в этом числе, за исключением нулей.
# Например:
# Дано число 123405. Результат будет: 1*2*3*4*5=120.

def get_digits_product(numb):
    """Function accepts both int and str but will work only in case
        it numb contain digits only"""
    prod = None
    if isinstance(numb, int):
        print(isinstance(numb, int))
        numb = str(numb)
    if not numb.isdigit():
        print('Task 8. Please, pass int number (digits only) to this function')
        exit()
    for x in numb:
        digit = int(x)
        if prod == None:
            prod = digit
            continue
        if digit == 0:
            continue
        prod *= digit
    return prod


numb = '123405'
product = get_digits_product(numb)
print(f"Task 8. Product value for {numb} is {product}")


# =======================================================
# 9) Есть массив с положительными числами и число n (def some_function(array, n)).
# Необходимо найти n-ую степень элемента в массиве с индексом n. Если n за границами массива, тогда вернуть -1.

def get_array_elem_pow(array, n):
    """ Find n power of the array element with index n.
        Pass array as a list or tuple or a string with delimiters: .,/ -:
        Function returns -1 in case n value is greater or equal than array's length
        """
    if isinstance(array, str):
        array = list(map(int, re.split(" *[/s+ +.,:-] *", array)))

    if isinstance(array, list) or isinstance(array, tuple):
        if n >= len(array):
            print(f"\nTask 9. Index is out of range. N max value should be {len(array)-1}")
            return -1
        else:
            result = array[n] ** n
            print(f"\nTask 9. {array[n]}^{n} = {result}")
            return result

#arr = '1, 2, 3, 4'
#arr = '1 2 3 4'
#arr = '1-2-3-4'
#arr = '1/2/3/4'
arr = [1, 4, 8, 16, 10]
n = 3
power = get_array_elem_pow(arr, n)


# =======================================================
# 10) Есть строка со словами и числами, разделенными пробелами (один пробел между словами и/или числами).
# Слова состоят только из букв. Вам нужно проверить есть ли в исходной строке три слова подряд.
# Для примера, в строке "hello 1 one two three 15 world" есть три слова подряд.

def get_three_words(text):
    words = re.findall(r'\w+', text.lower())
    words_count = 0
    for x in range(len(words)):
        if words[x].isalpha():
            words_count += 1
            if words_count == 3:
                index = x
                print('\nTask 10. Bingo! Your string contains 3 words in a row')
                return words[index-2: index+1]
        else:
            words_count = 0
    print('\nTask 10. Sorry, but there are no 3 words in a row in your string')
    return False


# my_string = "hello 1 one two 3333 three 15 world"
my_string = "hello 1 one two three 15 world"
result_10 = get_three_words(my_string)
print(result_10)
