import os
from contextlib import contextmanager
from contextlib import suppress
from time import time
from contextlib import ContextDecorator
from functools import wraps

existing_folder = 'test1'
non_existing_folder = 'test2'
cur_dir = os.getcwd()

# Задача-1
# Создать объект менеджера контекста который будет переходить в папку которую он принимает на вход.
# Так же ваш объект должен принимать исключение которое он будет подавлять
# Если флаг об исключении отсутствует, исключение должно быть поднято.


class ContextFolderNavigator:
    """Custom context manager for opening specified folder.
    exc_sup parameter:
    Passed values(e.g., FileNotFoundError) will mean that such exception will be suppressed if  folder doesn't exist.
    None value is used as default. In this case FileNotFoundError is not suppressed"""
    def __init__(self, folder, *exc_sup):
        self._folder = folder
        self._exc = exc_sup

    def __enter__(self):
        print('Current folder is ', os.getcwd())
        try:
            os.chdir(self._folder)
        except self._exc:
            print(f'{self._exc} handled successfully')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Now you're in {os.getcwd()}\n")


print('\nTask 1. Changing folder with using context manager\n')
with ContextFolderNavigator(existing_folder):
    print(f'Running for existing folder')

os.chdir(cur_dir) # need to navigate back to original folder to explicitly observe behavior
with ContextFolderNavigator(non_existing_folder, FileNotFoundError):
    print(f'Running for non-existing folder')


# Задача -2
# Описать задачу выше но уже с использованием @contextmanager

class Navigator:
    def __init__(self, folder, *exc_sup):
        self._folder = folder
        self._exc = exc_sup

    @contextmanager
    def change_folder(self, f=None):
        print(f'Folder before change: {os.getcwd()}')
        if f is not None:
            self._folder = f
        with suppress(self._exc):
            if self._exc:
                print(f'{self._exc} suppressed')
            os.chdir(self._folder)
        print(f'Current folder:{os.getcwd()}\n')


print('\nTask 2. Changing folder with @contextmanager. Solution 1\n')
os.chdir(cur_dir)
folder_1 = Navigator(existing_folder)
folder_1.change_folder()

os.chdir(cur_dir)
Navigator(existing_folder, FileNotFoundError).change_folder(non_existing_folder)


# *********************************


@contextmanager
def change_dir(folder, *exc_sup):
    print(f'Current folder before:{os.getcwd()}')
    try:
        os.chdir(folder)
    except exc_sup:
        print(f'{exc_sup} handled successfully')
    yield
    print(f'Current folder after:{os.getcwd()}\n')


print('\nTask 2. Changing folder with @contextmanager. Solution 2\n')
os.chdir(cur_dir)
with change_dir(existing_folder, FileNotFoundError):
    print('Changing folder')

os.chdir(cur_dir)
with change_dir(non_existing_folder, FileNotFoundError):
    print('Changing folder')


# Задача -3
# Создать менеджер контекста который будет подсчитывать время выполнения вашей функции

class ContextTimer(ContextDecorator):
    def __init__(self):
        self._start_time = None
        self._exec_time = None

    def __enter__(self):
        self._start_time = time()
        print('Execution started')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exec_time = time() - self._start_time
        print(f"Function took {self._exec_time} seconds to execute")


@ContextTimer()
def test_sleep_func(sec):
    print('sleeeeeeep')
    import time
    time.sleep(sec)


print('\nTask 3. Context manager. Counting function execution time. Solution 1. Inheritance from ContextDecorator \n')
test_sleep_func(1)

# ************************************************


class ContDecorator(object):
    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner


class ContextTimer(ContDecorator):
    def __init__(self):
        self._start_time = None
        self._exec_time = None

    def __enter__(self):
        self._start_time = time()
        print('Execution started')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exec_time = time() - self._start_time
        print(f"Function took {self._exec_time} seconds to execute")


@ContextTimer()
def test_sleep_func(sec):
    print('sleep a bit')
    import time
    time.sleep(sec)


print('\nTask 3. Context manager. Counting function execution time. Solution 2. Custom decorator \n')


test_sleep_func(2)


@ContextTimer()
def read_file(fname):
    print(f'Reading file {fname}')
    with open(fname) as f:
        f.read()


print('\nUsing the same to see time execution for reading this file')
file = 'insurance.csv'
read_file(file)
