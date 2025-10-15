import tkinter as tk
from tkinter import ttk
from datetime import datetime

# ----------------- ДАННЫЕ (в массивах) -----------------
# Формат: [Клиент, Телефон, Электронная почта, Дата заказа 'dd.mm.yyyy', Сотрудник]
bookings = [
    ["Иванов И. И.", "+762355889633", "ivan@yandex.ru", "25.02.2023", "Пестов А. М."],
    ["Иванов И. И.", "+762355889633", "ivan@yandex.ru", "15.03.2023", "Постов М. А."],
    ["Петров П. П.", "+795632258966", "petrov@mail.ru", "15.03.2023", "Пестов А. М."],
    ["Смирнов В. П.", "+792535165899", "smirnov@mail.ru", "15.05.2023", "Ткаченко И. В."],
]

filtered_bookings = bookings.copy()

# ----------------- ВСПОМОГАТЕЛЬНЫЕ -----------------
def parse_date(s):
    try:
        return datetime.strptime(s, "%d.%m.%Y")
    except Exception:
        return None

def refresh_client_options():
    clients = sorted({b[0] for b in bookings})
    combobox_clients['values'] = clients
    # по картинке на первом месте Иванов И. И.
    if "Иванов И. И." in clients:
        combobox_clients.set("Иванов И. И.")
    elif clients:
        combobox_clients.set(clients[0])
    else:
        combobox_clients.set("")

# ----------------- ЛОГИКА: фильтр/поиск/сортировка -----------------
def apply_filters_and_sort():
    global filtered_bookings
    result = bookings.copy()

    # 1) Фильтр по клиенту (если выбран)
    sel_client = combobox_clients.get().strip()
    if sel_client:
        result = [r for r in result if r[0] == sel_client]

    # 2) Поиск по строке (если заполнено) — подстрока в любой колонке
    query = entry_search.get().strip().lower()
    if query:
        def match(row):
            return any(query in str(col).lower() for col in row)
        result = [r for r in result if match(r)]

    # 3) Сортировка
    sel_idx = listbox_sort.curselection()
    field = "Клиент"
    if sel_idx:
        field = listbox_sort.get(sel_idx[0])
    reverse = (sort_var.get() == "desc")

    if field == "Клиент":
        result.sort(key=lambda x: x[0].lower(), reverse=reverse)
    elif field == "Дата заказа":
        result.sort(key=lambda x: parse_date(x[3]) or datetime.min, reverse=reverse)
    elif field == "Сотрудник":
        result.sort(key=lambda x: x[4].lower(), reverse=reverse)

    filtered_bookings = result
    update_table()

def on_filter_click():
    apply_filters_and_sort()

def on_show_all_click():
    # Сброс поиска, показать все (по картинке combobox содержит имя, но здесь логично оставить выбранным)
    entry_search.delete(0, tk.END)
    listbox_sort.selection_clear(0, tk.END)
    listbox_sort.selection_set(0)
    sort_var.set("asc")
    apply_filters_and_sort()

def on_find_click():
    apply_filters_and_sort()

# ----------------- CRUD (создать / удалить) -----------------
def add_entry():
    new = ["Новый Кл. Н. Н.", "+70000000000", "new@example.com", "01.01.2024", "Новый Сотрудник"]
    bookings.append(new)
    refresh_client_options()
    apply_filters_and_sort()

def delete_selected():
    sel = tree.selection()
    if not sel:
        return
    vals = tree.item(sel[0])["values"]
    # удалить первое совпадение в bookings
    for r in bookings:
        if [r[0], r[1], r[2], r[3], r[4]] == vals:
            bookings.remove(r)
            break
    refresh_client_options()
    apply_filters_and_sort()

# ----------------- GUI -----------------
root = tk.Tk()
root.title("Работа с заказами клиентов")
root.geometry("1000x480")  # примерно, чтобы разместить всё

# стиль для серой шапки таблицы
style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview.Heading", background="#d1d1d1", relief="raised")

# Верх: заголовок (как в картинке)
title_frame = tk.Frame(root)
title_frame.pack(fill="x", padx=6, pady=(6,0))
tk.Label(title_frame, text="Работа с заказами клиентов", anchor="w").pack(fill="x")

# Основная верхняя панель (фильтры/поиск/сортировка)
top_frame = tk.Frame(root, pady=6)
top_frame.pack(fill="x", padx=8)

# Левый сектор: выбор клиента + кнопки Фильтровать / Показать все
left_sector = tk.Frame(top_frame)
left_sector.pack(side="left", anchor="n")

tk.Label(left_sector, text="Выберите клиента").grid(row=0, column=0, sticky="w")
combobox_clients = ttk.Combobox(left_sector, state="readonly", width=28)
combobox_clients.grid(row=1, column=0, padx=(0,6), pady=4)

btn_filter = tk.Button(left_sector, text="Фильтровать", width=12, command=on_filter_click)
btn_filter.grid(row=1, column=1, padx=(4,4))
btn_show_all = tk.Button(left_sector, text="Показать все", width=12, command=on_show_all_click)
btn_show_all.grid(row=1, column=2, padx=(4,0))

# Средний сектор (слева под фильтрами): строка поиска и кнопка Найти
search_sector = tk.Frame(top_frame)
search_sector.pack(side="left", padx=24)

tk.Label(search_sector, text="Введите строку поиска").grid(row=0, column=0, sticky="w")
entry_search = tk.Entry(search_sector, width=36)
entry_search.grid(row=1, column=0, pady=4, sticky="w")
btn_find = tk.Button(search_sector, text="Найти", width=10, command=on_find_click)
btn_find.grid(row=1, column=1, padx=(8,0))

# Правый сектор: блок сортировки (как на картинке справа)
right_sector = tk.Frame(top_frame)
right_sector.pack(side="right", anchor="n")

tk.Label(right_sector, text="Выберите поле для сортировки").grid(row=0, column=0, sticky="w")

sort_frame = tk.Frame(right_sector)
sort_frame.grid(row=1, column=0, pady=4)

# Список полей сортировки (вертикально)
listbox_sort = tk.Listbox(sort_frame, height=3, width=20, exportselection=False)
for item in ["Клиент", "Дата заказа", "Сотрудник"]:
    listbox_sort.insert(tk.END, item)
listbox_sort.selection_set(0)
listbox_sort.grid(row=0, column=0)

# Радиокнопки справа от списка (вертикально)
sort_var = tk.StringVar(value="asc")
rb_frame = tk.Frame(sort_frame)
rb_frame.grid(row=0, column=1, padx=8, sticky="n")
tk.Radiobutton(rb_frame, text="По возрастанию", variable=sort_var, value="asc").pack(anchor="w")
tk.Radiobutton(rb_frame, text="По убыванию", variable=sort_var, value="desc").pack(anchor="w")

# Нижняя часть: кнопки Создать/Удалить слева и таблица под ними
controls_frame = tk.Frame(root, pady=6)
controls_frame.pack(fill="x", padx=8)

btn_create = tk.Button(controls_frame, text="Создать", width=12, command=add_entry)
btn_create.pack(side="left", padx=(4,6))
btn_delete = tk.Button(controls_frame, text="Удалить", width=12, command=delete_selected)
btn_delete.pack(side="left", padx=(0,6))

# Таблица (колонки в нужном порядке)
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=8, pady=(0,8))

cols = ("client", "phone", "email", "order_date", "employee")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)

tree.heading("client", text="Клиент")
tree.heading("phone", text="Телефон")
tree.heading("email", text="Электронная почта")
tree.heading("order_date", text="Дата заказа")
tree.heading("employee", text="Сотрудник")

tree.column("client", anchor="w", width=260)
tree.column("phone", anchor="center", width=140)
tree.column("email", anchor="w", width=300)
tree.column("order_date", anchor="center", width=110)
tree.column("employee", anchor="w", width=200)

vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
tree.pack(fill="both", expand=True, side="left")

# Обновление таблицы
def update_table():
    for it in tree.get_children():
        tree.delete(it)
    for r in filtered_bookings:
        tree.insert("", "end", values=r)

# Инициализация
refresh_client_options()
listbox_sort.selection_set(0)
sort_var.set("asc")
apply_filters_and_sort()

root.mainloop()
