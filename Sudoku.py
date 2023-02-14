
#!/usr/bin/env python3

# Terminal minesweeper
# 
# John Diaz january 2023
# TO DO list:
# generar subBoards hasta que no se repitan numeros en las filas y columnas....
#


import numpy as np
from itertools import permutations

def CountValidLines(TestBoard):
    nvalid = 0
    # Check if rows has repeated elements if not is valid
    for irow in range(9):
        arr = TestBoard[irow]
        if (len(arr) == len(np.unique(arr)) ):
            nvalid += 1

    # Check if columns has repeated elements if not is valid
    for icol in range(9):
        arr = TestBoard[irow]
        if (len(arr) == len(np.unique(arr)) ):
            nvalid += 1

    return nvalid    


def ValidBoard(AuxBoard,irow,icol):

    # Check if first row has repeated elements
    arr = AuxBoard[irow]
    arr = np.delete(arr, np.where(arr ==0))
    safe = True
    jrow = 0
    # Check rows    
    while safe and jrow < 3:
        arr = AuxBoard[irow+jrow]
        arr = np.delete(arr, np.where(arr == 0) )
        safe = (len(arr) == len(np.unique(arr)) )
        jrow += 1

    jcol = 0
    while safe and jcol < 3:
        arr = AuxBoard[:,icol+jcol]
        arr = np.delete(arr, np.where(arr == 0) )
        safe = (len(arr) == len(np.unique(arr)) )
        jcol += 1

    return safe

def FilterPerms(iniBoard,subBoard,inirow,inicol,Perms,ValidIndex):
    # Check if the permutation is valid using the initial board, if not, is remove.
    #print(len(Perms))
    EmptyBoard = np.zeros([9,9])

    ip = 0
    while ip < len(Perms):
        ValidNums = Perms[ip]
        subBoard = setSubBoard(subBoard,ValidNums,ValidIndex)  
        EmptyBoard[inirow:inirow+3,inicol:inicol+3] = subBoard
        if ValidBoard(iniBoard+EmptyBoard,inirow,inicol) == False:
            Perms.remove(ValidNums)

        ip += 1

    return Perms

def ValidSubBoard(subBoard):
    # List the numbers inside the subBoard
    subBnums = np.unique(subBoard)
    subBnums = np.delete(subBnums, np.where(subBnums == 0))
    Num = np.linspace(1,9,9,dtype = int)
    # Find the valid numbers to put into the subBoard
    ValidNums = np.setdiff1d(Num,subBnums)
    ValidIndex = np.argwhere(subBoard == 0)

    return ValidNums, ValidIndex

def setSubBoard(subBoard,ValidNums,ValidIndex):
    for jn in range(len(ValidNums)):
        row =  ValidIndex[jn,0]
        col =  ValidIndex[jn,1]
        subBoard[row,col] = ValidNums[jn]

    return subBoard

def SolveBoard(iniBoard):
    # Create a copy of initial array
    AuxBoard = np.copy(iniBoard)
    # Set iniBoard immutable
    iniBoard.setflags(write=False)
    # Create a dictionary to save Board data
    #print(iniBoard) 
    Board = {}
    isubB = 0
    emptys = np.zeros(9)
    for irow in range(3):
        inirow = irow*3
        for icol in range(3):
            inicol   = icol*3
            subBoard = 'subBoard'+str(isubB)    
            Nums     = 'Nums'+str(isubB)    
            Index    = 'Index'+str(isubB)
            Perm     = 'Perm'+str(isubB)   
            iniRow   = 'inirow'+str(isubB)   
            iniCol   = 'inicol'+str(isubB)   
            # Separate 9x9 Board into 9 3x3 boards
            Board[iniRow] = inirow
            Board[iniCol] = inicol
            Board[subBoard] = AuxBoard[inirow:inirow+3,inicol:inicol+3]
            # Get the valid subBoard index and the valid numbers to put into.
            Board[Nums], Board[Index] = ValidSubBoard(Board[subBoard])
            # Generate all possible permutations of ValidNums
            TempPerm = list(permutations(Board[Nums]))
            Board[Perm] = FilterPerms(iniBoard,Board[subBoard],inirow,inicol,TempPerm,Board[Index])
            isubB += 1


    #print(iniBoard)
    ntest = 99999999
    # Save the number of valid lines (rows and columns) per test
    ValidLines = np.zeros(ntest,dtype=int)
    # set maximum nuber of valid lines
    maxlines = 0
    for itest in range(ntest):
    # Create a copy of initial array
        TestBoard = np.copy(iniBoard)
        for isubB in range (9):
            subBoard = 'subBoard'+str(isubB)    
            Index    = 'Index'+str(isubB)
            Perm     = 'Perm'+str(isubB)   
            iniRow   = 'inirow'+str(isubB)   
            iniCol   = 'inicol'+str(isubB)   
            inirow   = Board[iniRow] 
            inicol   = Board[iniCol]
            Perms    = Board[Perm]
            subBoard = Board[subBoard]
            Index    = Board[Index]
            iperm    = np.random.randint(len(Perms))
            # print(f" subBoard: {isubB} ")
            # print(len(Perms))
            # print(np.random.randint(len(Perms)))
            ValidNums = Perms[iperm]
            subBoard = setSubBoard(subBoard,ValidNums,Index)  
            # print(subBoard) 
            TestBoard[inirow:inirow+3,inicol:inicol+3] = subBoard
 
        # Count the number of valid lines
        ValidLines[itest] = CountValidLines(TestBoard)
        if (itest%1000 == 0):  
            print(f" test: {itest} maxlines: {maxlines} ")
        if ValidLines[itest] > maxlines:
            print(f" test: {itest} has {ValidLines[itest]} valid lines ")
            print(f" a new best TestBoard: ")
            print(TestBoard)
            maxlines = ValidLines[itest]

if __name__ == '__main__':
   
    example_board = np.array([
        [ 3, 9, 0,   0, 5, 0,   0, 0, 0],
        [ 0, 0, 0,   2, 0, 0,   0, 0, 5],
        [ 0, 0, 0,   7, 1, 9,   0, 8, 0],

        [0, 5, 0,   0, 6, 8,   0, 0, 0],
        [2, 0, 6,   0, 0, 3,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 4],

        [5, 0, 0,   0, 0, 0,   0, 0, 0],
        [6, 7, 0,   1, 0, 5,   0, 4, 0],
        [1, 0, 9,   0, 0, 0,   2, 0, 0]
    ])
   
    SolveBoard(example_board)
    
    
    
    
    
    
