#
# окно с продажами sales.py
#
#-------------------------------

from tkinter import *
from tkinter import ttk

def SalesWindow():
    
    sales = Toplevel()
    sales.title("Продажи")
    sales.geometry("800x600")
    
    # Контент главного окна
    Label(sales, text="Добавление продажи").pack()


    Label(sales, text="Продукт").pack()
    test = ["1", "2", "3"]
    ttk.Combobox(sales, values=test).pack()

    Label(sales, text="Количество").pack()
    ttk.Combobox(sales, values=test).pack()

    Label(sales, text="Цена").pack()
    Entry().pack()

    Button(sales, text="Сохранить").pack()

    Button(sales, text="Отмена").pack()
    

