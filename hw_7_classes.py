import json
import pprint
import os
import pathlib
import fnmatch


# Задача-1
# У вас есть список(list) IP адресов. Вам необходимо создать
# класс который будет иметь методы:
# 1) Получить список IP адресов
# 2) Получить список IP адресов в развернутом виде
# (10.11.12.13 -> 13.12.11.10)
# 3) Получить список IP адресов без первых октетов
# (10.11.12.13 -> 11.12.13)
# 4) Получить список последних октетов IP адресов
# (10.11.12.13 -> 13)


class IpAddress:

    ip_list = ['10.11.12.13', '192.168.12.1', '147.22.243.33']

    def __init__(self):
        self._list = IpAddress.ip_list
        self._reversed_addr = []
        self._last_3_ocktets = []
        self._last_ocktets = []

    def get_ip_list(self):
        return f"IP addresses: {self._list}"

    def get_reversed_ip_addresses(self):
        for address in self._list:
            self._reversed_addr.append('.'.join(address.split('.')[::-1]))
        return f"Reversed addresses list: {self._reversed_addr}"

    def get_last_3_ocktets_list(self):
        for address in self._list:
            self._last_3_ocktets.append('.'.join(address.split('.')[1:]))
        return f"Last 3 ocktets: {self._last_3_ocktets}"

    def get_last_ocktets_list(self):
        for address in self._list:
            self._last_ocktets.append(address.split('.')[-1])
        return f"Last ocktets: {self._last_ocktets}"


print('\nTask 1. IP addresses class\n')
a = IpAddress()
print(a.get_ip_list())
print(a.get_reversed_ip_addresses())
print(a.get_last_3_ocktets_list())
print(a.get_last_ocktets_list())


# Задача-2
# У вас несколько JSON файлов. В каждом из этих файлов есть
# произвольная структура данных. Вам необходимо написать
# класс который будет описывать работу с этими файлами, а
# именно:
# 1) Запись в файл
# 2) Чтение из файла
# 3) Объединение данных из файлов в новый файл
# 4) Получить путь относительный путь к файлу
# 5) Получить абсолютный путь к файлу

class JsonHandler:

    default_file = 'example_json_1.json'

    def __init__(self, file):
        if file:
            self._file = file
        else:
            self._file = JsonHandler.default_file

    @staticmethod
    def find_path_to_file(file_name, fpath=os.getcwd()):
        """Function accepts file name and path to start search from with default value set to current directory.
        Examples: 'D:' , 'D:\folder'
        Returns absolute path to file or raises FileNotFoundError
        """
        print(f'\nSearching: {file_name}...')
        fpath.replace('\\', '\\\\')
        glob_path = pathlib.Path(fpath)
        file_path = None
        for path in sorted(glob_path.rglob('*.json')):
            if str(file_name) in str(path):
                # print(f'Requested file is located at: {str(path)}\n')
                file_path = str(path)
        if not file_path:
            print(f'File {file_name} was not found in {fpath}')
            raise FileNotFoundError
        return file_path

    def read_json(self, file):
        my_printer = pprint.PrettyPrinter(width=90, sort_dicts=False)
        try:
            with open(self.find_path_to_file(file)) as f:
                data = json.load(f)
                my_printer.pprint(data)
        except IOError:
            print(f'File {file} not found')

    def write_json(self, fdata, trg):
        if os.path.isfile(trg):
            print('\nFile exists. Overwriting...')
        else:
            print("File doesn't exist. Creating a new file")
        with open(trg, 'w') as output_file:
            json.dump(fdata, output_file)

    def merge_json_files(self, f1, f2, trg='merged_json.json'):
        try:
            with open(self.find_path_to_file(f1)) as file1:
                data1 = json.load(file1)
                print(data1)
            with open(self.find_path_to_file(f2)) as file2:
                data2 = json.load(file2)
                print(data2)
            if not os.path.isfile(trg):
                new_line = ''
            else:
                new_line = '\n'

            with open(trg, "a") as target_file:
                target_file.write(new_line)
                json.dump(data1, target_file, indent=4)
                target_file.write('\n')
                json.dump(data2, target_file, indent=4)
            print(f'Data was merged successfully. Please, check {trg}')
        except IOError:
            print(f'File {f1} or {f2} not found')

    @property
    def json_relative_path(self):
        return os.path.relpath(self.find_path_to_file(self._file))

    @property
    def json_absolute_path(self):
        return os.path.abspath(self.find_path_to_file(self._file))


print('\nTask 2. Working with json files')
json_file_1 = 'example_json_1.json'
json_file_2 = 'example_json_2.json'
handler1 = JsonHandler(json_file_1)
print('Absolute path: ', handler1.json_absolute_path)
print('Relative path: ', handler1.json_relative_path)
print('-'*30)

handler2 = JsonHandler(json_file_2)
print('Absolute path: ', handler2.json_absolute_path)
print('Relative path: ', handler2.json_relative_path)
handler2.read_json(json_file_2)

json3 = 'new_file.json'
data = {'a': 1, 'b': 2224}
handler1.write_json(data, json3)
print('-'*20)
handler1.merge_json_files(json_file_1, json3, 'merged_json2.json')


# Задача-3
#
# Создайте класс который будет хранить параметры для
# подключения к физическому юниту(например switch). В своем
# списке атрибутов он должен иметь минимальный набор
# (unit_name, mac_address, ip_address, login, password).
# Вы должны описать каждый из этих атрибутов в виде гетеров и
# сеттеров(@property). У вас должна быть возможность
# получения и назначения этих атрибутов в классе.


class Connector:

    def __init__(self, name='switch1', mac_addr='00:26:57:00:1f:02', ip_addr='192.168.14.33', login='test', passw=''):
        self._unit_name = name
        self._mac_address = mac_addr
        self._ip_address = ip_addr
        self._login = login
        self._password = passw

    @property
    def unit_name(self):
        return f"unit name {self._unit_name}"

    @unit_name.setter
    def set_unit_name(self, name):
        self._unit_name = name

    @property
    def mac_address(self):
        return f"Mac address: {self._mac_address}"

    @mac_address.setter
    def set_mac_address(self, m_addr):
        self._mac_address = m_addr

    @property
    def ip_address(self):
        return f"IP address: {self._ip_address}"

    @ip_address.setter
    def set_ip_address(self, ip):
        self._ip_address = ip

    @property
    def login(self):
        return f"Login: {self._login}"

    @login.setter
    def set_login(self, login):
        self._login = login

    @property
    def password(self):
        return f"Password: {self._password}"

    @password.setter
    def set_password(self, passwd):
        self._password = passwd


print('\nTask 3. Connector class')
unit1 = Connector()
print(f'\n{unit1.unit_name}\n{unit1.mac_address}\n{unit1.ip_address}\n{unit1.login}\n{unit1.password}')
unit1.set_unit_name = 'New unit name'
print(unit1.unit_name)

unit2 = Connector('switch2', '00:33:77:00:1f:06', '192.168.14.34', 'test2', '1234')
print(f'\n{unit2.unit_name}\n{unit2.mac_address}\n{unit2.ip_address}\n{unit2.login}\n{unit2.password}')
