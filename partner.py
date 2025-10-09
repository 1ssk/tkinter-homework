#
# окно с продажами sales.py
#
#-------------------------------

from tkinter import *
from tkinter import ttk


def PartnerWindow():

    # Создаем главное окно
    Partner = Toplevel()
    Partner.title("Добавление партнера")
    Partner.geometry("800x600")
    
    # Контент главного окна
    Label(Partner, text="Партнер").pack()
    Label(Partner, text="Добавление информации о партнере").pack()

    Label(Partner, text="Тип организации").pack()
    org = ["ooo", "ip"]
    ttk.Combobox(Partner, values=org).pack()

    Label(Partner, text="Наименование организации").pack()
    Entry(Partner, text="Введите название организации").pack()

    Label(Partner, text="ФИО директора").pack()
    Entry(Partner, text="Введите название организации").pack()
    
    Label(Partner, text="Телефон").pack()
    Entry(Partner, text="Введите название организации").pack()
    
    Label(Partner, text="Email").pack()
    Entry(Partner, text="Введите название организации").pack()
    
    Label(Partner, text="Юридический адрес").pack()
    Entry(Partner, text="Введите название организации").pack()
    
    Label(Partner, text="ИНН").pack()
    Entry(Partner, text="Введите название организации").pack()

    Label(Partner, text="Рейтинг (0-10)").pack()
    Entry(Partner, text="Введите название организации").pack()

