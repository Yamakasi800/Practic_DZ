import tkinter as tk

def init_window(width: int, height: int):
    """
    Инициализирует окно tkinter и создаёт канвас для рисования.
        width (int): Ширина окна в пикселях.
        height (int): Высота окна в пикселях.

    функция возвращает
        tuple: Объекты окна (window) и канваса (canvas).
    """
    window = tk.Tk()
    window.title("Метод Секущих")
    window.geometry(f"{width}x{height}")
    canvas = tk.Canvas(window, width=width, height=height, bg="black")
    canvas.pack()
    return window, canvas

def draw_axes(canvas, width: int, height: int, scale: float):
    """
    Рисует оси координат X и Y с делениями и подписями.
        canvas (tk.Canvas): Канвас для рисования.
        width (int): Ширина окна в пикселях.
        height (int): Высота окна в пикселях.
        scale (float): Количество пикселей на одну единицу координат.
    """
    center_x, center_y = width // 2, height // 2
    canvas.create_line(0, center_y, width, center_y, fill="white", width=2)
    canvas.create_line(center_x, 0, center_x, height, fill="white", width=2)
    
    for i in range(-10, 11):
        if i != 0:
            canvas.create_line(center_x + i * scale, center_y - 5, center_x + i * scale, center_y + 5, fill="white")
            canvas.create_text(center_x + i * scale, center_y + 15, text=str(i), fill="white", font=("Arial", 8))
            
            canvas.create_line(center_x - 5, center_y - i * scale, center_x + 5, center_y - i * scale, fill="white")
            canvas.create_text(center_x + 15, center_y - i * scale, text=str(i), fill="white", font=("Arial", 8))

def func(x):
    """
    Вычисляет значение функции f(x) = x^2 - 2.

    Args:
        x (float): Аргумент функции.

    Returns:
        float: Значение функции в точке x.
    """
    return x ** 2 - 2

def plot_function(canvas, width: int, height: int, scale: float, step=0.05):
    """
    Строит график функции f(x)
        canvas (tk.Canvas): поле для рисования.
        width (int): Ширина окна.
        height (int): Высота окна.
        scale (float): Масштаб координат.
        step (float, optional): Шаг по оси X для прорисовки (по умолчанию 0.05).
    """
    center_x, center_y = width // 2, height // 2
    x = -10
    while x <= 10:
        x1, y1 = x, func(x)
        x2, y2 = x + step, func(x + step)
        canvas.create_line(
            center_x + x1 * scale, center_y - y1 * scale,
            center_x + x2 * scale, center_y - y2 * scale,
            fill="cyan", width=2
        )
        x += step

def draw_secant(canvas, width: int, height: int, x0: float, y0: float, x1: float, y1: float, scale: float):
    """
    Рисует секущую линию между двумя точками (x0, y0) и (x1, y1).
        canvas (tk.Canvas): Канвас для рисования.
        width (int): Ширина окна.
        height (int): Высота окна.
        x0 (float): Абсцисса первой точки.
        y0 (float): Ордината первой точки.
        x1 (float): Абсцисса второй точки.
        y1 (float): Ордината второй точки.
        scale (float): Масштаб координат.
    """
    center_x, center_y = width // 2, height // 2
    canvas.create_line(
        center_x + x0 * scale, center_y - y0 * scale,
        center_x + x1 * scale, center_y - y1 * scale,
        fill="orange", width=2
    )

def mark_root(canvas, width: int, height: int, x_root: float, scale: float):
    """
    Отмечает найденный корень на графике.
        canvas (tk.Canvas): Канвас для рисования.
        width (int): Ширина окна.
        height (int): Высота окна.
        x_root (float): Найденный корень функции.
        scale (float): Масштаб координат.
    """
    center_x, center_y = width // 2, height // 2
    y_root = func(x_root)
    canvas.create_oval(
        center_x + x_root * scale - 4, center_y - y_root * scale - 4,
        center_x + x_root * scale + 4, center_y - y_root * scale + 4,
        fill="red"
    )
    canvas.create_text(center_x + x_root * scale + 10, center_y - y_root * scale - 10,
                       text=f"{x_root:.4f}", fill="red", font=("Arial", 10, "bold"))

def secant_visualization(canvas, width: int, height: int, x0: float, x1: float, scale: float, tol=1e-4, max_iter=20):
    """
    Реализует метод секущих с визуализацией процесса на графике.
        canvas (tk.Canvas): Канвас для рисования.
        width (int): Ширина окна.
        height (int): Высота окна.
        x0 (float): Первое начальное приближение.
        x1 (float): Второе начальное приближение.
        scale (float): Масштаб координат.
        tol (float, optional): Допустимая погрешность нахождения корня (по умолчанию 1e-4).
        max_iter (int, optional): Максимальное количество итераций (по умолчанию 20).
    """
    for _ in range(max_iter):
        y0 = func(x0)
        y1 = func(x1)

        if abs(y1 - y0) < 1e-12:
            break

        draw_secant(canvas, width, height, x0, y0, x1, y1, scale)

        x2 = x1 - y1 * (x1 - x0) / (y1 - y0)

        if abs(x2 - x1) < tol:
            mark_root(canvas, width, height, x2, scale)
            return

        x0, x1 = x1, x2

    mark_root(canvas, width, height, x1, scale)

if __name__ == "__main__":
    width, height = 800, 800
    scale = 80  # Пикселей на единицу координат

    window, canvas = init_window(width, height)
    draw_axes(canvas, width, height, scale)
    plot_function(canvas, width, height, scale)
    secant_visualization(canvas, width, height, x0=1.0, x1=2.0, scale=scale)

    window.mainloop()
