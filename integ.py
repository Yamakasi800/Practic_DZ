import tkinter as tk
import math

def f(x):
    """
    Функция для интегрирования.
    Здесь по умолчанию используется tan(x).
    """
    return math.tan(x)

def method_rectangles(start, finish, function, num, number):
    """
    Вычисляет приближённое значение определённого интеграла
    методом левых или правых прямоугольников.

    start — начало интервала интегрирования,
    finish — конец интервала,
    function — функция для интегрирования,
    num — количество прямоугольников,
    number — тип метода (0 — левых, 1 — правых прямоугольников).
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

def draw_met_rect(function, start, finish, num, scale, center_x, center_y, number, fill='darkorange'):
    """
    Рисует прямоугольники выбранного метода на Canvas.

    function — функция для интегрирования,
    start, finish — границы интервала интегрирования,
    num — количество прямоугольников,
    scale — масштаб,
    center_x, center_y — координаты центра,
    number — тип метода (0 — левых, 1 — правых прямоугольников),
    fill — цвет прямоугольников.
    """
    h = (finish - start) / num
    for i in range(num):
        if number == 0:
            x = start + i * h
            y = function(x)
        elif number == 1:
            x = start + (i + 1) * h
            y = function(x)

        x0_screen = center_x + (start + i * h) * scale
        x1_screen = center_x + (start + (i + 1) * h) * scale
        y_screen = center_y - y * scale

        canv.create_rectangle(x0_screen, center_y, x1_screen, y_screen, outline=fill)

def draw_func(func, a, b, scale, center_x, center_y, fill='mediumblue', width=2):
    """
    Рисует график функции на Canvas.

    func — функция для построения графика,
    a, b — начало и конец интервала,
    scale — масштаб,
    center_x, center_y — координаты центра,
    fill — цвет линии,
    width — толщина линии графика.
    """
    h = 0.01
    x = a
    while x < b:
        x0_screen = center_x + x * scale
        y0_screen = center_y - func(x) * scale
        x1_screen = center_x + (x + h) * scale
        y1_screen = center_y - func(x + h) * scale
        canv.create_line(x0_screen, y0_screen, x1_screen, y1_screen, fill=fill, width=width)
        x += h

def create_axes(center_x, center_y, scale):
    """
    Рисует систему координат.

    center_x, center_y — координаты центра осей,
    scale — масштаб делений.
    """
    canv.create_line(0, center_y, 1000, center_y, arrow=tk.LAST)  # ось X
    canv.create_line(center_x, 0, center_x, 800, arrow=tk.FIRST)  # ось Y

    # Деления и подписи
    for i in range(-10, 11):
        x = center_x + i * scale
        canv.create_line(x, center_y-5, x, center_y+5)
        canv.create_text(x, center_y+15, text=str(i))
    for i in range(-10, 11):
        y = center_y - i * scale
        canv.create_line(center_x-5, y, center_x+5, y)
        canv.create_text(center_x+15, y, text=str(i))

def run_method(number):
    """
    Очищает экран, рисует оси, функцию и прямоугольники выбранного метода.

    number — тип метода (0 — левых, 1 — правых прямоугольников).
    """
    canv.delete("all")
    create_axes(center_x, center_y, scale)
    draw_func(f, -7, 7, scale, center_x, center_y)
    draw_met_rect(f, a, b, n, scale, center_x, center_y, number)
    result = method_rectangles(a, b, f, n, number)
    result_label.config(text=f"Приближённое значение интеграла: {result:.5f}")

# Параметры интегрирования
a = 0
b = 1
n = 10
scale = 150
center_x = 500
center_y = 400

mainm = tk.Tk()
mainm.title('Метод прямоугольников')
mainm.geometry('1000x900')
mainm.configure(bg = "gray")
mainm.resizable(False, False)

canv = tk.Canvas(mainm, width=1000, height=800, bg='gainsboro')
canv.pack()

# Панель с кнопками
button_frame = tk.Frame(mainm)
button_frame.pack()

# Кнопки выбора метода
tk.Button(button_frame, text="Метод левых прямоугольников", command=lambda: run_method(0)).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Метод правых прямоугольников", command=lambda: run_method(1)).pack(side=tk.LEFT, padx=10)

# для вывода результата
result_label = tk.Label(mainm, text="Приближённое значение интеграла:", font=('Arial', 14))
result_label.pack(pady=10)

# Первоначальная отрисовка координат и графика функции
create_axes(center_x, center_y, scale)
draw_func(f, -7, 7, scale, center_x, center_y)

mainm.mainloop()
