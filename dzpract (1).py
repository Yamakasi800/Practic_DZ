import tkinter as tk
import math

def create_canvas(window, width=800, height=600, bg_color='white'):
    """
    Создает холст для рисования.
    
    window: Главное окно Tkinter.
    width: Ширина холста (по умолчанию 800).
    height: Высота холста (по умолчанию 600).
    bg_color: Цвет фона холста (по умолчанию белый).
    return: Объект Canvas.
    """
    canvas = tk.Canvas(window, width=width, height=height, bg=bg_color)
    canvas.pack()  
    return canvas  

def draw_axes(canvas, origin_x, origin_y, length=500, step=50, color='black'):
    """
    Рисует оси координат с отметками.
    
    canvas: Объект холста Tkinter.
    origin_x: Координата центра по оси X.
    origin_y: Координата центра по оси Y.
    length: Длина осей (по умолчанию 500).
    step: Расстояние между отметками (по умолчанию 50).
    color: Цвет осей (по умолчанию черный).
    """
    width = int(canvas['width'])  # Получаем ширину холста
    height = int(canvas['height'])  # Получаем высоту холста
    
    # Рисуем ось X
    canvas.create_line(0, origin_y, width, origin_y, arrow=tk.LAST, fill=color)
    for x in range(origin_x % step, width, step):  # Отметки на оси X
        canvas.create_line(x, origin_y - 5, x, origin_y + 5, fill=color)
        canvas.create_text(x, origin_y + 15, text=str((x - origin_x) // step), fill=color)
    
    # Рисуем ось Y
    canvas.create_line(origin_x, 0, origin_x, height, arrow=tk.FIRST, fill=color)
    for y in range(origin_y % step, height, step):  # Отметки на оси Y
        canvas.create_line(origin_x - 5, y, origin_x + 5, y, fill=color)
        canvas.create_text(origin_x - 15, y, text=str(-(y - origin_y) // step), fill=color)

def plot_function(canvas, func, x_range, origin_x, origin_y, step=50, color='blue'):
    """
    Рисует график функции на холсте.
    
    canvas: Объект холста Tkinter.
    func: Функция, которую нужно нарисовать.
    x_range: Кортеж (мин, макс) значений X.
    origin_x: Координата центра по X.
    origin_y: Координата центра по Y.
    step: Масштабный коэффициент (по умолчанию 50).
    color: Цвет линии графика (по умолчанию синий).
    """
    prev_x, prev_y = None, None  # Переменные для хранения предыдущих точек
    for x in range(x_range[0] * step, x_range[1] * step):  # Перебираем точки
        real_x = x / step  # Преобразуем координату X в реальное значение
        real_y = func(real_x)  # Вычисляем Y
        screen_x = origin_x + x  # Переводим в координаты холста
        screen_y = origin_y - real_y * step  # Инвертируем Y для отображения на экране
        if prev_x is not None:
            canvas.create_line(prev_x, prev_y, screen_x, screen_y, fill=color)  # Рисуем линию между точками
        prev_x, prev_y = screen_x, screen_y  # Обновляем предыдущие точки

def find_root(func, a, b, precision=0.001):
    """
    Находит корень уравнения f(x) = 0 методом бисекции.
    
    func: Функция, для которой ищется корень.
    a: Левая граница поиска.
    b: Правая граница поиска.
    precision: Точность вычисления корня (по умолчанию 0.001).
    return: Приближенное значение корня.
    """
    while abs(b - a) > precision:  # Пока разница больше точности
        mid = (a + b) / 2  # Находим середину отрезка
        if func(mid) == 0:
            return mid  # Если нашли точный корень
        elif func(mid) * func(a) < 0:
            b = mid  # Корень в левой половине
        else:
            a = mid  # Корень в правой половине
    root = (a + b) / 2  # Возвращаем приближенное значение
    print(f"Корень: {root:.3f}, 0.000")  # Выводим корень функции
    return root

def highlight_root(canvas, root, origin_x, origin_y, step=50, color='red'):
    """
    Отмечает найденный корень на графике.
    
    canvas: Объект холста Tkinter.
    root: Найденное значение корня.
    origin_x: Координата центра по X.
    origin_y: Координата центра по Y.
    step: Масштабный коэффициент (по умолчанию 50).
    color: Цвет точки корня (по умолчанию красный).
    """
    screen_x = origin_x + root * step  # Координата X на экране
    screen_y = origin_y - 0 * step  # Координата Y (по оси X)
    canvas.create_oval(screen_x - 5, screen_y - 5, screen_x + 5, screen_y + 5, fill=color)  # Рисуем точку корня
    canvas.create_text(screen_x + 10, screen_y - 10, text=f'{root:.3f}', fill=color)  # Добавляем подпись

def main():
    """
    Главная функция программы, создающая окно, рисующая оси, график и находящая корень.
    """
    root = tk.Tk()  # Создаем главное окно
    root.title("График функции")  # Устанавливаем заголовок
    
    canvas = create_canvas(root)  # Создаем холст
    center_x, center_y = 400, 300  # Определяем центр координат
    scale = 50  # Масштаб
    
    draw_axes(canvas, center_x, center_y, step=scale)  # Рисуем оси
    
    # Строим график перевёрнутой параболы
    plot_function(canvas, lambda x: -x**2 + 2, (-5, 5), center_x, center_y, step=scale)
    
    # Находим корень функции -x^2 + 2 в интервале от -2 до 2
    root_x = find_root(lambda x: -x**2 + 2, -2, 2)
    highlight_root(canvas, root_x, center_x, center_y, step=scale)  # Выделяем найденный корень
    
    # Выводим координаты точки пересечения с осью Y
    y_intersection = 2  # Пересечение с осью Y для функции f(x) = -x^2 + 2 происходит при x=0, y=2
    print(f"Пересечение с осью Y: (0, {y_intersection})")

    root.mainloop()  # Запускаем главный цикл Tkinter

if __name__ == "__main__":
    main()  # Запуск программы
