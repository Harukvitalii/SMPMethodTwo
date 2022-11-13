import numpy as np
from pprint import pp
import copy


MATRIX = [
    [2,1,-2,18], 
    [1,2,4,22], 
    [-1,1,-2,-10]]

Func = [2,-3,-6,1,0,0,0]

# MATRIX = [
#     [-1.5,-3,1,-1,-18], 
#     [-3  ,-2,0, 1,-24],
#     # [-1,1,-2,-10]
# ]

# Func = [5,6,1,1,0,0,0]

print(len(MATRIX[0]))
print(MATRIX[0])
# Func = [0,	0,	-4,	-4,	0,	0,	0]



class MT: 
    def __init__(self, matrix, func): 
        self.func_x = 0
        for i in func: 
            if i != 0:  self.func_x += 1
        self.func_x = list(range(self.func_x))
        self.shape = (len(matrix),len(matrix[0])-1)
        basis = self.add_basis(matrix)
        self.matrix = basis + [func]
        
    
    
    def add_basis(self,initmass):
        result = []
        add_m = np.eye(self.shape[0], self.shape[0])
        
        for i, mass in enumerate(initmass): 
            last, y = mass[-1], mass[:-1]
            y = y + list(add_m[i]) + [last]
            result.append(y)
        return result 
    
    
    def make_full_table(self, table): 
        #scrape all elements -1 of table and find minimum
        basis = [i[-1] for  i in table]
        basis[-1] = 0
        minelem_index, minelem = basis.index(min(basis)), min(basis)
        #check element >- 0
        if minelem >= 0: return table,(None,None), 'end'  
        
        serline_mass = table[minelem_index]
        # print('serednja linia' , serline_mass)
        delta  = table[-1]
        
        #find -delta/serline_massija
        delta_mass = []
        for i in range(len(serline_mass)-1):
            if serline_mass[i] == 0: 
                elem = 0
            else: 
                elem = -delta[i]/serline_mass[i]
            delta_mass.append(elem)
        delta_mass.append(0)
        
        # find stovbetzch
        mas = []
        print('check mass', serline_mass)
        for i in range(len(serline_mass)-1): 
            t = True if serline_mass[i] < 0 else False   
            check = [abs(delta[i]), i]
        
            if t: mas.append(check) #and delta[i] != 0
        print('mass check ', mas)
        if not mas: return 0,0,'end_error_no_minus_elements_in_stovbetsh'
        
        if len(mas) == 1: 
            index = mas[0][1]
        elif len(mas) > 1:
            for i in range(len(mas)-1): 
                if mas[i][0] <= mas[i+1][0]: 
                    index = mas[i][1]
                else:
                    index = mas[i+1][1]
            
        else: index = None

                
        # chenge main radok 
        # print('dfdfd', table[minelem_index][index])

        
        return table + [delta_mass], (minelem_index, index),'continue'
        
        
        
    def create_table_gaucce(self, table, inds): 
        SR_ELEM = table[inds[0]][inds[1]]
        
        #обнулимо
        if table[inds[0]][inds[1]] != 1:
            table[inds[0]] = [-i for i in table[inds[0]]]
            for i, nb in enumerate(table[inds[0]]): 
                # print(nb)
                if nb == -0.0 or nb == - 0: table[inds[0]][i] = 0
            
            snak_main_radok = True 
        else: snak_main_radok = False
        
        
        # pp(table)
        table_new = copy.deepcopy(table)
        for i,tb in enumerate(table): 
            if i == inds[0]: continue   
            for j, _ in enumerate(tb): 
                # print(i,j)
                main_rad_znak = -table[inds[0]][j] if snak_main_radok else table[inds[0]][j]
                
                table_new[i][j] = round(table[i][j] - (main_rad_znak * table[i][inds[1]])/SR_ELEM, 3)
                if table_new[i][j] == -0.0: table_new[i][j] = 0
                # print(table[i][inds[1]])
                # print(f"{table_new[i][j]} = {znach} - {main_rad_znak} * {table[i][inds[1]]} / {SR_ELEM}")

        if table[inds[0]][inds[1]] != 1: 
            temp = [ round(i/table[inds[0]][inds[1]],3) for i in table[inds[0]]]
            table_new[inds[0]] = temp
        
                
        return table_new
        
    
    def main(self): 
        end = 'continue'
        find_table = self.matrix   
        xes = []
        pp(find_table)
        iterat = 0
        while True: 

            table, inds, end  = self.make_full_table(find_table)
            xes.append(inds[0]) 
            print('iter: ', iterat+1)
            pp(table)
            pp('-'*100)

            if 'end' in end: 
                print(end)
                xes.pop(-1)
                # print('inds', xes, self.func_x)
                for i in self.func_x: 
                    for j in xes: 
                        if i == j:
                            print(f'x{i+1} = {table[i][-1]}')
                            self.func_x.remove(i)
                for i in self.func_x: 
                   print(f'x{i+1} = 0')
                print(f'F(X) = {table[-1][-1]}')
                    


                exit()
            table.pop(-1)
            pp(inds)
            table_new = self.create_table_gaucce(table,inds)
            iterat +=1
            # pp(table_new)
            find_table = table_new
            # print(find_table)
            # exit()
        
        
        
        
    
    
    
        
        
        
if __name__ == "__main__":
    mt = MT(MATRIX, Func)
    mt.main()
    





