import tkinter as tk
import math

# --- Исходные параметры ---
a, b = 0.0, 1.0
n = 10
scale = 100
center_x, center_y = 400, 300
graph_start, graph_end = -5, 5

# --- Целевая функция ---
def f(x):
    return math.tan(x)

# --- Метод Симпсона ---
def simpson_method(func, start, end, steps):
    if steps % 2 != 0:
        steps += 1
    h = (end - start) / steps
    total = 0
    try:
        total += func(start) + func(end)
    except:
        return float('nan')
    for i in range(1, steps):
        x = start + i * h
        coeff = 4 if i % 2 != 0 else 2
        try:
            total += coeff * func(x)
        except:
            continue
    return (h / 3) * total

# --- Рисуем оси ---
def draw_axes(canvas):
    canvas.create_line(0, center_y, 800, center_y, arrow=tk.LAST)
    canvas.create_line(center_x, 0, center_x, 600, arrow=tk.LAST)
    for i in range(-10, 11):
        x = center_x + i * scale
        y = center_y - i * scale
        canvas.create_line(x, center_y - 4, x, center_y + 4)
        canvas.create_line(center_x - 4, y, center_x + 4, y)
        if i != 0:
            canvas.create_text(x, center_y + 15, text=str(i))
            canvas.create_text(center_x + 20, y, text=str(i))

# --- Рисуем график функции ---
def draw_function(canvas):
    step = 0.01
    x = graph_start
    prev = None
    while x <= graph_end:
        try:
            y = f(x)
            if abs(y) > 1e4:
                prev = None
                x += step
                continue
            sx = center_x + x * scale
            sy = center_y - y * scale
        except:
            prev = None
            x += step
            continue
        if prev:
            canvas.create_line(prev[0], prev[1], sx, sy, fill="blue")
        prev = (sx, sy)
        x += step

# --- Рисуем визуализацию Симпсона ---
def draw_simpson(canvas):
    global a, b, n
    steps = n
    if steps % 2 != 0:
        steps += 1
    h = (b - a) / steps
    for i in range(0, steps, 2):
        x0 = a + i*h
        x1 = x0 + h
        x2 = x0 + 2*h
        try:
            y0 = f(x0)
            y1 = f(x1)
            y2 = f(x2)
        except:
            continue
        poly = []
        for k in range(21):
            t = k / 20
            xt = x0 + 2*h*t
            L0 = (1 - t)*(1 - 2*t)
            L1 = 4 * t * (1 - t)
            L2 = t * (2*t - 1)
            yt = y0*L0 + y1*L1 + y2*L2
            sx = center_x + xt * scale
            sy = center_y - yt * scale
            poly.append((sx, sy))
        poly.append((center_x + x2*scale, center_y))
        poly.append((center_x + x0*scale, center_y))
        coords = [c for p in poly for c in p]
        canvas.create_polygon(coords, fill="#c2f0c2", outline="green")

# --- Перерисовка ---
def run_method():
    global a, b, n, scale
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
    except ValueError:
        result_label.config(text="Ошибка: некорректный ввод a или b")
        return

    canvas.delete("all")
    draw_axes(canvas)
    draw_function(canvas)
    draw_simpson(canvas)
    try:
        result = simpson_method(f, a, b, n)
        result_label.config(text=f"Симпсон: {result:.6f}")
    except Exception as e:
        result_label.config(text=f"Ошибка вычисления: {e}")

# --- Обновление масштаба ---
def update_scale(val):
    global scale
    scale = int(val)
    run_method()

# --- Обновление количества сегментов ---
def update_n(val):
    global n
    n = int(val)
    run_method()

# --- UI ---
root = tk.Tk()
root.title("Метод Симпсона — tan(x) + масштаб + ввод границ + количество сегментов")
root.resizable(False, False)

canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# --- Контрольная панель ---
control_frame = tk.Frame(root)
control_frame.pack(pady=5)

tk.Label(control_frame, text="a =").pack(side=tk.LEFT)
entry_a = tk.Entry(control_frame, width=8)
entry_a.pack(side=tk.LEFT)
entry_a.insert(0, str(a))

tk.Label(control_frame, text="b =").pack(side=tk.LEFT)
entry_b = tk.Entry(control_frame, width=8)
entry_b.pack(side=tk.LEFT)
entry_b.insert(0, str(b))

btn_run = tk.Button(control_frame, text="Вычислить", command=run_method)
btn_run.pack(side=tk.LEFT, padx=10)

# --- Масштаб ---
scale_frame = tk.Frame(root)
scale_frame.pack()

tk.Label(scale_frame, text="Масштаб").pack()
scale_slider = tk.Scale(scale_frame, from_=30, to=300,
                        orient=tk.HORIZONTAL, command=update_scale)
scale_slider.set(scale)
scale_slider.pack()

# --- Кол-во сегментов ---
segments_frame = tk.Frame(root)
segments_frame.pack()

tk.Label(segments_frame, text="Сегменты (n)").pack()
segments_slider = tk.Scale(segments_frame, from_=2, to=200, resolution=2,
                           orient=tk.HORIZONTAL, command=update_n)
segments_slider.set(n)
segments_slider.pack()

# --- Результат ---
result_label = tk.Label(root, text="Симпсон: ", font=("Arial", 12))
result_label.pack(pady=5)

# --- Первый запуск ---
run_method()
root.mainloop()
