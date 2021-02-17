import re
import pprint
from collections import Counter
from csv import DictWriter


# 1)Из текстового файла удалить все слова, содержащие от трех до пяти символов,
# но при этом из каждой строки должно быть удалено только четное количество таких слов.

def remove_even_words_of_length(src, target, minval, maxval=None):
    """Function takes .txt file (src) and removes even occurences of words with required length per line.
     minval - specifies min length of a word.
     maxval defaults to minval. If specified, length is considered to be [minval, maxval] including border values.
     target - target file to save selected lines to"""
    min_len = minval
    if maxval is None:
        max_len = min_len
    else:
        max_len = maxval
    with open(src, encoding='utf-8') as src_file, open(target, "w+", encoding='utf-8') as target_file:
        for line in src_file:
            full_list = line.split()
            words_to_remove = [word for word in re.findall(r'\w+', line) if
                               min_len <= len(word) <= max_len]
            if len(words_to_remove) % 2:
                words_to_remove = words_to_remove[:len(words_to_remove) - 1]
            line = ' '.join([w for w in full_list if w not in words_to_remove or words_to_remove.remove(w)])
            target_file.writelines(line + '\n')


print('\nTask 1. Delete even number of words consisting of min to max characters from eah line of a text file')
src_file_path_1 = r'text1.txt'
trg_file_path_1 = r'text1_processed.txt'
print(f'\nCheck "{trg_file_path_1}" to see output for source file "{src_file_path_1}"')
remove_even_words_of_length(src_file_path_1, trg_file_path_1, 3, 5)


# 2)Текстовый файл содержит записи о телефонах и их владельцах.
# Переписать в другой файл телефоны тех владельцев, фамилии которых начинаются с букв К и С.

def get_records_by_chars(src, target, *args):
    """Function takes .txt file (src) that contains data about owners (first/last name) and their phone numbers.
    First and Last names in source file should be divided by whitespace. Whitespaces in double names/last names are
    not supported.
    Passed *args arguments may contain letters or substring to select rows with family names starting with them.
    Target - target file to save selected lines to"""

    with open(src, encoding='utf-8') as src_file, open(target, "w+", encoding='utf-8') as target_file:
        for line in src_file:
            owners_list = line.split()
            for arg in args:
                if owners_list[1].lower().startswith(arg.lower()):
                    target_file.writelines(owners_list[2] + '\n')


print('\nTask 2. Copy phone numbers owners ')
src_file_path_phones = r'text2.txt'
trg_file_path_phones = r'text2_processed.txt'
letter_1 = 'k'
letter_2 = 'cA'
print(f'\nCheck "{trg_file_path_phones}" to see output for source file "{src_file_path_phones}"')
get_records_by_chars(src_file_path_phones, trg_file_path_phones, letter_1, letter_2)


# 3) Получить файл, в котором текст выровнен по правому краю путем равномерного добавления пробелов.
def align_text_right(src, target):
    """Function takes .txt file and right-aligns text filling lines with leading spaces"""
    with open(src, encoding='utf-8') as src_file, open(target, "w+", encoding='utf-8') as target_file:
        max_len = len(max(src_file, key=len))
        # re-setting cursor to the beginning of the file with seek() to read src_file lines
        src_file.seek(0)
        for line in src_file:
            if line[-1] != '\n':
                max_len -= 1
            line = line.rjust(max_len)
            target_file.write(line)


print('\nTask 3. Right-align text file via adding whitespaces.')
src_file_path_ra = r'text1.txt'
trg_file_path_ra = r'text3 - right-aligned.txt'
print(f'\nCheck "{trg_file_path_ra}" to see output for source file "{src_file_path_ra}"')
align_text_right(src_file_path_ra, trg_file_path_ra)


# 4)Дан текстовый файл со статистикой посещения сайта за неделю.
# Каждая строка содержит ip адрес, время и название дня недели (например, 139.18.150.126 23:12:44 sunday).
# Создайте новый текстовый файл, который бы содержал список ip без повторений из первого файла.
# Для каждого ip укажите количество посещений, наиболее популярный день недели.
# Последней строкой в файле добавьте наиболее популярный отрезок времени в сутках длиной один час в целом для сайта.

def group_data_by(fdata, grouper):
    """Function takes list of dictionaries (fdata) and groups it by grouper - one of dictionary keys.
    Output - dict of dictionaries with key defined by grouper and values as lists of aggregated dictionaries"""
    group_keys = []
    for i in fdata:
        if i[grouper] not in group_keys:
            group_keys.append(i[grouper])
    grouped_dict = {}
    for x in group_keys:
        temp_values_list = []
        for j in fdata:
            if j[grouper] == x:
                t = dict(j)
                del t[grouper]
                temp_values_list.append(t)
        grouped_dict[x] = temp_values_list
    return grouped_dict


def get_most_popular_period(periods_list):
    """Function accepts list of time periods(hours, days, etc.). Return value is a string that contains 1 period in case
    there is only one most frequent period in periods_list
    or several comma-separated periods with the same frequency as max"""
    periods = dict(Counter(periods_list))
    counter_period = Counter(periods_list).most_common(1)[0][0]
    pop_period = [counter_period]
    for key in periods.keys():
        if key != counter_period and periods[key] == periods[counter_period]:
            pop_period.append(key)
    most_popular_period = ', '.join(p for p in pop_period)
    return most_popular_period


def get_info_by_ip(src, target):
    """Function takes .txt file with info on ip address, visiting time and week day  according to following pattern:
     139.18.150.126 23:12:44 sunday
     Output: created target file with following information:
     unique ip-addresses from src file, number of visits, the most popular day of the week and at the end the most
     popular visiting hour(s) is specified for the whole site (all ip addresses).
     Example:
     IP Address   Visits Day
     139.18.150.126  9   sunday
     The most popular hour(s): 11:00
     """
    with open(src, encoding='utf-8') as src_file:
        # Saving data to ip_data list of dicts
        ip_data = []
        result = []
        for line in src_file:
            line = line.split()
            info_dict = {"ip": line[0], "time": line[1], "day": line[2]}
            ip_data.append(info_dict)
        # my_printer = pprint.PrettyPrinter(width=90, sort_dicts=False)
        # my_printer.pprint(ip_data)
        ip_groups = group_data_by(ip_data, 'ip')
        # my_printer.pprint(ip_groups)
        unique_ip_addr = list(ip_groups.keys())
        # Collecting info on visits and days per IP address
        for ip in unique_ip_addr:
            visits = len(ip_groups[ip])
            # Collecting info on days per ip address
            days = []
            for item in ip_groups[ip]:
                days.append(item['day'])
            popular_day = get_most_popular_period(days)
            output_dict = {"IP Address": ip, "Visits": visits, "Day": popular_day}
            result.append(output_dict)

        # Collecting visits hours data
        visit_hours = []
        for data in ip_data:
            visit_hours.append(data['time'].split(':')[0] + ':00')
        popular_hour = get_most_popular_period(visit_hours)

    with open(target, "w+", encoding='utf-8') as target_file:
        dict_writer = DictWriter(target_file, result[0].keys(), delimiter="\t")
        dict_writer.writeheader()
        for value in result:
            dict_writer.writerow(value)
        target_file.write(f'Most popular hour(s) for the site: {popular_hour}')


print('\nTask 4. Site statistics data analysis')
src_file_path_ip = r'text4.txt'
trg_file_path_ip = r'text4-ip-analytics.txt'
print(f'\nCheck "{trg_file_path_ip}" to see output for source file "{src_file_path_ip}"')
get_info_by_ip(src_file_path_ip, trg_file_path_ip)
