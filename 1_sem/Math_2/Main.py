from Analysis import anal_all

file = open('C:/Users/MOkAS/Desktop/Math_2/outside.txt', 'r')
matrix  = list()
for line in file:
    tmp = list()
    for i in line:
        if(i != " " and i != "\n"):
            tmp.append(int(i))
    matrix.append(tmp)
file.close()


anal_all(matrix)