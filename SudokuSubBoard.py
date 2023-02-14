
#!/usr/bin/env python3

# Terminal minesweeper
# 
# John Diaz january 2023
# TO DO list:
# generar subBoards hasta que no se repitan numeros en las filas y columnas....
#


import random
import numpy as np
import math



def ValidSubBoard(subBoard):
    # List the numbers inside the subBoard
    subBnums = np.unique(subBoard)
    subBnums = np.delete(subBnums, np.where(subBnums == -1))
    Num = np.linspace(1,9,9,dtype = int)
    # Find the valid numbers to put into the subBoard
    ValidNums = np.setdiff1d(Num,subBnums)
    ValidIndex = np.argwhere(subBoard == -1)
    #ValidNums = list(np.setdiff1d(Num,subBnums))
    #ValidIndex = list(np.argwhere(subBoard == -1))

    return ValidNums, ValidIndex
    
def setSubBoard(subBoard,ValidNums,ValidIndex):
    # Suffle ValidNums to set subBoard
    np.random.shuffle(ValidNums)
    for jn in range(len(ValidNums)):
        row =  ValidIndex[jn,0]
        col =  ValidIndex[jn,1]
        subBoard[row,col] = ValidNums[jn]
    
    return subBoard

def ValidBoard(Board,irow,icol):
    Aux = np.zeros([9,9])

    # Check if first row has repeated elements
    arr = Board[irow]
    arr = np.delete(arr, np.where(arr == -1))
    safe = True
    jrow = 0
    # Check rows    
    while safe and jrow < 3:
        arr = Board[irow+jrow]
        Aux[irow+jrow] = arr 
        arr = np.delete(arr, np.where(arr == -1))
        safe = (len(arr) == len(np.unique(arr)) )
        jrow += 1

    jcol = 0
    while safe and jcol < 3:
        arr = Board[:,icol+jcol]
        Aux[:,icol+jcol] = arr 
        arr = np.delete(arr, np.where(arr == -1))
        safe = (len(arr) == len(np.unique(arr)) )
        jcol += 1
   
    return safe

def SolveBoard(Board):
    # Create the 9 3x3 subBoards
    # print()
    for irow in range(3):
        # print()
        inirow = irow*3
        for icol in range(3):
            # print()
            # print(f" {irow} {icol}")
            inicol = icol*3
            subBoard = Board[inirow:inirow+3,inicol:inicol+3]
            # Separate 9x9 Board into 9 3x3 boards
            #print()
            #print(subBoard)
            #print()
            # Get the valid subBoard index and the valid numbers to put into.
            ValidNums, ValidIndex = ValidSubBoard(subBoard)
            # Calculate the maximum tries to suffle a subBoard of 3x3
            nmax = math.factorial(len(ValidNums))
            # print(ValidNums)
            unsafe = True
            # Counter for the number of times shuffle subBoard
            ntries = 0
 
            while unsafe and ntries < nmax:
                subBoard = setSubBoard(subBoard,ValidNums,ValidIndex)
                Board[inirow:inirow+3,inicol:inicol+3] = subBoard
                ntries += 1
                if ValidBoard(Board,inirow,inicol):
                    unsafe = False    

            #print()
            #print(Board) 
            
            if ntries == nmax: break
            

    print(Board)
    return unsafe
             


if __name__ == '__main__':
   
    example_board = np.array([
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ])
   
    unsafe = SolveBoard(example_board)
    
    
    
    
    
    
