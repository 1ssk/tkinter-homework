# partner.py
from tkinter import *
from tkinter import ttk, messagebox
from db import session, Partner

def PartnerWindow():
    win = Toplevel()
    win.title("Добавление партнёра")
    win.geometry("700x650")
    win.configure(bg="#FFF8DC")

    Label(win, text="Партнёры", font=("Arial", 18, "bold"), bg="#FFF8DC").pack(pady=8)

    # Верх — поиск и кнопки
    top = Frame(win, bg="#FFF8DC")
    top.pack(pady=5, padx=10, fill=X)

    search_var = StringVar()
    Label(top, text="Поиск:", bg="#FFF8DC").pack(side=LEFT, padx=(0,6))
    Entry(top, textvariable=search_var, width=40).pack(side=LEFT)

    # Таблица
    table_frame = Frame(win, bg="#FFF8DC")
    table_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

    columns = ("id", "org_type", "org_name", "director", "phone", "email", "address", "inn", "rating")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", rowheight=24, font=("Arial", 10))

    headings = {
        "org_type": "Тип",
        "org_name": "Наименование",
        "director": "ФИО директора",
        "phone": "Телефон",
        "email": "Email",
        "address": "Юр. адрес",
        "inn": "ИНН",
        "rating": "Рейтинг"
    }
    for col in columns:
        if col == "id":
            tree.column("id", width=0, stretch=NO)
            continue
        tree.heading(col, text=headings.get(col, col))
        tree.column(col, width=120)

    scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)

    def load_partners(filter_text=""):
        for r in tree.get_children():
            tree.delete(r)
        q = session.query(Partner)
        if filter_text:
            like = f"%{filter_text}%"
            q = q.filter(Partner.org_name.ilike(like) | Partner.director.ilike(like) | Partner.phone.ilike(like))
        for p in q.order_by(Partner.id).all():
            tree.insert("", END, values=(
                p.id, p.org_type or "", p.org_name, p.director or "", p.phone or "", p.email or "", p.address or "", p.inn or "", p.rating or 0
            ))

    load_partners()

    def on_search(*args):
        load_partners(search_var.get())
    search_var.trace_add("write", on_search)

    def open_partner_window(edit_id=None):
        is_edit = edit_id is not None
        w = Toplevel(win)
        w.title("Изменение партнёра" if is_edit else "Добавление партнёра")
        w.geometry("520x560")
        w.configure(bg="#FFF8DC")

        Label(w, text=w.title(), font=("Arial", 14, "bold"), bg="#FFF8DC").pack(pady=10)
        form = Frame(w, bg="#FFF8DC")
        form.pack(padx=10, pady=5, fill=BOTH, expand=True)

        def add_field(label_text):
            Label(form, text=label_text, bg="#FFF8DC", anchor="w").pack(fill=X, pady=(6,2))
            ent = Entry(form)
            ent.pack(fill=X)
            return ent

        org_types = ["ООО", "ИП", "Другой"]
        org_box = ttk.Combobox(form, values=org_types)
        Label(form, text="Тип организации", bg="#FFF8DC", anchor="w").pack(fill=X, pady=(6,2))
        org_box.pack(fill=X)

        name_ent = add_field("Наименование организации")
        director_ent = add_field("ФИО директора")
        phone_ent = add_field("Телефон")
        email_ent = add_field("Email")
        address_ent = add_field("Юридический адрес")
        inn_ent = add_field("ИНН")
        Label(form, text="Рейтинг (0-10)", bg="#FFF8DC", anchor="w").pack(fill=X, pady=(6,2))
        rating_spin = Spinbox(form, from_=0, to=10)
        rating_spin.pack(fill=X)

        if is_edit:
            p = session.get(Partner, edit_id)
            if p:
                org_box.set(p.org_type or "")
                name_ent.insert(0, p.org_name)
                director_ent.insert(0, p.director or "")
                phone_ent.insert(0, p.phone or "")
                email_ent.insert(0, p.email or "")
                address_ent.insert(0, p.address or "")
                inn_ent.insert(0, p.inn or "")
                rating_spin.delete(0, "end")
                rating_spin.insert(0, str(p.rating or 0))

        def save_partner():
            try:
                org_type = org_box.get().strip()
                name = name_ent.get().strip()
                if not name:
                    messagebox.showwarning("Внимание", "Наименование обязательно")
                    return
                director = director_ent.get().strip()
                phone = phone_ent.get().strip()
                email = email_ent.get().strip()
                address = address_ent.get().strip()
                inn = inn_ent.get().strip()
                rating = int(rating_spin.get())
                if is_edit:
                    p.org_type = org_type
                    p.org_name = name
                    p.director = director
                    p.phone = phone
                    p.email = email
                    p.address = address
                    p.inn = inn
                    p.rating = rating
                else:
                    new_p = Partner(
                        org_type=org_type, org_name=name, director=director,
                        phone=phone, email=email, address=address, inn=inn, rating=rating
                    )
                    session.add(new_p)
                session.commit()
                load_partners(search_var.get())
                w.destroy()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", str(e))

        Button(w, text="Сохранить", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
               width=12, command=save_partner).pack(pady=10)
        Button(w, text="Отмена", bg="#F44336", fg="white", font=("Arial", 10, "bold"),
               width=12, command=w.destroy).pack()

    def add_partner():
        open_partner_window(None)

    def edit_partner():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Ошибка", "Выберите запись")
            return
        pid = tree.item(sel[0])["values"][0]
        open_partner_window(pid)

    def delete_partner():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Ошибка", "Выберите запись")
            return
        if not messagebox.askyesno("Подтвердите", "Удалить выбранного партнёра?"):
            return
        pid = tree.item(sel[0])["values"][0]
        try:
            session.query(Partner).filter_by(id=pid).delete()
            session.commit()
            load_partners(search_var.get())
        except Exception as e:
            session.rollback()
            messagebox.showerror("Ошибка", str(e))

    bottom = Frame(win, bg="#FFF8DC")
    bottom.pack(pady=10, padx=10, fill=X)

    Button(bottom, text="Добавить", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
           width=12, command=add_partner).pack(side=LEFT, padx=5)
    Button(bottom, text="Изменить", bg="#66BB6A", fg="white", font=("Arial", 10, "bold"),
           width=12, command=edit_partner).pack(side=LEFT, padx=5)
    Button(bottom, text="Удалить", bg="#F44336", fg="white", font=("Arial", 10, "bold"),
           width=12, command=delete_partner).pack(side=LEFT, padx=5)
    Button(bottom, text="Обновить", bg="#FFA726", fg="white", font=("Arial", 10, "bold"),
           width=12, command=lambda: load_partners(search_var.get())).pack(side=LEFT, padx=5)
    Button(bottom, text="Назад", bg="#FF7043", fg="white", font=("Arial", 10, "bold"),
           width=12, command=win.destroy).pack(side=LEFT, padx=5)
