import tkinter as tk
import math

def f(x):
    """
    Функция для интегрирования.
    """
    return math.tan(x)

def method_rectangles(start, finish, function, num, number):
    """
    Вычисляет приближённое значение определённого интеграла методом прямоугольников (левым или правым).

    start — начало интервала интегрирования  
    finish — конец интервала интегрирования  
    function — функция, которую интегрируем  
    num — количество прямоугольников  
    number — тип метода (0 — левых, 1 — правых прямоугольников)  
    """
    s = 0
    h = (finish - start) / num

    if number == 0:  # метод левых прямоугольников
        x = start
        for i in range(num):
            s += function(x) * h
            x += h
    elif number == 1:  # метод правых прямоугольников
        x = start + h
        for i in range(num):
            s += function(x) * h
            x += h
    return s

def method_trapezoid(start, finish, function, num):
    """
    Вычисляет приближённое значение определённого интеграла методом трапеций.

    start — начало интервала  
    finish — конец интервала  
    function — функция, которую интегрируем  
    num — количество трапеций  
    """
    h = (finish - start) / num
    s = (function(start) + function(finish)) / 2
    for i in range(1, num):
        s += function(start + i * h)
    return s * h

def draw_met_rect(function, start, finish, num, scale, center_x, center_y, number, fill='red'):
    """
    Рисует прямоугольники метода.

    function — функция, которую интегрируем  
    start — начало интервала  
    finish — конец интервала  
    num — количество прямоугольников  
    scale — масштаб  
    center_x — центр по оси x  
    center_y — центр по оси y  
    number — тип метода (0 — левых, 1 — правых прямоугольников)  
    fill — цвет обводки  
    """
    h = (finish - start) / num
    for i in range(num):
        if number == 0:
            x = start + i * h
            y = function(x)
        elif number == 1:
            x = start + (i + 1) * h
            y = function(x)
        else:
            continue  # не рисуем, если метод не прямоугольников

        x0_screen = center_x + (start + i * h) * scale
        x1_screen = center_x + (start + (i + 1) * h) * scale
        y_screen = center_y - y * scale

        canv.create_rectangle(x0_screen, center_y, x1_screen, y_screen, outline=fill)

def draw_met_trapezoid(function, start, finish, num, scale, center_x, center_y, fill='red'):
    """
    Рисует трапеции метода трапеций.

    function — функция, которую интегрируем  
    start — начало интервала  
    finish — конец интервала  
    num — количество трапеций  
    scale — масштаб  
    center_x — центр по оси x  
    center_y — центр по оси y  
    fill — цвет линий  
    """
    h = (finish - start) / num
    for i in range(num):
        x0 = start + i * h
        x1 = x0 + h
        y0 = function(x0)
        y1 = function(x1)

        x0_screen = center_x + x0 * scale
        x1_screen = center_x + x1 * scale
        y0_screen = center_y - y0 * scale
        y1_screen = center_y - y1 * scale

        canv.create_polygon(x0_screen, center_y, x0_screen, y0_screen,
                            x1_screen, y1_screen, x1_screen, center_y,
                            outline=fill, fill='', smooth=False)

def draw_func(func, a, b, scale, center_x, center_y, fill='blue', width=2):
    """
    Рисует график функции на Canvas.

    func — функция для отрисовки  
    a — начало отрезка  
    b — конец отрезка  
    scale — масштаб  
    center_x — центр по оси x  
    center_y — центр по оси y  
    fill — цвет линии  
    width — толщина линии  
    """
    h = 0.01
    x = a
    while x < b:
        try:
            x0_screen = center_x + x * scale
            y0_screen = center_y - func(x) * scale
            x1_screen = center_x + (x + h) * scale
            y1_screen = center_y - func(x + h) * scale
            canv.create_line(x0_screen, y0_screen, x1_screen, y1_screen, fill=fill, width=width)
        except:
            pass
        x += h

def create_axes(center_x, center_y, scale):
    """
    Рисует оси координат на Canvas.

    center_x — центр по оси x  
    center_y — центр по оси y  
    scale — масштаб  
    """
    canv.create_line(0, center_y, 1000, center_y, arrow=tk.LAST)  # ось X
    canv.create_line(center_x, 0, center_x, 800, arrow=tk.FIRST)  # ось Y

    for i in range(-10, 11):
        x = center_x + i * scale
        canv.create_line(x, center_y-5, x, center_y+5)
        canv.create_text(x, center_y+15, text=str(i))
    for i in range(-10, 11):
        y = center_y - i * scale
        canv.create_line(center_x-5, y, center_x+5, y)
        canv.create_text(center_x+15, y, text=str(i))

def redraw():
    """
    Перерисовывает координаты, график функции и выбранный метод.
    """
    canv.delete("all")
    create_axes(center_x, center_y, scale)
    draw_func(f, -7, 7, scale, center_x, center_y)
    if current_method == 0 or current_method == 1:
        draw_met_rect(f, a, b, n, scale, center_x, center_y, current_method)
        result = method_rectangles(a, b, f, n, current_method)
    elif current_method == 2:
        draw_met_trapezoid(f, a, b, n, scale, center_x, center_y)
        result = method_trapezoid(a, b, f, n)
    result_label.config(text=f"Приближённое значение интеграла: {result:.5f}")

def run_method(number):
    """
    Запускает расчёт и отрисовку выбранного метода.

    number — тип метода (0 — левые, 1 — правые прямоугольники, 2 — трапеции)  
    """
    global current_method
    current_method = number
    redraw()

def on_scale_change(value):
    """
    Обновляет масштаб и перерисовывает график при изменении значения ползунка.
    """
    global scale
    scale = float(value)
    redraw()

# Параметры интегрирования
a = 0
b = 1
n = 10
scale = 200
center_x = 500
center_y = 400
current_method = 0

# Окно
mainm = tk.Tk()
mainm.title('Метод прямоугольников и трапеций')
mainm.geometry('1000x900')
mainm.resizable(False, False)

# Canvas
canv = tk.Canvas(mainm, width=1000, height=800, bg='white')
canv.pack()

# Панель кнопок
button_frame = tk.Frame(mainm)
button_frame.pack()

tk.Button(button_frame, text="Метод левых прямоугольников", command=lambda: run_method(0)).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Метод правых прямоугольников", command=lambda: run_method(1)).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Метод трапеций", command=lambda: run_method(2)).pack(side=tk.LEFT, padx=10)

# Ползунок масштаба
scale_slider = tk.Scale(mainm, from_=50, to=400, orient=tk.HORIZONTAL, label="Масштаб (пикселей на единицу)",
                        command=on_scale_change)
scale_slider.set(scale)
scale_slider.pack(pady=10)

# Метка результата
result_label = tk.Label(mainm, text="Приближённое значение интеграла:", font=('Arial', 14))
result_label.pack(pady=10)

# Первая отрисовка
redraw()

# Запуск
mainm.mainloop()
