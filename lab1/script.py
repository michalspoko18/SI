from pyscript import document

def check_hetman(hetman, ustawienie):
    for pozycja in ustawienie:
        if hetman != pozycja:
            # Sprawdź czy hetmani są w tym samym wierszu
            if hetman[0] == pozycja[0]:
                return 1
            # Sprawdź czy hetmani są w tej samej kolumnie
            if hetman[1] == pozycja[1]:
                return 1
            # Sprawdź czy hetmani są na tej samej przekątnej
            if abs(hetman[0] - pozycja[0]) == abs(hetman[1] - pozycja[1]):
                return 1
    return 0

def draw_board(ustawienie, n):
    # Usuń poprzednią tabelę, jeśli istnieje
    table_container = document.querySelector("#table-container")
    table_container.innerHTML = ""

    # Tworzenie tabeli w HTML
    table_html = "<table>"
    
    for i in range(n):
        table_html += "<tr>"
        for j in range(n):
            
            if (i+j)%2==0:
                color = '#d3d3d3'
            else:
                color = 'white'

            if (j, i) in ustawienie:
                content = "&#9813;"
                if check_hetman((j, i), ustawienie)==1:
                    color = 'red'
            
            else: content = ''

            table_html += f"<td style='background-color: {color};'>{content}</td>"
        table_html += "</tr>"

    table_html += "</table>"

    return table_html


def set_value(event):
    err=0
    try:
        n = int(document.querySelector("#val").value)
        ustawienie = eval(document.querySelector("#val2").value)
    except:
        n = 4  # Domyślny rozmiar, jeśli nie podano poprawnej wartości
        ustawienie = [(2,0), (0,1), (3,2), (1,3)]
        err = 1
        info = f"<div class='msg-err'>Błędne dane w formularzu | Przykład n: 4, ustawinie: {ustawienie}</div>"

    table_container = document.querySelector("#table-container")
    table_container.innerHTML = ""

    table_html = draw_board(ustawienie, n)

    # Wyświetl informację o ustawieniu
    if err!=1:
        # Dodanie tabeli do kontenera
        table_container.innerHTML = table_html
        info = f"<div class='msg-scc'>Ustawienie hetmanów: {ustawienie}</div>"
        
    table_container.innerHTML += info

def show_result(event):
    table_container = document.querySelector("#table-container")
    
    try: 
        n = int(document.querySelector("#val").value)
    except:
        n = 4
    
    # Wybierz algorytm (można dodać przycisk wyboru w HTML)
    algorithm = "bfs"  # DFS jest zwykle szybszy dla tego problemu
    
    # Znajdź rozwiązanie
    solution = bfs_dfs(n, algorithm)
    
    if solution:
        table_html = draw_board(solution, n)
        info = f"<div class='msg-scc'>Rozwiązanie znalezione algorytmem {algorithm.upper()}: {solution}</div>"
        table_container.innerHTML = table_html + info
    else:
        table_container.innerHTML = "<div class='msg-err'>Nie znaleziono rozwiązania</div>"


def bfs_dfs(n, algorithm="bfs"):
    # Stan początkowy - pusta szachownica
    initial_state = []
    
    # Inicjalizacja kolejki/stosu Open
    open_list = [initial_state]
    
    # Zbiór stanów odwiedzonych
    visited = set()
    visited.add(str(initial_state))
    
    while open_list:
        # Pobierz stan z początku (BFS) lub końca (DFS) listy
        if algorithm.lower() == "bfs":
            current_state = open_list.pop(0)  # FIFO - kolejka
        else:
            current_state = open_list.pop()   # LIFO - stos
        
        # Sprawdź czy to stan końcowy (n hetmanów, które się nie atakują)
        if len(current_state) == n:
            # Sprawdź czy hetmani się nie atakują
            is_valid = True
            for i, pos1 in enumerate(current_state):
                for j, pos2 in enumerate(current_state):
                    if i != j and check_hetman(pos1, [pos2]) == 1:
                        is_valid = False
                        break
                if not is_valid:
                    break
            
            if is_valid:
                return current_state
        
        # Jeśli nie mamy jeszcze n hetmanów, generuj stany potomne
        if len(current_state) < n:
            # Generuj stany potomne - próbuj umieścić hetmana w każdym wierszu następnej kolumny
            col = len(current_state)
            for row in range(n):
                new_position = (col, row)
                
                # Sprawdź czy nowa pozycja nie koliduje z istniejącymi hetmanami
                if new_position not in current_state and check_hetman(new_position, current_state) == 0:
                    new_state = current_state.copy()
                    new_state.append(new_position)
                    
                    # Jeśli stan nie był jeszcze odwiedzony, dodaj go do listy Open
                    state_str = str(new_state)
                    if state_str not in visited:
                        open_list.append(new_state)
                        visited.add(state_str)
    
    # Jeśli nie znaleziono rozwiązania
    return None


def generate_children(state, n):
    """Generuje stany potomne umieszczając hetmana w następnej kolumnie."""
    children = []
    col = len(state)  # Kolumna, w której umieścimy następnego hetmana
    
    if col < n:
        for row in range(n):
            new_position = (col, row)
            # Sprawdź czy nowa pozycja nie koliduje z istniejącymi hetmanami
            if all(not is_attacking(new_position, (c, r)) for c, r in enumerate(state)):
                new_state = state.copy()
                new_state.append(row)
                children.append(new_state)
    
    return children

def is_attacking(pos1, pos2):
    """Sprawdza czy hetmani na pozycjach pos1 i pos2 się atakują."""
    col1, row1 = pos1
    col2, row2 = pos2
    
    # Ten sam wiersz
    if row1 == row2:
        return True
    # Ta sama kolumna
    if col1 == col2:
        return True
    # Ta sama przekątna
    if abs(col1 - col2) == abs(row1 - row2):
        return True
    
    return False
        
