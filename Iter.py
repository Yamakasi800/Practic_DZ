import tkinter as tk

def create_window_with_canvas(width: int, height: int):
    '''
    Создает главное окно и канвас для рисования.
    '''
    root = tk.Tk()
    root.title("Метод простой итерации")
    root.geometry(f"{width}x{height}")
    # Фон канваса — тёмно-синий
    canvas = tk.Canvas(root, width=width, height=height, bg="#0a0f2a")
    canvas.pack()
    return root, canvas

def draw_axes_with_ticks(canvas, width: int, height: int, scale: float):
    '''
    Рисует оси X и Y с делениями и подписанными метками.
    '''
    # Оси — светло-серые
    axis_color = "#dddddd"
    canvas.create_line(width // 2, 0, width // 2, height, fill=axis_color, width=2)
    canvas.create_line(0, height // 2, width, height // 2, fill=axis_color, width=2)

    arrow = 15
    # Стрелка X — светло-серый
    canvas.create_polygon(
        width - arrow, height // 2 - arrow // 2,
        width,       height // 2,
        width - arrow, height // 2 + arrow // 2,
        fill=axis_color
    )
    canvas.create_text(width - arrow - 10, height // 2 + 15,
                       text="X", font=("Arial", 12, "bold"), fill=axis_color)

    # Стрелка Y — светло-серый
    canvas.create_polygon(
        width // 2 - arrow // 2, arrow,
        width // 2,             0,
        width // 2 + arrow // 2,arrow,
        fill=axis_color
    )
    canvas.create_text(width // 2 + 15, arrow + 5,
                       text="Y", font=("Arial", 12, "bold"), fill=axis_color)

    # Деления и метки — чуть темнее осей
    tick_color = "#bbbbbb"
    for i in range(-10, 11):
        if i == 0:
            continue
        # деление по X
        canvas.create_line(
            width // 2 + i * scale, height // 2 - 5,
            width // 2 + i * scale, height // 2 + 5,
            fill=tick_color
        )
        canvas.create_text(
            width // 2 + i * scale, height // 2 + 15,
            text=str(i), font=("Arial", 10), fill=tick_color
        )
        # деление по Y
        canvas.create_line(
            width // 2 - 5, height // 2 - i * scale,
            width // 2 + 5, height // 2 - i * scale,
            fill=tick_color
        )
        canvas.create_text(
            width // 2 + 15, height // 2 - i * scale,
            text=str(i), font=("Arial", 10), fill=tick_color
        )

def f(x):
    return x**2 - 2

def g(x):
    return 0.5 * (x + 2 / x)

def draw_graph(canvas, width, height, func, scale, step=0.1):
    '''
    Рисует график функции.
    '''
    graph_color = "#00ff00"  # ярко-зелёный
    x = -10.0
    while x <= 10.0:
        x1, y1 = x, func(x)
        x2, y2 = x + step, func(x + step)
        canvas.create_line(
            width // 2 + x1 * scale, height // 2 - y1 * scale,
            width // 2 + x2 * scale, height // 2 - y2 * scale,
            fill=graph_color, width=2
        )
        x += step

def draw_iteration(canvas, width, height, x0, x1, scale):
    '''
    Рисует шаг итерации.
    '''
    iter_color = "#ff00ff"  # магента
    # вертикальная линия
    canvas.create_line(
        width // 2 + x0 * scale, height // 2 - x0 * scale,
        width // 2 + x0 * scale, height // 2 - x1 * scale,
        fill=iter_color, dash=(3,3)
    )
    # горизонтальная линия
    canvas.create_line(
        width // 2 + x0 * scale, height // 2 - x1 * scale,
        width // 2 + x1 * scale, height // 2 - x1 * scale,
        fill=iter_color, dash=(3,3)
    )

def plot_root(canvas, width, height, root_x, scale):
    '''
    Помечает найденный корень.
    '''
    root_color = "#ff0000"  # красный
    root_y = f(root_x)
    r = 5
    canvas.create_oval(
        width // 2 + root_x * scale - r, height // 2 - root_y * scale - r,
        width // 2 + root_x * scale + r, height // 2 - root_y * scale + r,
        fill=root_color
    )
    canvas.create_text(
        width // 2 + root_x * scale + 10,
        height // 2 - root_y * scale - 10,
        text=f"{root_x:.4f}",
        font=("Arial", 12),
        fill=root_color
    )

def simple_iteration_method(canvas, width, height, x0, scale, tol=1e-4, max_iter=20):
    '''
    Метод простой итерации для уравнения f(x) = 0.
    '''
    for _ in range(max_iter):
        x1 = g(x0)
        draw_iteration(canvas, width, height, x0, x1, scale)
        if abs(x1 - x0) < tol:
            break
        x0 = x1
    plot_root(canvas, width, height, x0, scale)

if __name__ == "__main__":
    width, height = 700, 700
    scale = 100
    root, canvas = create_window_with_canvas(width, height)
    draw_axes_with_ticks(canvas, width, height, scale)
    draw_graph(canvas, width, height, f, scale)
    simple_iteration_method(canvas, width, height, x0=1.0, scale=scale)
    root.mainloop()
