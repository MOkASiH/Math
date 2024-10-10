import random
from Setting_the_set import input_count_sets, input_count_El
from Solving import Spliting
def input_formula():
    print("Введите формулу:")
    print("+ - объединение")
    print("# - пересечение")
    print("- - разность")
    print(": - симметрическая разность")
    print("~ - дополнение")
    print(
        "Название множеств вводится английскими заглавными буквами, между множеством и оператором должен быть отступ, (кроме дополнения)")
    print("Например: (A + C) : (B # ~C)")

    while (True):
        check_set = False
        check_name = False
        formula = input()
        for i in range(len(formula)):
            if ((formula[i] in wrong_name) or (formula[i] in wrong_name_smr) or (formula[i] in wrong_name_r)):
                check_name = True
            if(formula[i] in set_name):
                for j in range(len(set_name)):
                    if(formula[i] == set_name[j]):
                        if(j >= len(sets)):
                            check_set = True
        if(check_set == False):
            break
        else:
            print("Такого множества нет")
            continue
        if (check_name == False):
            break
        else:
            print("Введите названия множеств английскими заглавными буквами")

    result = Spliting(sets, formula, set_name)
    for i in range(len(set_name)):
        if (set_name[i] == result):
            if(sets[i] == None):
                input_formula()
            else:
                print("Ответ:")
                print(str(sets[i]).replace('[','{').replace(']','}'))



set_name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
wrong_name = "abcdefghijklmnopqrstuvwxyz"
wrong_name_r = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
wrong_name_smr = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

universe = [i-50 for i in range(101)]

print("Универсум от -50 до 50\n")

count_sets = input_count_sets()
print(count_sets)

sets = list(range(count_sets))

for i in range(count_sets):
    set_num = i
    input_count_El(set_name[i], set_num, sets)
for i in range(count_sets):
    print("Множество ", set_name[i], ": ", str(sets[i]).replace('[','{').replace(']','}'))

input_formula()



