import math
from tabulate import tabulate

def create_truth_table(function):
    """Создает таблицу истинности для одной функции."""
    table = []
    num_vars = int(math.log2(len(function)))
    headers = [chr(97 + i) for i in range(num_vars)] + ["f"]

    for i, value in enumerate(function):
        binary = format(i, f'0{num_vars}b')
        table.append(list(binary) + [value])

    return headers, table

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

def validate_function_input(input_str):
    if not all(c in '01' for c in input_str):
        return False, "Нужно вводить только 0 или 1."
    if not is_power_of_two(len(input_str)):
        return False, "Длина функции должна быть степенью двойки."
    return True, None

def check_constants(table):
    """Проверяет функцию на константность (T0, T1)."""
    first_value = table[0][-1]
    last_value = table[-1][-1]
    return ["+" if first_value == '0' else " ", "+" if last_value == '1' else " "]

def check_self_duality(function):
    """Проверяет функцию на самодвойственность."""
    n = len(function)
    for i in range(n // 2):
        if function[i] == function[-i - 1]:
            return " "
    return "+"

def check_monotonicity(table):
    """Проверяет функцию на монотонность."""
    num_vars = len(table[0]) - 1

    for i in range(len(table)):
        for j in range(len(table)):
            # Сравнение строк, чтобы убедиться, что одна меньше другой по переменным
            if all(table[i][k] <= table[j][k] for k in range(num_vars)):
                # Проверяем, что значение функции не убывает
                if table[i][-1] > table[j][-1]:
                    return " "
    return "+"


def check_linearity(tru_table):
    num_vars = len(tru_table[0]) - 1  # Количество переменных
    table = [[int(value) for value in row] for row in tru_table]

    # Преобразуем фу000нкцию в вектор значений
    func_values = [row[-1] for row in table]

    # Если все значения функции одинаковы, она линейная
    if all(value == func_values[0] for value in func_values):
        return "+"

    # Проверка линейности через декомпозицию по весовым коэффициентам
    n = len(func_values)
    walsh_transform = [0] * n

    # Вычисляем преобразование Уолша-Адамара
    for i in range(n):
        for j in range(n):
            xor_sum = bin(i & j).count('1') % 2
            walsh_transform[i] += (-1) ** xor_sum * func_values[j]

    # Линейность: если все значения преобразования Уолша делятся на 2, функция линейна
    for value in walsh_transform:
        if value % 2 != 0:
            return " "  # Функция нелинейная

    return "+"  # Функция линейная


def fully(analysis_results):
    """Определяет, является ли система полной."""
    transposed_results = list(zip(*analysis_results))
    # Пропускаем первый столбец с названиями функций
    for column in transposed_results[1:]:
        if all(value == "+" for value in column):
            return "-"
    return "+"

def main():
    while True:
        print("\nВведите функции для анализа (каждая строка — одна функция, пустая строка для завершения ввода):")
        user_inputs = []
        while True:
            input_str = input(f"f{len(user_inputs) + 1}: ").strip()
            if not input_str:
                break

            is_valid, error_message = validate_function_input(input_str)
            if not is_valid:
                print(f"Ошибка: {error_message}")
                continue

            user_inputs.append(input_str)

        if not user_inputs:
            print("Не было введено ни одной функции. Попробуйте снова.")
            continue

        analysis_results_all = []

        for func_index, input_str in enumerate(user_inputs):
            headers, table = create_truth_table(input_str)
            #print(f"\nТаблица истинности для функции f{func_index + 1}:")
            #print(tabulate(table, headers=headers, tablefmt="grid"))

            constants = check_constants(table)
            self_duality = check_self_duality(input_str)
            monotonicity = check_monotonicity(table)
            linearity = check_linearity(table)

            analysis_results = [f"f{func_index + 1}"] + constants + [self_duality, monotonicity, linearity]
            analysis_results_all.append(analysis_results)

        analysis_headers = ["Функция", "T0", "T1", "S", "M", "L"]
        print("\nОбщий анализ всех функций:")
        print(tabulate(analysis_results_all, headers=analysis_headers, tablefmt="grid"))

        full_system = fully(analysis_results_all)
        print("\nПолная система?")
        print("нет" if full_system == "-" else "да")

        repeat = input("\nХотите проанализировать другую систему функций? (да/нет): ").strip().lower()
        if repeat != "да":
            print("Работа программы завершена.")
            break

if __name__ == "__main__":
    main()
