from collections import deque
from icecream import ic
import time

def checkHetman(s, newCol):
    newRow = len(s)
    
    for row, col in enumerate(s):
        # Sprawdzenie kolumny
        if col == newCol:
            return False
        
        # Sprawdzenie wiersza
        if row == newRow:
            return False
        
        # Sprawdzenie przekątnych
        if abs(row - newRow) == abs(col - newCol):
            return False
    
    return True

def validCheckHetman(s, n):
    if len(s) == n:
        for i in range(n):
            for j in range(i+1, n):
                if s[i][0] == s[j][0] or s[i][1] == s[j][1] or abs(s[i][0] - s[j][0]) == abs(s[i][1] - s[j][1]):
                    return False
        return True
    
def showResult(s):
    # Pokazuje pierwsze rozwiazanie 
    if s:
        result = s[0]
        format = []

        for pos, val in enumerate(result):
            format.append((pos, val))

        # print(f"Pierwsze rozwiązanie: {format}")
        return format
    else:
        print("Brak rozwiązania")

def generateChildren(s, n):
    # Generuje stan o 1 więcej 
    children = []
    row = len(s)

    if row>=n:
        return children
    
    for col in range(n):
        t = s + [(row,col)]
        children.append(t)

    return children 

def solve(n, metod='bfs'):
    openList = deque() if metod == "bfs" else []  # BFS -> FIFO deque, DFS -> LIFO stack\
    closedList = set()
    sol = []

    openList.append([])

    while openList:
        s = openList.popleft() if metod == 'bfs' else openList.pop()

        if validCheckHetman(s, n):
            # return s # Jedno rozwiazanie
            sol.append(s) # Zbiera wszystkie rozwiazania 
            continue

        closedList.add(tuple(s))

        for children in generateChildren(s, n):
            if tuple(children) not in closedList:
                openList.append(children)

    return sol, len(sol), len(closedList)

def dfs(n):
    ic('not exist yet')
    pass    

def bfs(n):
    openList = deque([()])  # Lista openList
    closed = set()       # Lista closed
    sol = [] # Rozwiazania

    while openList:
        s = openList.popleft() # Stan s
        closed.add(s)  # Dodajemy stan do listy closed
        
        row = len(s)
        # ic(row)
        if row == n:
            # return [s] # Jedno rozwiazanie
            sol.append(s) # Zbiera wszystkie rozwiazania  
            continue
            
        for col in range(n):
            if checkHetman(s, col):
                t = s + (col,) # Zbior stanow potomnych
                if t not in closed: 
                    openList.append(t)

    ic(sol, len(sol), len(closed))
    return sol, len(sol), len(closed)

    # print(len(openList))
    # ic(openList)
    # print(len(closed))
    # ic(closed)

def eksperyment(nMin=4, nMax=12):
    openListEksBfs = []
    closedEksBfs = []
    timeEksBfs = []

    openListEksDfs = []
    closedEksDfs = []
    timeEksDfs = []

    for i in range(nMin, nMax+1):
        ic("iteracja:",i)
        startTime = time.time()
        sol, openList, closed = solve(i, 'bfs')
        showResult(sol)
        timeEksBfs.append(time.time() - startTime)
        ic("czas liczenia: ", timeEksBfs[i-4])
        openListEksBfs.append(openList)
        closedEksBfs.append(closed)

        startTime = time.time()
        sol, openList, closed = solve(i, 'dfs')
        showResult(sol)
        timeEksDfs.append(time.time() - startTime)
        ic("czas liczenia: ", timeEksDfs[i-4])
        openListEksDfs.append(openList)
        closedEksDfs.append(closed)

    ic(openListEksBfs, closedEksBfs, timeEksBfs)
    ic(openListEksDfs, closedEksDfs, timeEksDfs)


# eksperyment(8, 8) # i=13 ~ 25s
ic(solve(9, 'bfs'))