# sales.py
from tkinter import *
from tkinter import ttk, messagebox
from db import session, Sale, Product

def SalesWindow():
    win = Toplevel()
    win.title("Продажи")
    win.geometry("700x520")
    win.configure(bg="#FFF8DC")

    Label(win, text="Продажи", font=("Arial", 18, "bold"), bg="#FFF8DC").pack(pady=8)

    # Таблица продаж
    table_frame = Frame(win, bg="#FFF8DC")
    table_frame.pack(padx=10, pady=5, fill=BOTH, expand=True)

    columns = ("id", "product", "quantity", "price")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", rowheight=24, font=("Arial", 10))

    tree.heading("product", text="Продукт")
    tree.heading("quantity", text="Кол-во")
    tree.heading("price", text="Сумма (₽)")
    tree.column("id", width=0, stretch=NO)
    tree.column("product", width=380)
    tree.column("quantity", width=100, anchor="center")
    tree.column("price", width=140, anchor="e")

    scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)

    def load_sales():
        for r in tree.get_children():
            tree.delete(r)
        sales = session.query(Sale).order_by(Sale.id).all()
        for s in sales:
            pname = s.product.name if s.product else "—"
            tree.insert("", END, values=(s.id, pname, s.quantity, f"{s.price:,.2f} ₽"))

    load_sales()

    # Форма добавления/редактирования продажи
    def open_sale_window(edit_id=None):
        is_edit = edit_id is not None
        w = Toplevel(win)
        w.title("Изменение продажи" if is_edit else "Добавление продажи")
        w.geometry("480x420")
        w.configure(bg="#FFF8DC")

        Label(w, text=w.title(), font=("Arial", 14, "bold"), bg="#FFF8DC").pack(pady=10)
        form = Frame(w, bg="#FFF8DC")
        form.pack(padx=10, pady=5, fill=BOTH, expand=True)

        # product combobox
        Label(form, text="Продукт", bg="#FFF8DC", anchor="w").pack(fill=X, pady=(6,2))
        products = session.query(Product).order_by(Product.name).all()
        prod_map = {f"{p.name} (ID:{p.id})": p.id for p in products}
        prod_list = list(prod_map.keys())
        prod_box = ttk.Combobox(form, values=prod_list)
        prod_box.pack(fill=X)

        Label(form, text="Количество", bg="#FFF8DC", anchor="w").pack(fill=X, pady=(6,2))
        qty_ent = Entry(form)
        qty_ent.insert(0, "1")
        qty_ent.pack(fill=X)

        Label(form, text="Цена за единицу (₽)", bg="#FFF8DC", anchor="w").pack(fill=X, pady=(6,2))
        price_ent = Entry(form)
        price_ent.pack(fill=X)

        if is_edit:
            s = session.get(Sale, edit_id)
            if s:
                key = next((k for k, v in prod_map.items() if v == s.product_id), "")
                prod_box.set(key)
                qty_ent.delete(0, "end")
                qty_ent.insert(0, str(s.quantity))
                # если у тебя цена хранилась как total, то можно показать total/qty
                unit_price = s.price / s.quantity if s.quantity else 0
                price_ent.insert(0, f"{unit_price:.2f}")

        def save_sale():
            try:
                prod_sel = prod_box.get()
                if prod_sel not in prod_map:
                    messagebox.showwarning("Внимание", "Выберите продукт")
                    return
                product_id = prod_map[prod_sel]
                qty = int(qty_ent.get())
                unit_price = float(price_ent.get().replace(",", "."))
                total = qty * unit_price
                if is_edit:
                    s.product_id = product_id
                    s.quantity = qty
                    s.price = total
                else:
                    new_s = Sale(product_id=product_id, quantity=qty, price=total)
                    session.add(new_s)
                session.commit()
                load_sales()
                w.destroy()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", str(e))

        Button(w, text="Сохранить", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
               width=12, command=save_sale).pack(pady=10)
        Button(w, text="Отмена", bg="#F44336", fg="white", font=("Arial", 10, "bold"),
               width=12, command=w.destroy).pack()

    def add_sale():
        # проверяем, есть ли продукты
        if session.query(Product).count() == 0:
            messagebox.showwarning("Внимание", "Нет продуктов в базе. Добавьте продукт сначала.")
            return
        open_sale_window(None)

    def edit_sale():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Ошибка", "Выберите запись")
            return
        sid = tree.item(sel[0])["values"][0]
        open_sale_window(sid)

    def delete_sale():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Ошибка", "Выберите запись")
            return
        if not messagebox.askyesno("Подтвердите", "Удалить выбранную продажу?"):
            return
        sid = tree.item(sel[0])["values"][0]
        try:
            session.query(Sale).filter_by(id=sid).delete()
            session.commit()
            load_sales()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Ошибка", str(e))

    bottom = Frame(win, bg="#FFF8DC")
    bottom.pack(pady=8, padx=10, fill=X)

    Button(bottom, text="Добавить", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
           width=12, command=add_sale).pack(side=LEFT, padx=5)
    Button(bottom, text="Изменить", bg="#66BB6A", fg="white", font=("Arial", 10, "bold"),
           width=12, command=edit_sale).pack(side=LEFT, padx=5)
    Button(bottom, text="Удалить", bg="#F44336", fg="white", font=("Arial", 10, "bold"),
           width=12, command=delete_sale).pack(side=LEFT, padx=5)
    Button(bottom, text="Обновить", bg="#FFA726", fg="white", font=("Arial", 10, "bold"),
           width=12, command=load_sales).pack(side=LEFT, padx=5)
    Button(bottom, text="Назад", bg="#FF7043", fg="white", font=("Arial", 10, "bold"),
           width=12, command=win.destroy).pack(side=LEFT, padx=5)
