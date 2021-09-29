import argparse
import os
import tempfile
import json
from filelock import FileLock

# настройки:
# имя файла хранилища
filename = 'storage.data'
# пустое значение по-умолчанию
empty_result = None


# чтение хранилища в память
def load_storage(path):
    result = {}
    if os.path.isfile(path):
        with open(path, 'r') as file:
            result = json.load(file)
    return result


# сохранение хранилища
def save_storage(obj, path):
    # примитивная блокировка, не лишённая минусов, но это вообще никак не оговаривалось в задании
    # поэтому пусть кладёт рядышком .lock, который можно удалить руками в случае падения скрипта
    with FileLock('.lock'):
        try:
            with open(path, 'w') as file:
                json.dump(obj, file)
        # тут можно бы отдельно обрабатывать проблемы с правами доступа и прочее, но это не оговорено в задании
        except Exception as e:
            print('Panic! There is a Big error!')
            raise e


# возвращает значения ключа
def value_get(dict_obj, key):
    # ключ есть - выводим, нет - выводим пустое значение по-умолчанию
    return dict_obj[key] if key in dict_obj else [str(empty_result)]


# добавляем значения по ключу
def value_add(dict_obj, key, val):
    # здесь можно бы обработать случай, когда значение ключа не было передано
    # и присваивать пустое по-умолчанию (empty_result), но такое поведение не оговорено в постановке задачи
    if key not in dict_obj:
        dict_obj[key] = list(val)
    else:
        dict_obj[key].extend(val)
    return


# создаём парсер аргументов и подготавливаем его
def prepare_parser():
    result = argparse.ArgumentParser(description='Key-Value storage')
    result.add_argument('--key', nargs='?', required=True, help='Key to assign passed or show stored values')
    # задаем такой формат, чтобы можно было передать в одном параметре сразу несколько значений (опционально)
    # формат параметра тогда будет --val [value1 [value2 ...]]
    result.add_argument('--val', nargs='*', help='Values to store. If param is not passed, prints stored values')
    return result


if __name__ == '__main__':
    # создадим парсер и распарсим аргументы
    parser = prepare_parser()
    args = parser.parse_args()
    # определяем положение файла
    storage_path = os.path.join(tempfile.gettempdir(), filename)
    # читаем хранилище
    storage = load_storage(storage_path)
    # если новое значение не задано, то выводим то, что найдём
    if args.val is None:
        stored = value_get(storage, args.key)
        print(str.join(', ', stored))
    else:
        value_add(storage, args.key, args.val)
        # сохраняем хранилище
        save_storage(storage, storage_path)