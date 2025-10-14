
#
# окно с продажами product.py
#
#-------------------------------

from tkinter import *
from tkinter import ttk, messagebox
from db import session, Product

def ProductWindow():
    win = Toplevel()
    win.title("Продукция")
    win.geometry("950x550")
    win.configure(bg="#FFF8DC")

    Label(win, text="Продукция", font=("Arial", 18, "bold"), bg="#FFF8DC").pack(pady=10)

    # Поиск
    search_var = StringVar()
    search_frame = Frame(win, bg="#FFF8DC")
    search_frame.pack(pady=5)
    Label(search_frame, text="Поиск:", bg="#FFF8DC", font=("Arial", 10)).pack(side=LEFT, padx=5)
    search_entry = Entry(search_frame, textvariable=search_var, width=40)
    search_entry.pack(side=LEFT, padx=5)

    # Таблица
    table_frame = Frame(win, bg="#FFF8DC")
    table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

    columns = ("id", "name", "article", "type", "price")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", rowheight=26, font=("Arial", 10))

    tree.heading("name", text="Название продукции")
    tree.heading("article", text="Артикул")
    tree.heading("type", text="Тип продукции")
    tree.heading("price", text="Мин. стоимость")
    tree.column("id", width=0, stretch=NO)
    tree.column("name", width=400)
    tree.column("article", width=120, anchor="center")
    tree.column("type", width=180, anchor="center")
    tree.column("price", width=120, anchor="e")

    scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)

    def load_products(filter_text: str = ""):
        for r in tree.get_children():
            tree.delete(r)
        query = session.query(Product)
        if filter_text:
            like = f"%{filter_text}%"
            query = query.filter(Product.name.ilike(like) | Product.article.ilike(like) | Product.type.ilike(like))
        products = query.order_by(Product.id).all()
        for p in products:
            tree.insert("", END, values=(p.id, p.name, p.article or "", p.type or "", f"{p.price:,.2f} ₽"))

    load_products()

    def on_search(*args):
        load_products(search_var.get())

    search_var.trace_add("write", on_search)

    # Формы добавления / редактирования
    def open_edit_window(item_id=None):
        is_edit = item_id is not None
        edit = Toplevel(win)
        edit.title("Изменение продукции" if is_edit else "Добавление продукции")
        edit.geometry("420x380")
        edit.configure(bg="#FFF8DC")

        Label(edit, text=edit.title(), font=("Arial", 14, "bold"), bg="#FFF8DC").pack(pady=10)
        form = Frame(edit, bg="#FFF8DC")
        form.pack(pady=5, padx=10, fill=BOTH, expand=True)

        lbls = ["Название", "Артикул", "Тип", "Стоимость"]
        entries = {}
        for l in lbls:
            Label(form, text=l, bg="#FFF8DC", anchor="w").pack(fill=X, pady=(8, 2))
            ent = Entry(form)
            ent.pack(fill=X)
            entries[l] = ent

        if is_edit:
            p = session.get(Product, item_id)
            if p:
                entries["Название"].insert(0, p.name)
                entries["Артикул"].insert(0, p.article or "")
                entries["Тип"].insert(0, p.type or "")
                entries["Стоимость"].insert(0, str(p.price))

        def save():
            try:
                name = entries["Название"].get().strip()
                if not name:
                    messagebox.showwarning("Внимание", "Название обязательно")
                    return
                article = entries["Артикул"].get().strip()
                ptype = entries["Тип"].get().strip()
                price_text = entries["Стоимость"].get().strip() or "0"
                price = float(price_text.replace(",", "."))
                if is_edit:
                    p.name = name
                    p.article = article
                    p.type = ptype
                    p.price = price
                else:
                    new_p = Product(name=name, article=article, type=ptype, price=price)
                    session.add(new_p)
                session.commit()
                load_products(search_var.get())
                edit.destroy()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", str(e))

        Button(edit, text="Сохранить", bg="#4CAF50", fg="white",
               font=("Arial", 10, "bold"), width=12, command=save).pack(pady=10)
        Button(edit, text="Отмена", bg="#F44336", fg="white",
               font=("Arial", 10, "bold"), width=12, command=edit.destroy).pack()

    def add_product():
        open_edit_window(None)

    def edit_product():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Ошибка", "Выберите запись для изменения")
            return
        item = tree.item(sel[0])["values"]
        pid = item[0]
        open_edit_window(pid)

    def delete_product():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Ошибка", "Выберите запись для удаления")
            return
        if not messagebox.askyesno("Подтвердите", "Удалить выбранную запись?"):
            return
        pid = tree.item(sel[0])["values"][0]
        try:
            session.query(Product).filter_by(id=pid).delete()
            session.commit()
            load_products(search_var.get())
        except Exception as e:
            session.rollback()
            messagebox.showerror("Ошибка", str(e))

    bottom = Frame(win, bg="#FFF8DC")
    bottom.pack(pady=12, padx=20, fill=X)

    Button(bottom, text="Добавить", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
           width=12, command=add_product).pack(side=LEFT, padx=5)
    Button(bottom, text="Изменить", bg="#66BB6A", fg="white", font=("Arial", 10, "bold"),
           width=12, command=edit_product).pack(side=LEFT, padx=5)
    Button(bottom, text="Удалить", bg="#F44336", fg="white", font=("Arial", 10, "bold"),
           width=12, command=delete_product).pack(side=LEFT, padx=5)
    Button(bottom, text="Обновить", bg="#FFA726", fg="white", font=("Arial", 10, "bold"),
           width=12, command=lambda: load_products(search_var.get())).pack(side=LEFT, padx=5)
    Button(bottom, text="Назад", bg="#FF7043", fg="white", font=("Arial", 10, "bold"),
           width=12, command=win.destroy).pack(side=LEFT, padx=5)

    Label(bottom, text="База: data.db", bg="#FFF8DC", font=("Arial", 10, "italic")).pack(side=RIGHT)