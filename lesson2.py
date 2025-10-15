import tkinter as tk
from tkinter import ttk
from datetime import datetime

# ---------- Данные ----------
bookings = [
    ["00008", "10.08.2025", "Одноместный эконом"],
    ["00010", "12.08.2025", "Бизнес с 1 или 2 кроватями"],
]
filtered_bookings = bookings.copy()

# ---------- Функции ----------
def str_to_date(s):
    """Преобразует строку 'дд.мм.гггг' в объект datetime"""
    try:
        return datetime.strptime(s, "%d.%m.%Y")
    except ValueError:
        return None

def update_table():
    """Обновляет таблицу"""
    for row in table.get_children():
        table.delete(row)
    for b in filtered_bookings:
        table.insert("", "end", values=b)

def filter_data():
    """Фильтрует записи по диапазону дат"""
    global filtered_bookings
    s = str_to_date(entry_start.get())
    e = str_to_date(entry_end.get())
    if not s or not e:
        return
    filtered_bookings = [b for b in bookings if s <= str_to_date(b[1]) <= e]
    update_table()

def show_all():
    """Показывает все записи"""
    global filtered_bookings
    filtered_bookings = bookings.copy()
    update_table()

def create_booking():
    """Создаёт новую запись"""
    new_id = f"{int(bookings[-1][0]) + 1:05d}" if bookings else "00001"
    bookings.append([new_id, "01.01.2026", "Новая категория"])
    show_all()

def delete_booking():
    """Удаляет выделенную запись"""
    selected = table.selection()
    if not selected:
        return
    booking_id = table.item(selected[0])["values"][0]
    for b in bookings:
        if b[0] == booking_id:
            bookings.remove(b)
            break
    show_all()

# ---------- Окно ----------
root = tk.Tk()
root.title("Работа с бронированием номеров")
root.geometry("600x400")

# ---------- Верхняя панель ----------
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Укажите период с").grid(row=0, column=0, padx=5)

entry_start = tk.Entry(frame_top, width=12, justify="center")
entry_start.insert(0, "10.08.2025")
entry_start.grid(row=0, column=1)

tk.Label(frame_top, text="по").grid(row=0, column=2, padx=5)

entry_end = tk.Entry(frame_top, width=12, justify="center")
entry_end.insert(0, "15.08.2025")
entry_end.grid(row=0, column=3)

tk.Button(frame_top, text="Фильтровать", command=filter_data).grid(row=0, column=4, padx=5)
tk.Button(frame_top, text="Показать все", command=show_all).grid(row=0, column=5, padx=5)

# ---------- Кнопки управления ----------
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Создать", width=15, command=create_booking).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Удалить", width=15, command=delete_booking).grid(row=0, column=1, padx=10)

# ---------- Таблица ----------
frame_table = tk.Frame(root)
frame_table.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("id", "date", "category")
table = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)

table.heading("id", text="Номер бронирования")
table.heading("date", text="Дата заезда")
table.heading("category", text="Категория размещения")

table.column("id", width=150, anchor="center")
table.column("date", width=150, anchor="center")
table.column("category", width=250, anchor="center")

table.pack(fill="both", expand=True)

# ---------- Первичное обновление ----------
update_table()

root.mainloop()
