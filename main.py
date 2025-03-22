from collections import deque
from icecream import ic
import time
import matplotlib.pyplot as plt

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
    n = list(range(nMin, nMax+1))

    openListBfs = []
    closedBfs = []
    timeBfs = []

    openListDfs = []
    closedDfs = []
    timeDfs = []

    for i in range(nMin, nMax+1):
        ic("iteracja:",i)
        startTime = time.time()
        sol, openList, closed = solve(i, 'bfs')
        showResult(sol)
        timeBfs.append(time.time() - startTime)
        ic("czas liczenia: ", timeBfs[-1])
        openListBfs.append(openList)
        closedBfs.append(closed)

        startTime = time.time()
        sol, openList, closed = solve(i, 'dfs')
        showResult(sol)
        timeDfs.append(time.time() - startTime)
        ic("czas liczenia: ", timeDfs[-1])
        openListDfs.append(openList)
        closedDfs.append(closed)

    ic(openListBfs, closedBfs, timeBfs)
    ic(openListDfs, closedDfs, timeDfs)

    # Wykres czasu wykonania
    plt.figure(figsize=(10, 5))
    plt.plot(n, timeBfs, marker='o', label="BFS", color='blue')
    plt.plot(n, timeDfs, marker='s', label="DFS", color='red')
    plt.xlabel("Rozmiar szachownicy (n)")
    plt.ylabel("Czas wykonania (s)")
    plt.title("Porównanie czasu wykonania BFS vs DFS")
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(n, openListBfs, marker='o', label="BFS", color='blue')
    plt.plot(n, openListDfs, marker='s', label="DFS", color='red')
    plt.xlabel("Rozmiar szachownicy (n)")
    plt.ylabel("Liczba openList")
    plt.title("OpenList BFS vs DFS")
    plt.legend()
    plt.grid()
    plt.show()

    # Wykres liczby odwiedzonych stanów
    plt.figure(figsize=(10, 5))
    plt.plot(n, closedBfs, marker='o', label="BFS", color='blue')
    plt.plot(n, closedDfs, marker='s', label="DFS", color='red')
    plt.xlabel("Rozmiar szachownicy (n)")
    plt.ylabel("Liczba closedList")
    plt.title("ClosedList BFS vs DFS")
    plt.legend()
    plt.grid()
    plt.show()

eksperyment(4, 7) # i=13 ~ 25s
# ic(solve(7, 'bfs'))