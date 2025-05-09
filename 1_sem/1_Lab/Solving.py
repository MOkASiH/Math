def parentheses(sets, formula, set_name):
    i = 0
    while("(" in formula):
        in_parentheses_tmp = ""
        new_form = ""
        if (formula[i] == "("):
            j = i + 1
            while (formula[j] != ")"):
                in_parentheses_tmp += formula[j]
                j += 1
            if (i != 0):
                for k in range(i):
                    new_form = new_form + formula[k]
                formula = new_form + Spliting(sets, in_parentheses_tmp, set_name)
                i = 0
            else:
                for k in range(j + 1, len(formula)):
                    new_form = new_form + formula[k]
                formula = Spliting(sets, in_parentheses_tmp, set_name) + new_form
                i = 0
        i += 1
    return formula

def Spliting(sets, formula, set_name):
    split = []
    if ("(" in formula):
        formula = parentheses(sets, formula, set_name)
    rev = len(formula) - 1
    while (rev >= 0):
        if(formula[rev] != " "):
            split.append(formula[rev])
        rev -= 1
    while(True):
        if(len(split) <= 1):
            break
        cnt = 0
        action = ""
        i = 0
        cnt_sets = 0
        while(cnt != 2 ):
            action = action + split.pop()
            if(action[i] == "~" and i == 0):
                cnt += 1
                cnt_sets = 1
            if(action[i] in set_name):
                cnt += 1
            i += 1
        if("~~" in action):
            action = action.replace('~~', '')
        if(len(action) == 1):
            return action
        sets.append(actions(sets, action, set_name, cnt_sets))
        split.append(set_name[len(sets)-1])
    return split.pop()

def actions(sets, formula, set_name, cnt_sets):
    need_sets = [0]*2
    k = 0
    for i in range (len(formula)):
        if (formula[i] in set_name):
            for j in range(len(set_name)):
                if(formula[i] == set_name[j]):
                    need_sets[k] = sets[j]
                    k += 1
                    break
    if("~" in formula):                                   
        if("~" == formula[0] or "~" == formula[1]):
            need_sets[0] = addition(need_sets[0])
        else:
            need_sets[1] = addition(need_sets[1])
        if (cnt_sets == 1):
            return need_sets[0]
    if("+" in formula):
        return union(need_sets)
    elif("#" in formula):
        return intersection(need_sets)
    elif("-" in formula):
        return difference(need_sets)
    elif(":" in formula):
        return symmetric_difference(need_sets)
    else:
        print("Неправильный ввод")
        return


def addition(set):
    result = list()
    for i in range(101):
        if((i - 50) in set ):
            continue
        result.append(i-50)
    return result

def union(need_sets):
    result = need_sets[0]
    for i in range(len(need_sets[1])):
        if (need_sets[1][i] in result):
            continue
        result.append(need_sets[1][i])
    return result
def intersection(need_sets):
    result = list()
    for i in range(len(need_sets[0])):
        if (need_sets[0][i] in need_sets[1]):
            result.append(need_sets[0][i])
    return result

def difference(need_sets):
    result = list()
    for i in range(len(need_sets[0])):
        if(need_sets[0][i] in need_sets[1]):
            continue
        result.append(need_sets[0][i])
    return result

def symmetric_difference(need_sets):
    result = list()
    for i in range(len(need_sets[0])):
        if(need_sets[0][i] in need_sets[1]):
            continue
        result.append(need_sets[0][i])
    for i in range(len(need_sets[1])):
        if(need_sets[1][i] in need_sets[0]):
            continue
        result.append(need_sets[1][i])
    return result
