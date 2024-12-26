import math
from tabulate import tabulate #для табличек


def create_true(input_str):
    num_vars = int(math.log2(len(input_str)))
    table = []
    headers = [chr(97 + i) for i in range(num_vars)] + ["f"]
    for i, value in enumerate(input_str):
        binary = format(i, f'0{num_vars}b')
        table.append(list(binary) + [value])
    return headers, table

def Degree_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


def check_input(input_str):
    if not all(c in '01' for c in input_str):
        return False, "Нужно вводить только 0 или 1"
    if not Degree_of_two(len(input_str)):
        return False, "Количество символов должно быть больше 1-го и кратно 4-ём"
    return True, None

def connect_terms(term1, term2):
    diff_count = 0
    combined = []
    for bit1, bit2 in zip(term1, term2):
        if bit1 != bit2:
            diff_count += 1
            combined.append('-')
        else:
            combined.append(bit1)
    return None if diff_count != 1 else ''.join(combined)

def create_sdnf(table):
    terms = []
    for row in table:
        if row[-1] == '1':
            terms.append(
                " * ".join(f"{chr(97 + i)}" if bit == '1' else f"~{chr(97 + i)}" for i, bit in enumerate(row[:-1]))
            )
    return " ∨ ".join(f"({term})" for term in terms)

def create_sknf(table):
    terms = []
    for row in table:
        if row[-1] == '0':
            terms.append(
                " ∨ ".join(f"{chr(97 + i)}" if bit == '0' else f"~{chr(97 + i)}" for i, bit in enumerate(row[:-1]))
            )
    return " * ".join(f"({term})" for term in terms)


def min_sdnf(terms):
    while True:
        new_terms = set()
        used = set()
        for i, term1 in enumerate(terms):
            for j, term2 in enumerate(terms):
                if i < j:
                    combined = connect_terms(term1, term2)
                    if combined:
                        new_terms.add(combined)
                        used.add(term1)
                        used.add(term2)
        terms = terms - used | new_terms
        if not new_terms:
            break
    return terms

def create_implicant_matrix(terms, minterms):
    print("Импликантная матрица:")
    matrix = []
    for term in terms:
        row = []
        for minterm in minterms:
            match = True
            for bit_term, bit_minterm in zip(term, minterm):
                if bit_term != '-' and bit_term != bit_minterm:
                    match = False
                    break
            row.append('+' if match else '')
        matrix.append(row)
    return matrix

def terms_to_squeeze(terms):
    expressions = []
    for term in terms:
        expr = " * ".join(
            f"{chr(97 + i)}" if bit == '1' else f"~{chr(97 + i)}" for i, bit in enumerate(term) if bit != '-'
        )
        expressions.append(f"({expr})" if expr else "")
    return " ∨ ".join(expressions)


def terms_to_squeeze_list(terms):
    expressions = []
    for term in terms:
        expr = " * ".join(
            f"{chr(97 + i)}" if bit == '1' else f"~{chr(97 + i)}" for i, bit in enumerate(term) if bit != '-'
        )
        expressions.append(expr)
    return expressions

def find_essential_implicants(matrix, terms):
    essential = set()
    covered = set()
    for col in range(len(matrix[0])):
        rows_with_one = [row for row in range(len(matrix)) if matrix[row][col] == '+']
        if len(rows_with_one) == 1:
            essential.add(rows_with_one[0])
            covered.add(col)
    return essential, covered


def find_min_and_red_forms(matrix, terms):
    covered_minterms = set()
    minimal_forms = []
    for term_index, row in enumerate(matrix):
        if '+' in row:
            if all(col_index in covered_minterms or cell == '' for col_index, cell in enumerate(row)):
                continue
            minimal_forms.append(terms[term_index])
            covered_minterms.update(col_index for col_index, cell in enumerate(row) if cell == '+')
    redundant_forms = set(terms) - set(minimal_forms)
    return minimal_forms, list(redundant_forms)


def main():
    while(True):
        input_str = input("Введите вектор длиной до 16 символов из '0' и '1': ")
        is_valid, error_message = check_input(input_str)

        if not is_valid:
            print(f"Error: {error_message}")
            continue
        break

    headers, table = create_true(input_str)
    print(tabulate(table, headers=headers, tablefmt="grid"))

    sdnf = create_sdnf(table)
    print(f"СДНФ: {sdnf}")

    sknf = create_sknf(table)
    print(f"СКНФ: {sknf}")

    minterms = [format(i, f'0{len(table[0]) - 1}b') for i, row in enumerate(table) if row[-1] == '1']
    minimized_terms = list(min_sdnf(set(minterms)))
    minimized_list = terms_to_squeeze_list(minimized_terms)
    print("Минимальные импликанты:")
    for term in minimized_list:
        print(f"- {term}")

    matrix = create_implicant_matrix(minimized_terms, minterms)
    term_labels = [
        "".join(f"{chr(97 + i)}" if bit == '1' else f"~{chr(97 + i)}" for i, bit in enumerate(term) if bit != '-') for
        term in minimized_terms]
    minterm_labels = ["".join(f"{chr(97 + i)}" if bit == '1' else f"~{chr(97 + i)}" for i, bit in enumerate(minterm))
                      for minterm in minterms]
    print(tabulate(matrix, headers=minterm_labels, showindex=term_labels, tablefmt="grid"))

    minimal_forms, redundant_forms = find_min_and_red_forms(matrix, minimized_terms)

    minimal_dnf = terms_to_squeeze(minimal_forms)
    redundant_dnf = terms_to_squeeze(redundant_forms)

    print(f"Минимальная форма: {minimal_dnf}")
    print(f"Тупиковая форма: {redundant_dnf}")


main()
