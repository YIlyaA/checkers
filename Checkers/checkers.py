import numpy as np
import matplotlib.pyplot as plt
import math

# В массиве массивов боард нужно вести вычисления от (y, x) = (строка, колонна)
# Создаем доску, -1 справа и снизу нужно для того, чтобы не было ошибки выхода за поле (с помощью -1 как бы увеличили поле)
board = [
    [0, 2, 0, 2, 0, 2, 0, 2, -1],
    [2, 0, 2, 0, 2, 0, 2, 0, -1],
    [0, 2, 0, 2, 0, 2, 0, 2, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, -1],
    [1, 0, 1, 0, 1, 0, 1, 0, -1],
    [0, 1, 0, 1, 0, 1, 0, 1, -1],
    [1, 0, 1, 0, 1, 0, 1, 0, -1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1]
]
# Создание изображения и фигур
fig, ax = plt.subplots()

rectangles = []        # этот массив нам нужен длля хранения всег черных клеток
circles = []           # для хранения черных и белых кругов
circles_w = []         # для хранения белых кругов
circles_b = []         # для хранения черных кругов
circle_chosen = []     # для хранения круга на который нажали
current_player = 1     # переменнаая текущего игрока (1 - белые, 2 - черные)

# Создаем черные и белые квадраты - поле 
for i in range(8):
    for j in range(8):
        if (i+j)%2 == 0:
            ax.add_patch(plt.Rectangle((i,j), 1, 1, color='#95A5A6')) # выводим на  экран белые квадраты
        else:
            r = plt.Rectangle((i,j), 1, 1, color='#4169E1')  #4169E1
            ax.add_patch(r)                                          # выводим на экран                              
            rectangles.append(r)                                     # Записали в массив черный квадарт 

# Расставляем шашки
for i in range(8):
    for j in range(8): 
        if board[j][i] == 1:
            c = plt.Circle((i+.5, j+.5), 0.4, color='white') 
            ax.add_patch(c)
            circles.append(c)                          # записываем в общий массив белую шашку
            circles_w.append(c)                        # чисто белые в массив
        elif board[j][i] == 2:
            c2 = plt.Circle((i+.5, j+.5), 0.4, color='black') 
            ax.add_patch(c2)
            circles.append(c2)                         # в общий массив черную шашку
            circles_b.append(c2)                       # чисто черные в массив
                

# Функция, которая проверяет находится ли передоваемая ей точка в круге именно среди белых шашек
def check_circle_w(x, y):  
    point = (x, y)
    for circle in circles_w:
        if circle.center == point:
            return circle
        
# Функция, которая проверяет находится ли передоваемая ей точка в круге именно среди черных шашек
def check_circle_b(x, y):  
    point = (x, y)
    for circle in circles_b:
        if circle.center == point:
            return circle

# Функция, которая проверяет находится ли передоваемая ей точка в круге именно среди всех шашек
def check_circle(x, y):
    point = (x, y)
    for circle in circles:
        if circle.center == point:
            return circle

# Функция, которая возвращает квадрат на который было совершенно нажатие         
def check_rectangle(x, y):
    for rect in light_rect:
        xx = rect.get_x()
        yy = rect.get_y()
        if x == xx and y == yy:
            return rect        

# Функция, которая проверяет условие конца игры        
def game_over_check():
    count_w = 0
    count_b = 0
    for c in circles:
        x = int(c.center[0] - 0.5)
        y = int(c.center[1] - 0.5)
        if board[y][x] == 1:
            count_w += 1
        elif board[y][x] == 2:
            count_b += 1
            
    if count_w == 0 or count_b == 0:
        return False
    else:
        return True

# Функция, которая передвигает шашки    
def move_circle(circle, x_dest, y_dest):
    x_orig = int(circle.center[0] - 0.5)   # начальная координата круга
    y_orig = int(circle.center[1] - 0.5)
    if board[y_orig][x_orig] == 1:                                   # Белая шашка
        if abs(y_orig - y_dest) == 2 and abs(x_dest - x_orig) == 2:  # если перемещение круга равно 2 клеткам по х и у, то.. (находи координату круга, который будет сбит)
            if y_orig > y_dest:
                yy = y_orig - 1
            else:
                yy = y_dest - 1
            if x_orig > x_dest:
                xx = x_orig - 1
            else:
                xx = x_dest - 1
            if(check_circle(xx+.5, yy+.5)):   # проверям есть ли такой круг среди всех кругов
                cir = check_circle(xx+.5, yy+.5)   # передаем этот круг в переменную 
                if cir in circles:                 # Если он есть в массиве вссех кругов, то 
                    cir.remove()                   # Удаляем с экрана
                    circles.remove(cir)            # Удаляем из общего массива
                    circles_b.remove(cir)          # Удаляем из массива черных кргов
                board[yy][xx] = 0  # Удаляем круг который сбили - его координата была 2 - стала 0
        board[y_orig][x_orig] = 0  # Удаляем шашку с исходной позиции
        board[y_dest][x_dest] = 1  # Перемещаем шашку на новую позицию
    if board[y_orig][x_orig] == 2:  # Черная шашка (аналогично что и для белой)
        if abs(y_orig - y_dest) == 2 and abs(x_dest - x_orig) == 2:
            if y_orig > y_dest:
                yy = y_orig - 1
            else:
                yy = y_dest - 1
            if x_orig > x_dest:
                xx = x_orig - 1
            else:
                xx = x_dest - 1
            if(check_circle(xx+.5, yy+.5)):
                cir = check_circle(xx+.5, yy+.5)
                if cir in circles:
                    cir.remove()
                    circles.remove(cir)
                    circles_w.remove(cir)
                board[yy][xx] = 0
        board[y_orig][x_orig] = 0                            # Удаляем шашку с исходной позиции
        board[y_dest][x_dest] = 2                            # Перемещаем шашку на новую позицию
    circle.set_center((x_dest + 0.5, y_dest + 0.5))  # Обновляем координаты шашки на графике
    plt.draw()          # обновляем экран
    light_rect.clear()  # очищаем массив подсвечивающихся квадратов
    ####################################
    # for i in board:
    #     print(i)
    # print('--------------------------')
    ####################################
    for i in rectangles:           # расскрашиваем все квадраты в черный после подсветки
        i.set_color('#4169E1')
    
    ####################################
    # for j in circles:
    #     print(j)
    ####################################

    # Скрипт очередности 
    global current_player
    if current_player == 1:                           # Если белая шашка 
        if abs(x_dest - x_orig) == 2:                 # Если ход на 2 клетки, т е сбиваем какую то шашку  
            mov = get_possible_moves(x_dest, y_dest)  # Получаем возможный ход для шашки которой только что побили 
            if mov == []:                             # Если больше нельзя ходить этой шашкой, то переход к другому игроку
                current_player = 2  
            else:
                for el in mov:                        # ЕФсли есть куда ходить, с условие что этот в этот ход будет сбита шашка 
                    if abs(el[0] - x_dest) == 2:
                        current_player = 1            # Опять ход этой шашки 
                    else:
                        current_player = 2            # Если нельзя больше бить, то ход черных  
        else:
            current_player = 2
    else:                                             # Черная шашка (тоже самое, что и для белых) 
        if abs(x_dest - x_orig) == 2:
            mov = get_possible_moves(x_dest, y_dest)
            if mov == []:
                current_player = 1   
            else:
                for el in mov:
                    if abs(el[0] - x_dest) == 2:
                        current_player = 2
                    else:
                        current_player = 1
        else:
            current_player = 1

# Функция нажатия на шашку
def on_click(event):
    if game_over_check():      # Проверяем условие конца игры
        # global current_player
        xd, yd = event.xdata, event.ydata  # Получаем координаты точки, на которую было совершено нажатие
        try: 
            # Возможные ходы
            x = math.trunc(xd)  # отбрасывает дробную часть числа = вершина квадрата
            y = math.trunc(yd)  
            if 0 <= y < 8 and 0 <= x < 8 and board[y][x] != 0:
                    
                x_circ, y_circ = x + .5, y + .5          
                
                if current_player == 1:                        # Если игрок белый то ходим белыми 
                    if check_circle_w(x_circ, y_circ):
                        c = check_circle_w(x_circ, y_circ)
                        circle_chosen.clear()                  # Очищаем массив выбранных кругов
                        highlight(x, y)
                        circle_chosen.append(c)                # Добавляем выбранный круг
                else:                                          # Если игрок черный, то этот скрипт
                    if check_circle_b(x_circ, y_circ):
                        c = check_circle_b(x_circ, y_circ)
                        circle_chosen.clear()
                        highlight(x, y)
                        circle_chosen.append(c)      
        except TypeError:
            print('Not in the zone of board')
    else:    # Если конец игры то отключаем оси -> больше ходить нельзя
        plt.gca().set_axis_off()

# Функция нажатия на клетку куда хотим походить 
def click_step(event):
    if game_over_check():   # Условие конца игры
        xd, yd = event.xdata, event.ydata  # Получаем координаты точки, на которую было совершено нажатие
        # Возможные ходы
        x = math.trunc(xd)  # отбрасывает дробную часть числа = вершина квадрата
        y = math.trunc(yd)  
        c = circle_chosen[0]
        if c:
            if check_rectangle(x, y):    
                # Шашка уже выбрана, передвигаем ее на новое поле
                move_circle(c, x, y)
    else:
        plt.gca().set_axis_off()   # Если конец игры - отключаем оси  

# Функция подсветки
def highlight(x, y):
    for i in rectangles:
        i.set_color('#4169E1')  # Раскрашиваем в черный цвет все квадраты
    possible_moves = get_possible_moves(x, y)  # передает массив возможных ходов  
    if len(possible_moves) > 0:
        global light_rect
        light_rect = []          # Массив квадратов возможных ходов - желтого цвета
        for point in possible_moves:    # для каждой точки из возможных ходов
            for squar in rectangles:    # для каждого квадрата во всех квадратах 
                xx = squar.get_x()   #координаты вершины квадрата х
                yy = squar.get_y()   #координаты вершины квадрата у
                if point[0] == xx and point[1] == yy:   # если возможная вершина совпадает с координатой квадрата, то это возможный ход
                    squar.set_color('yellow')   # Подсветка возможных ходов 
                    light_rect.append(squar)    # добавляем в массив квадратов возможные ходы (передаем квадраты)
                elif x == xx and y == yy:
                    squar.set_color('yellow')   # Подсветка квадрата на который нажали 
        
        plt.draw()            # обновляем экран

# Функция поиска ходов для белых
def get_possible_moves(x, y):
    possible_moves = []

    # Определить текущие координаты шашки
    current_row, current_col = x, y
    
    status = True     # Статус была ли побита шашка (False), если просто ход, то (True)
    
    directions = []   # массив возможных ходов
    
    if board[current_col][current_row] == 2:  # Черная шашка
        
        if board[current_col+1][current_row-1] == 0:      # Если слева свободно 
            directions.append((-1, 1))                 
        if board[current_col+1][current_row-1] == 1:      
            if board[current_col+2][current_row-2] == 0:  # Если слева вверху шашка белая
                directions.append((-2, 2))
                status = False
        if board[current_col-1][current_row-1] == 1:      # Если слева внизу шашка белая
            if board[current_col-2][current_row-2] == 0:
                directions.append((-2, -2))
                status = False
        
        if board[current_col+1][current_row+1] == 0:       # Если справа свободно
            directions.append((1, 1))
        if board[current_col+1][current_row+1] == 1:       # Если справа вверху белая
            if board[current_col+2][current_row+2] == 0:
                directions.append((2, 2))
                status = False
        if board[current_col-1][current_row+1] == 1:        # Если справа внизу белая
            if board[current_col-2][current_row+2] == 0:
                directions.append((2, -2))
                status = False
            
    if board[current_col][current_row] == 1:   # Белая шашка   (аналогия черным)
        if board[current_col-1][current_row-1] == 0:
            directions.append((-1, -1))
        if board[current_col-1][current_row-1] == 2:
            if board[current_col-2][current_row-2] == 0:
                directions.append((-2, -2))
                status = False
        if board[current_col+1][current_row-1] == 2:
            if board[current_col+2][current_row-2] == 0:
                directions.append((-2, 2))
                status = False
                
        if board[current_col-1][current_row+1] == 0:
            directions.append((1, -1))
        if board[current_col-1][current_row+1] == 2:
            if board[current_col-2][current_row+2] == 0:
                directions.append((2, -2))
                status = False
        if board[current_col+1][current_row+1] == 2:
            if board[current_col+2][current_row+2] == 0:
                directions.append((2, 2))
                status = False
    
    # Если был ход на 2 клетки, то удаляем из возможных ходов простые ходы на 1 клетку 
    if status == False:
        if (1, -1) in directions:
            directions.remove((1, -1))
        if (-1, -1) in directions:
            directions.remove((-1, -1))
        if (1, 1) in directions:
            directions.remove((1, 1))
        if (-1, 1) in directions:
            directions.remove((-1, 1))
        
    if len(directions) > 0: 
        for direction in directions:
            row_step, col_step = direction
            new_row = current_row + row_step
            new_col = current_col + col_step

            # Проверить, если новые координаты в пределах доски
            if new_row >= 0 and new_row <= 8 and new_col >= 0 and new_col <= 8:
                # Добавить новую позицию в список возможных ходов
                possible_moves.append((new_row, new_col))

    return possible_moves

# Настраиваем оси
ax.set_xlim(0, 8)
ax.set_ylim(8, 0)
ax.set_aspect('equal')

# Устанавливаем буквенные обозначения на оси X
ax.set_xticks(np.arange(0.5, 8.5, step=1))
ax.set_xticklabels(['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A'])

# Устанавливаем числовые обозначения на оси Y
ax.set_yticks(np.arange(0.5, 8.5, step=1))
ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '7', '8'])

# draw_circles()

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('button_press_event', click_step)

# if len(circles) != 0:
plt.show()