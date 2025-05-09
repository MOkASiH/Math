def anal_all(matrix):
    reflex(matrix)
    
def reflex(matrix):
    flag_ref = True
    flag_antiref = True
    for i in range(len(matrix)):
        if (matrix[i][i] == 0 and (flag_ref == True)):
            flag_ref = False
        if(matrix[i][i] == 1 and (flag_antiref == True)):
            flag_antiref = False      
    if(flag_ref == True):
        print("Матрица рефлексивна")
    elif(flag_antiref == True):
        print("Матрица антирефлексивна")
        
        
#def antireflex():
    
#def symmetric():
    
#def antisymmetric():
    
#def asymmetric():
    
#def transitive():
    
#def full():