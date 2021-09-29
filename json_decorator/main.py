import json


def to_json(function_to_decorate):
    # Внутри себя декоратор определяет функцию-"обертку". Она будет обернута вокруг декорируемой,
    # получая возможность исполнять произвольный код до и после нее.
    # обёртка для вызываемых функций
    def to_json_wrapper(*args, **kwargs):
        # результат вызова оригинальной функции
        original_result = function_to_decorate(*args, **kwargs)
        return json.dumps(original_result)
    # декоратор возвращает обёртку
    return to_json_wrapper


@to_json
def get_data():
    return {
        'data': 42
    }


@to_json
def get_complex_data():
    result = {
        'list': [1, 2, 3, 4],
        'number': 42.,
        'str': 'this is a string',
    }
    return result


@to_json
def get_sum_of_two(first, second):
    result = {
        'first': first,
        'second': second,
        'answer': first + second
    }
    return result


@to_json
def get_sum_of_all(*args):
    result = {
        'input': args,
        'answer': sum(args)
    }
    return result


if __name__ == '__main__':
    print(get_data())
    print(get_complex_data())
    print(get_sum_of_two(11, 31))
    print(get_sum_of_all(1, 2, 3, 4))
