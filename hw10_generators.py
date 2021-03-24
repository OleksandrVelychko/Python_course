import time


# Задача-1
# У вас есть файл из нескольких строк. Нужно создать генератор который будет построчно выводить строки из вашего файла.
# При вызове итерировании по генератору необходимо проверять строки на уникальность.
# Если строка уникальна, тогда ее выводим на экран, если нет - скипаем

def get_unique_lines(file):
    unique_lines = []
    for line in open(file):
        line = line.strip()
        if line not in unique_lines:
            yield line
            unique_lines.append(line)


print(f'Unique lines are:\n{list(get_unique_lines("text_10.txt"))}')


# Задача-2 (оригинальный вариант и его делать не обязательно):
# представим есть файл с логами, его нужно бессконечно контролировать
# на предмет возникнования заданных сигнатур.
#
# Необходимо реализовать пайплайн из корутин, который подключается к существующему файлу
# по принципу команды tail, переключается в самый конец файла и с этого момента начинает следить
# за его наполнением, и в случае возникнования запиcей, сигнатуры которых мы отслеживаем -
# печатать результат
#
# Архитектура пайплайна

#                    --------
#                   /- grep -\
# dispenser(file) <- - grep - -> pprint
#                   \- grep -/
#                    --------

# Структура пайплайна:
# ```

def coroutine(func):
    """decorator for coroutines to avoid using next for new yields"""
    def wrap(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)  # next(gen) will also work instead of gen.send(None)
        return gen
    return wrap


@coroutine
def grep(*args):
    pattern, target = args
    while True:
        line = yield
        if pattern in line:
            target.send(line)


@coroutine
def printer():
    while True:
        line = yield
        print(line)


@coroutine
def dispenser(*args):
    while True:
        item = yield
        for target in list(*args):
            target.send(item)


def follow(file, disp):
    while True:
        line = file.readline().rstrip()
        if not line:
            continue
        disp.send(line)


# ```
#
# Каждый grep следит за определенной сигнатурой
#
# Как это будет работать:
#
# ```

print('\nTask 2. Asynchronous event handler')
with open('log.txt', 'r') as f_open:
    follow(f_open,
           # delegating events and tracking specified patterns
           dispenser([
               grep('python', printer()),
               grep('is', printer()),
               grep('great', printer())])
           )


# ```
# Как только в файл запишется что-то содержащее ('python', 'is', 'great') мы сможем это увидеть
#
# Итоговая реализация фактически будет асинхронным ивент хендлером, с отсутствием блокирующих операций.
#
# Если все плохо - план Б лекция Дэвида Бизли
# [warning] решение там тоже есть :)
# https://www.dabeaz.com/coroutines/Coroutines.pdf


# Задача-3 (упрощенный вариант делаете его если задача 2 показалась сложной)
# Вам нужно создать pipeline (конвеер, подобие pipeline в unix https://en.wikipedia.org/wiki/Pipeline_(Unix)).
#
# Схема пайплайна :
# source ---send()--->coroutine1------send()---->coroutine2----send()------>sink
#
# Все что вам нужно сделать это выводить сообщение о том что было получено на каждом шаге и обработку ошибки GeneratorExit.
#
# Например: Ваш source (это не корутина, не генератор и прочее, это просто функция ) в ней опеделите цикл из 10 элементов
# которые будут по цепочке отправлены в каждый из корутин и в каждом из корутив вызвано сообщение о полученном элементе.
# После вызова .close() вы должны в каждом из корутин вывести сообщение что работа завершена.
