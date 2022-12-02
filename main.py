"""
Лабораторная работа №3. Сборка рюкзака
Вариант 3: Рюкзак 2х4, Заражение. 10 очков
"""

# pylint: disable=invalid-name,redefined-outer-name
from functools import reduce

# Стартовые значения
START_POINTS = 10
# Размер рюкзака - 4x2 элемента = 8 слотов. Т.к. ограничение на
# расположение нет, рассмотрим как цепочку элементов
BACKPACK_SIZE = 8
# Необходимый предмет
REQUIRED_ITEM = 'д'

# Зададим словарь с очками выживания
STUFF_DICT = {
    'в': (3, 25), 'п': (2, 15), 'б': (2, 15), 'а': (2, 20),
    'и': (1, 5), 'н': (1, 15), 'т': (3, 20), 'о': (1, 25),
    'ф': (1, 15), 'д': (1, 10), 'к': (2, 20), 'р': (2, 20)
}


def get_variants(stuff: dict, weight: int) -> list:
    """
    Функция перебора элементов
    :param stuff:   Вещи
    :param weight:  Максимальный вес
    :return:        Список вещей, которые необходимо вять
    """

    items = list(stuff.items())
    # пустой массив, содержащий на каждой позиции пару из списка
    # предметов и количества очков для этого списка предметов
    variants = [[([], points) for _ in range(weight + 1)] for _ in range(len(items) + 1)]
    for i in range(1, len(items) + 1):
        for j in range(1, weight + 1):
            item = items[i - 1]
            n, w, v = item[0], item[1][0], item[1][1]
            if w > j:
                variants[i][j] = variants[i - 1][j]
            else:
                # Умножаем ценность на 2, потому что сначала ее вычли
                variants[i][j] = max(variants[i - 1][j],
                                     (variants[i - 1][j - w][0] + [n],
                                      variants[i - 1][j - w][1] + v * 2),
                                     key=lambda x: x[1])
    return variants


# Для начала рассчитаем количество стартовых очков
points = sum(v[1] for v in STUFF_DICT.values()) * -1 + START_POINTS

# заполняем таблицу для 8 ячеек рюкзака
variants = get_variants(STUFF_DICT, BACKPACK_SIZE)
# Выведем все возможные варианты
print('Возможные решения: ')
for variant in reduce(lambda past_, next_: past_ + next_, variants):
    if variant[1] > 0:
        print(f'Очки: {variant[1]}, набор {variant[0]}')

# оптимальное решение — последняя ячейка таблицы
optimal = list(variants[-1][-1])
# Проверка, что нужен определенный предмет
if REQUIRED_ITEM is not None:
    # Проверка на пристуствие нобходимого предмета в рюкзаке
    if REQUIRED_ITEM not in optimal[0]:
        # Если нет, ищем наименее ценный предмет
        item_to_replace = min(list(filter(lambda i: STUFF_DICT[i][0] == 1,
                                          optimal[0])),
                              key=lambda i: STUFF_DICT[i][1])
        # Заменим очки выживания в соответствии с найденным предметом
        optimal[1] = optimal[1] - STUFF_DICT[item_to_replace][1] * 2 + STUFF_DICT['д'][1] * 2
        # Заменим предмет
        optimal[0].remove(item_to_replace)
        optimal[0].append(REQUIRED_ITEM)

# сортируем предметы по весу, чтобы правильно собрать рюкзак
optimal[0].sort(key=lambda i: STUFF_DICT[i][0],
                reverse=True)

# собираем рюкзак
bag = []
for item in optimal[0]:
    # В соответствии со словарем данных ищем размер нашего предмета
    bag.extend([item] * STUFF_DICT[item][0])

print('Итоговый набор:')
print(''.join([f'[{bag[i]}],' if i % 4 != 3 else f'[{bag[i]}]\n' for i in range(len(bag))]))
print('Итоговые очки выживания:', optimal[1])

if optimal[1] > 0:
    print('Том выживет с таким набором предметов')
else:
    print('Зомби сожрут Тома заживо...')
