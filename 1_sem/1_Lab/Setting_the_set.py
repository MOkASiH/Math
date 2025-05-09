import random

def hand(cnt, name, set_num, sets):
    tmp_ar = [0]*cnt

    for i in range(cnt):
        print("Введите ", i+1, " число множества ", name, ": ")

        while (True):
            try:
                tmp_ar[i] = int(input())
            except ValueError:
                print("Ошибка")
                continue
            if (-50 <= tmp_ar[i] <= 50):
                break
            else:
                print("Ведите число от -50 до 50")

    sets[set_num] = tmp_ar

def rand(cnt, name, set_num, sets):
    missing_seats = cnt
    multiplicity = 1
    custom_range = [-50, 50]
    tmp_ar = []

    while(True):
        print("\nУсловия задания множества ", name,": ")
        print("1. Все элементы меньше 0")
        print("2. Все элементы больше 0")
        print("3. Все элементы кратны определённому числу(меньше 10)")
        print("4. Все элементы лежат в определённом диапозоне")
        print("5. Не буду")
        try:
            choise_condition = int(input("\nВыберите условие: "))
        except ValueError:
            print("Ошибка, нужно ввести число")
            continue
        if(choise_condition == 1):
            while(missing_seats > 0):
                tmp = random.randint(-50, 0)
                if tmp not in tmp_ar:
                    tmp_ar.append(tmp)
                    missing_seats -= 1
            break
        elif(choise_condition == 2):
            while(missing_seats > 0):
                tmp = random.randint(0, 50)
                if (tmp not in tmp_ar):
                    tmp_ar.append(tmp)
                    missing_seats -= 1
            break
        elif(choise_condition == 3):
            while(True):
                try:
                    multiplicity = int(input("Введите число которому будет кратны элементы множества (меньше 10): "))
                except ValueError:
                    print("Ошибка, нужно ввести число")
                if(multiplicity >= 10):
                    continue
                else:
                    while (missing_seats > 0):
                        tmp = random.randint(-50, 50)
                        if (tmp not in tmp_ar and tmp % multiplicity == 0):
                            tmp_ar.append(tmp)
                            missing_seats -= 1
                    break
            break
        elif(choise_condition == 4):
            while (True):
                try:
                    custom_range[0] = int(input("Элементы лежат в диапозоне от: "))
                    custom_range[1] = int(input("до: "))
                except ValueError:
                    print("Ошибка, нужно ввести число")
                if (custom_range[0] < -50 or custom_range[1] > 50):
                    print("Диапозон должен входить в универсум (универсум от -50 до 50)")
                elif(custom_range[1]-custom_range[0] < cnt):
                    print("Диапозон меньше, чем количество элементов во множестве")
                else:
                    while (missing_seats > 0):
                        tmp = random.randint(custom_range[0], custom_range[1])
                        if (tmp not in tmp_ar):
                            tmp_ar.append(tmp)
                            missing_seats -= 1
                    break
            break
        elif(choise_condition == 5):
            while (missing_seats > 0):
                tmp = random.randint(-50, 50)
                if (tmp not in tmp_ar):
                    tmp_ar.append(tmp)
                    missing_seats -= 1
            break
        else:
            print("Ошибка выберите число от 1 до 5")
            continue

    sets[set_num] = tmp_ar

def input_count_sets():
    while(True):
        try:
            cnt = int(input("Введите количество множеств: "))
        except ValueError:
            print("Ошибка, нужно ввести число")
            continue
        break
    return(cnt)

def input_count_El(name,  set_num, sets):
    print("\nВведите количество элементов во множестве ", name, ": ")

    while(True):
        try:
            count_el = int(input())
        except ValueError:
            print("Ошибка, нужно ввести число")
            continue
        break

    print("\nВыберите, каким способом хотите заполнить множество")
    print ("1. Заполнить вручную")
    print("2. Заполнить псевдослучайными числами")
    while(True):
        try:
            choise = int(input())
        except ValueError:
            print("Ошибка")
            continue
        if (choise == 1):
            hand(count_el, name, set_num, sets)
            break
        elif(choise == 2):
            rand(count_el, name, set_num, sets)
            break
        else:
            print("Ошибка")