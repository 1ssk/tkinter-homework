# 
# Образец 05.09
#
# Обзор https://metanit.com/python/tkinter/2.2.php
#
# -------------------------

from tkinter import *
from switch_window import SwitchWindow


r = Tk()
r.title("Мастер пол")
r.iconbitmap(default="favicon.ico")
r.geometry("600x400")

python_logo = PhotoImage(file="./images.png")

def auth_b():
    if login.get() == "1" and password.get() == "1":
        print("Логин:", login.get(), "Пароль:", password.get())
        SwitchWindow(r)
    else:
        print("неправильно")

Label(image=python_logo, compound="top").pack()

Label(text="Логин").pack()
login = Entry()
login.pack()

l = Label(text="Пароль").pack()
password = Entry(show="*")
password.pack()

Button(text="Войти", command=auth_b).pack()

r.mainloop()