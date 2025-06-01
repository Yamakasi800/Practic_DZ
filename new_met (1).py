import tkinter as tk

def init_window(width: int, height: int):
    """
    Создаёт окно и холст для рисования.
    """
    window = tk.Tk()
    window.title("Метод Ньютона")
    window.geometry(f"{width}x{height}")
    canvas = tk.Canvas(window, width=width, height=height, bg="black")
    canvas.pack()
    return window, canvas

def draw_axes(canvas, width: int, height: int, scale: float):
    """
    Рисует оси координат с делениями.
    """
    center_x, center_y = width // 2, height // 2

    # Оси
    canvas.create_line(0, center_y, width, center_y, fill="white", width=2)
    canvas.create_line(center_x, 0, center_x, height, fill="white", width=2)

    # Деления и подписи
    for i in range(-10, 11):
        if i != 0:
            canvas.create_line(center_x + i * scale, center_y - 5, center_x + i * scale, center_y + 5, fill="white")
            canvas.create_text(center_x + i * scale, center_y + 15, text=str(i), fill="white", font=("Arial", 8))

            canvas.create_line(center_x - 5, center_y - i * scale, center_x + 5, center_y - i * scale, fill="white")
            canvas.create_text(center_x + 15, center_y - i * scale, text=str(i), fill="white", font=("Arial", 8))

def func(x):
    """
    Целевая функция: f(x) = x^2 - 2
    """
    return x ** 2 - 2

def func_derivative(x):
    """
    Производная функции: f'(x) = 2x
    """
    return 2 * x

def plot_function(canvas, width: int, height: int, scale: float, step=0.05):
    """
    Рисует график функции f(x).
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

def draw_tangent(canvas, width: int, height: int, x0: float, y0: float, slope: float, scale: float):
    """
    Рисует касательную к графику функции в точке (x0, y0).
    """
    center_x, center_y = width // 2, height // 2
    x_left = x0 - 1
    x_right = x0 + 1
    y_left = y0 - slope
    y_right = y0 + slope

    canvas.create_line(
        center_x + x_left * scale, center_y - y_left * scale,
        center_x + x_right * scale, center_y - y_right * scale,
        fill="orange", width=2
    )

def mark_root(canvas, width: int, height: int, x_root: float, scale: float):
    """
    Отмечает найденный корень на графике.
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

def newton_visualization(canvas, width: int, height: int, start_x: float, scale: float, tolerance=1e-4, iterations=10):
    """
    Метод Ньютона с визуализацией процесса нахождения корня.
    """
    x = start_x
    for _ in range(iterations):
        y = func(x)
        dy = func_derivative(x)
        if abs(y) < tolerance:
            break
        draw_tangent(canvas, width, height, x, y, dy, scale)
        x = x - y / dy
    mark_root(canvas, width, height, x, scale)

if __name__ == "__main__":
    width, height = 800, 800
    scale = 30  # Пикселей на 1 единицу

    window, canvas = init_window(width, height)
    draw_axes(canvas, width, height, scale)
    plot_function(canvas, width, height, scale)
    newton_visualization(canvas, width, height, start_x=1.5, scale=scale)

    window.mainloop()
