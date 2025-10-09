# 
# Образец 05.09 main.py
#
# Обзор https://metanit.com/python/tkinter/2.2.php
#
# -------------------------

from tkinter import *
from switch import SwitchWindow


auth = Tk()
auth.title("Мастер пол")
auth.iconbitmap(default="favicon.ico")
auth.geometry("600x500")
auth.configure(bg="#FFF8DC")

python_logo = PhotoImage(file="./images.png")

def auth_b():
    if login.get() == "1" and password.get() == "1":
        print("Логин:", login.get(), "Пароль:", password.get())
        SwitchWindow(auth)
    else:
        print("неправильно")

# Указываем фон для всех виджетов
Label(auth, image=python_logo, compound="top", bg="#FFF8DC").pack(pady=20)

# Фрейм для логина с выравниванием меток слева
login_frame = Frame(auth, bg="#FFF8DC")
login_frame.pack(pady=10)

Label(login_frame, text="Логин:", width=8, anchor="e", bg="#FFF8DC").pack(side=LEFT, padx=5)
login = Entry(login_frame, width=20)
login.pack(side=LEFT, padx=5)

# Фрейм для пароля с выравниванием меток слева
password_frame = Frame(auth, bg="#FFF8DC")
password_frame.pack(pady=10)

Label(password_frame, text="Пароль:", width=8, anchor="e", bg="#FFF8DC").pack(side=LEFT, padx=5)
password = Entry(password_frame, show="*", width=20)
password.pack(side=LEFT, padx=5)

Button(auth, text="Войти", command=auth_b, 
       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
       width=10, padx=3, pady=3).pack(pady=15)


auth.mainloop()