from pyscript import document

def check_hetman(hetman, ustawienie):
    for pozycja in ustawienie:
        print(pozycja)
        if hetman != pozycja: 
            if hetman[0] == pozycja[0]: 
                # print(hetman, pozycja)
                return 1
            if hetman[1] == pozycja[1]: 
                # print(hetman, pozycja)
                return 1
            if (hetman[1]-hetman[0]) == (pozycja[1]-pozycja[0]): return 1
            if (hetman[1]+hetman[0]) == (pozycja[1]+pozycja[0]): return 1

def set_value(event):
    err=0
    try:
        n = int(document.querySelector("#val").value)
        ustawienie = eval(document.querySelector("#val2").value)
    except:
        n = 4  # Domyślny rozmiar, jeśli nie podano poprawnej wartości
        ustawienie = [(2,0), (0,1), (3,2), (1,3), (4,4)]
        err = 1
        info = "<div class='msg-err'>Błędne dane w formularzu | n: int, ustawinie: [(1,1), (0,0), (2,2)]</div>"

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

    # Wyświetl informację o ustawieniu
    if err!=1:
        # Dodanie tabeli do kontenera
        table_container.innerHTML = table_html
        info = f"<div class='msg-scc'>Ustawienie hetmanów: {ustawienie}</div>"
        
    table_container.innerHTML += info

def show_result(event):
    table_container = document.querySelector("#table-container")

    table_container.innerHTML = "<div class='msg-err'>Funkcja nieaktywna</div>"

