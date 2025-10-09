#
# окно с таблицей продукции product.py
#
#-------------------------------

from tkinter import *
from tkinter import ttk

def ProductWindow():
    
    product = Toplevel()
    product.title("Продукция")
    product.geometry("800x600")
    
    # Контент главного окна
    Label(product, text="Продукция").pack()

    Label(product, text="Поиск").pack()
    Entry(product).pack()

    # Фрейм для таблицы
    table_frame = Frame(product)
    table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

    # Создаем таблицу
    columns = ("name", "article", "type", "price")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    
    # Настраиваем заголовки
    tree.heading("name", text="Название продукции")
    tree.heading("article", text="Артикул")
    tree.heading("type", text="Тип продукции")
    tree.heading("price", text="Мин. стоимость")
    
    # Настраиваем ширину колонок
    tree.column("name", width=300)
    tree.column("article", width=100, anchor="center")
    tree.column("type", width=150)
    tree.column("price", width=120, anchor="e")
    
    # Добавляем скроллбар
    scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Данные для таблицы (как в вашем примере)
    products_data = [
        ("Инженерная доска Дуб Французская елка ...", "8858958", "Паркетная доска", "7 330,99 ₽"),
        ("Ламинат Дуб дымчато-белый 33 класс 12 ...", "7750282", "Ламинат", "1 799,33 ₽"),
        ("Ламинат Дуб серый 32 класс 8 мм с фаской", "7028748", "Ламинат", "3 890,41 ₽"),
        ("Паркетная доска Ясень темный однополо...", "8758385", "Паркетная доска", "4 456,90 ₽"),
        ("Пробковое напольное клеевое покрытие ...", "5012543", "Пробковое покрытие", "5 450,59 ₽")
    ]
    
    # Заполняем таблицу данными
    for item in products_data:
        tree.insert("", END, values=item)
    
    # Фрейм для кнопок и информации
    bottom_frame = Frame(product)
    bottom_frame.pack(pady=10, padx=20, fill=X)
    
    # Кнопки управления
    buttons_frame = Frame(bottom_frame)
    buttons_frame.pack(side=LEFT)
    
    Button(buttons_frame, text="Добавить", width=10).pack(side=LEFT, padx=5)
    Button(buttons_frame, text="Изменить", width=10).pack(side=LEFT, padx=5)
    Button(buttons_frame, text="Удалить", width=10).pack(side=LEFT, padx=5)
    Button(buttons_frame, text="Назад", width=10).pack(side=LEFT, padx=5)
    
    # Информация о записях
    info_frame = Frame(bottom_frame)
    info_frame.pack(side=RIGHT)
    
    Label(info_frame, text=f"Всего записей: {len(products_data)}", 
          font=("Arial", 10)).pack(side=RIGHT)
    

