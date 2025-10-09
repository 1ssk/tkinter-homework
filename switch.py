#
# окно с выбором в какое окно переходить sales.py
#
#-------------------------------

from tkinter import *
from product import ProductWindow
from sales import SalesWindow
from partner import PartnerWindow

def SwitchWindow(auth):
    """Создает главное окно"""
    # Закрываем окно авторизации
    auth.withdraw()
    
    # Создаем главное окно
    switch = Toplevel()
    switch.title("Главное меню")
    switch.geometry("800x600")
    
    # Контент главного окна
    Label(switch, text="Добро пожаловать!").pack()
    

    Button(switch, text="Продукты", command=lambda: ProductWindow()).pack()

    Button(switch, text="Продажи", command=lambda: SalesWindow()).pack()

    Button(switch, text="Партнеры", command=lambda: PartnerWindow()).pack()





